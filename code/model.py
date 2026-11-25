"""Memoria financial model.

Single source of truth for every number and figure in the report.
Run:  python code/model.py      (from the repository root)
Outputs: figures/*.pdf and figures/numbers.tex (LaTeX macros used by the chapters).
Deterministic: no randomness except a seeded Monte-Carlo with seed 2611.
"""
import inspect
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# ---- palette (must match memoria.cls) -------------------------------------------
TEAL, TEAL_D, AMBER, SEPIA, PAPER, INK, GREY = (
    "#0B5563", "#073B45", "#E0A030", "#8A6A4B", "#FBF6EC", "#1F2A30", "#6B7780")

for p in Path.home().glob("AppData/Local/Programs/MiKTeX/fonts/opentype/public/libertinus-fonts/*Sans-Regular.otf"):
    font_manager.fontManager.addfont(str(p))
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=str(p)).get_name()
plt.rcParams.update({
    "axes.facecolor": PAPER, "figure.facecolor": "white", "axes.edgecolor": GREY,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": "#E4DCCB", "grid.linewidth": 0.7, "font.size": 10,
})

# ---- risk register (probability, impact), in table order -------------------------
RISKS = [(2, 5), (3, 4), (4, 3), (3, 4), (2, 3), (2, 3)]


def risk_marker_tex():
    """TikZ marker nodes for the risk map. Markers sharing a grid cell are spread
    horizontally and centred on the cell, so none can hide another (incident I-13)."""
    cells = {}
    for n, rc in enumerate(RISKS, 1):
        cells.setdefault(rc, []).append(n)
    out = []
    for (p, i), ids in cells.items():
        for k, n in enumerate(ids):
            dx = (k - (len(ids) - 1) / 2) * 0.30
            out.append(r"\node[circle,fill=mtealdark,text=white,font=\sffamily\tiny\bfseries,"
                       rf"inner sep=1.4pt] at ({p + dx:.2f},{i}) {{\num{{{n}}}}};")
    return "\n".join(out) + "\n"


# ---- assumptions (ILS) -----------------------------------------------------------
TIERS = {  # name: (price per order, variable cost per order, share of orders)
    "Basic":    (390.0,   85.0, 0.55),
    "Pro":      (790.0,  190.0, 0.35),
    "Heritage": (2900.0, 780.0, 0.10),
}
MONTHS = 36
HIRE3_MONTH = 13      # third employee starts: salaries and marketing step up in this month
ADS_MONTH = 7         # paid advertising (Google Ads) starts; chapter 6 channel table
HOSTING_MONTH = 1     # archive subscription is sold from the first month
HOSTING_PRICE, HOSTING_COST, HOSTING_ATTACH, CHURN = 19.0, 3.0, 0.30, 0.02
INVESTMENT = 250_000.0


# ---- launch timeline: (label, first month, last month, colour); months are 1-based ----
GANTT = [
    ("Setup and hiring", 1, 3, "mteal"),
    ("Pilot, 30 families", 3, 8, "mteal"),
    ("Local launch", ADS_MONTH, 18, "mamber"),
    ("Paid ads", ADS_MONTH, MONTHS, "msepia"),
    ("Third hire", HIRE3_MONTH, MONTHS, "msepia"),
    ("Nationwide and B2B", 19, MONTHS, "mtealdark"),
    ("Archive subscriptions", HOSTING_MONTH, MONTHS, "mamber"),
]


def gantt_tex():
    """Bars of the launch timeline. Month m occupies the interval [m-1, m] on the axis."""
    out = []
    for row, (label, a, b, colour) in enumerate(GANTT):
        y = len(GANTT) - 1 - row
        out.append(rf"\fill[{colour},rounded corners=1pt] ({a - 1},{y}) rectangle ({b},{y + 0.45});")
        out.append(rf"\node[anchor=east,font=\sffamily\scriptsize] at (-0.5,{y + 0.22}) {{{label}}};")
    return "\n".join(out) + "\n"


def orders(t):
    """Orders per month: ramp from 25 toward 200 (saturating growth)."""
    return 25 + 175 * (1 - np.exp(-t / 14.0))


def fixed_costs(t):
    salaries = np.where(t < HIRE3_MONTH, 32_000, 48_000)          # 2 then 3 staff
    marketing = np.where(t < HIRE3_MONTH, 6_000, 8_000)
    return salaries + marketing + 4_500 + 3_500 + 2_000  # rent, GPU/software, other


def run(price_factor=1.0, volume_factor=1.0):
    t = np.arange(1, MONTHS + 1)
    n = orders(t) * volume_factor
    avg_price = sum(p * s for p, _, s in TIERS.values()) * price_factor
    avg_var = sum(v * s for _, v, s in TIERS.values())
    customers = np.zeros(MONTHS)
    subs = 0.0
    for i in range(MONTHS):
        subs = subs * (1 - CHURN) + (n[i] * HOSTING_ATTACH if i + 1 >= HOSTING_MONTH else 0.0)
        customers[i] = subs
    revenue = n * avg_price + customers * HOSTING_PRICE
    var = n * avg_var + customers * HOSTING_COST
    fixed = fixed_costs(t)
    profit = revenue - var - fixed
    cash = -INVESTMENT + np.cumsum(profit)
    return dict(t=t, n=n, revenue=revenue, var=var, fixed=fixed, profit=profit,
                cash=cash, avg_price=avg_price, avg_var=avg_var, subs=customers)


def first_positive(x):
    idx = np.where(x > 0)[0]
    return int(idx[0]) + 1 if len(idx) else None


def save(name):
    plt.tight_layout()
    plt.savefig(FIG / name, format="pdf", bbox_inches="tight")
    plt.close()


def fig_revenue_costs(r):
    plt.figure(figsize=(6.6, 3.4))
    plt.stackplot(r["t"], r["var"], r["fixed"], colors=[SEPIA, TEAL_D], alpha=0.85,
                  labels=["Variable cost", "Fixed cost"])
    plt.plot(r["t"], r["revenue"], color=AMBER, lw=2.6, label="Revenue")
    plt.xlabel("Month"); plt.ylabel("ILS / month"); plt.legend(frameon=False, loc="upper left")
    plt.gca().yaxis.set_major_formatter(lambda v, _: f"{int(v/1000)}k")
    save("revenue_costs.pdf")


def fig_cash(r):
    plt.figure(figsize=(6.6, 3.2))
    c = r["cash"]
    plt.plot(r["t"], c / 1000, color=TEAL, lw=2.6)
    plt.fill_between(r["t"], c / 1000, 0, where=c >= 0, color=AMBER, alpha=0.35)
    plt.fill_between(r["t"], c / 1000, 0, where=c < 0, color=SEPIA, alpha=0.25)
    pb = first_positive(c)
    if pb:
        plt.axvline(pb, color=GREY, ls="--", lw=1)
        plt.text(pb + 0.4, c.min() / 1000 * 0.5, f"payback: month {pb}", color=INK)
    plt.axhline(0, color=INK, lw=0.8)
    plt.xlabel("Month"); plt.ylabel("Cumulative cash, k ILS")
    save("cash.pdf")


def fig_breakeven(r):
    t_ = np.arange(1, MONTHS + 1)
    f = fixed_costs(t_)
    cm = r["avg_price"] - r["avg_var"]
    plt.figure(figsize=(6.6, 3.2))
    plt.plot(t_, f / cm, color=SEPIA, lw=2.2, label="Break-even orders  F / (p - v)")
    plt.plot(t_, r["n"], color=TEAL, lw=2.6, label="Orders per month")
    m = first_positive(r["n"] - f / cm)
    if m:
        plt.scatter([m], [r["n"][m - 1]], color=AMBER, s=70, zorder=5)
        plt.annotate(f"month {m}", (m, r["n"][m - 1]), textcoords="offset points", xytext=(8, -16))
    plt.xlabel("Month"); plt.ylabel("Orders"); plt.legend(frameon=False)
    save("breakeven.pdf")


def unit_table_tex():
    """Body rows of the unit-economics table (chapter 4): price, variable cost, contribution, rate."""
    f = lambda v: f"{int(round(v)):,}".replace(",", "{,}")
    rows = []
    for name, (price, var, _) in TIERS.items():
        c = price - var
        rows.append(rf"\en{{{name}}} & \num{{{f(price)}}} & \num{{{f(var)}}} & \num{{{f(c)}}} & "
                    rf"\num{{{c / price * 100:.0f}}}\% \\")
    return "\n".join(rows) + "\n"


def fig_mix():
    names = list(TIERS)
    rev = [TIERS[k][0] * TIERS[k][2] for k in names]
    con = [(TIERS[k][0] - TIERS[k][1]) * TIERS[k][2] for k in names]
    x = np.arange(len(names)); w = 0.38
    plt.figure(figsize=(5.4, 3.2))
    plt.bar(x - w / 2, rev, w, color=TEAL, label="Revenue per average order")
    plt.bar(x + w / 2, con, w, color=AMBER, label="Contribution margin")
    plt.xticks(x, names); plt.ylabel("ILS per average order")
    plt.ylim(0, max(rev + con) * 1.35)             # headroom so the legend never overlaps bars (I-17)
    plt.legend(frameon=False, loc="upper left")
    save("tier_mix.pdf")


def fig_sensitivity():
    pf = np.linspace(0.8, 1.2, 9); vf = np.linspace(0.6, 1.4, 9)
    z = np.array([[run(p, v)["cash"][-1] / 1e6 for p in pf] for v in vf])
    plt.figure(figsize=(5.6, 3.8))
    im = plt.imshow(z, origin="lower", aspect="auto", cmap="YlGnBu",
                    extent=[pf[0] * 100, pf[-1] * 100, vf[0] * 100, vf[-1] * 100])
    plt.grid(False); plt.colorbar(im, label="Cash after 36 months, M ILS")
    plt.xlabel("Price level, % of plan"); plt.ylabel("Order volume, % of plan")
    save("sensitivity.pdf")


def monte_carlo(runs=2000):
    rng = np.random.default_rng(2611)
    end = []
    for _ in range(runs):
        end.append(run(rng.normal(1.0, 0.06), rng.normal(1.0, 0.18))["cash"][-1])
    end = np.array(end)
    plt.figure(figsize=(5.6, 3.0))
    plt.hist(end / 1e6, bins=30, color=TEAL, edgecolor="white")
    plt.axvline(0, color=AMBER, lw=2)
    plt.xlabel("Cash after 36 months, M ILS"); plt.ylabel("Scenarios")
    save("montecarlo.pdf")
    return float((end > 0).mean()), float(np.percentile(end, 10)), float(np.percentile(end, 90))


def main():
    r = run()
    fig_revenue_costs(r); fig_cash(r); fig_breakeven(r); fig_mix(); fig_sensitivity()
    p_pos, p10, p90 = monte_carlo()
    worst = min(run(p, v)["cash"][-1] for p in (0.8, 1.2) for v in (0.6, 1.4))
    cm = r["avg_price"] - r["avg_var"]
    be_m = first_positive(r["profit"]); pb_m = first_positive(r["cash"])
    fmt = lambda v: f"{int(round(v)):,}".replace(",", "{,}")
    macros = {
        "AvgOrderPrice": fmt(r["avg_price"]), "AvgOrderVar": fmt(r["avg_var"]),
        "ContribPerOrder": fmt(cm), "BreakEvenMonth": str(be_m), "PaybackMonth": str(pb_m),
        "BreakEvenOrdersEarly": str(int(np.ceil(fixed_costs(np.array([6]))[0] / cm))),
        "Investment": fmt(INVESTMENT),
        "RevenueYearOne": fmt(r["revenue"][:12].sum()), "RevenueYearThree": fmt(r["revenue"][24:].sum()),
        "ProfitYearThree": fmt(r["profit"][24:].sum()), "CashEnd": fmt(r["cash"][-1]),
        "ProbPositive": f"{p_pos*100:.0f}", "McTen": fmt(p10), "McNinety": fmt(p90),
        "OrdersEnd": str(int(round(r["n"][-1]))), "SensWorstLoss": fmt(abs(worst)),
    }
    for n, (p, i) in enumerate(RISKS):
        macros[f"RiskP{chr(97 + n)}"] = str(p); macros[f"RiskI{chr(97 + n)}"] = str(i)
    macros["UnitRows"] = unit_table_tex().strip()   # \input inside tabularx breaks; a macro does not
    excerpt = inspect.getsource(orders) + "\n\n" + inspect.getsource(fixed_costs).rstrip() + "\n"
    (FIG / "model_excerpt.py").write_text(excerpt, encoding="utf-8")
    (FIG / "gantt.tex").write_text(gantt_tex(), encoding="utf-8")
    macros.update(HireThree=str(HIRE3_MONTH), TwoStaffUntil=str(HIRE3_MONTH - 1),
                  AdsStart=str(ADS_MONTH), HostingStart=str(HOSTING_MONTH))
    (FIG / "riskmap.tex").write_text(risk_marker_tex(), encoding="utf-8")
    lines = [f"\\newcommand{{\\M{k}}}{{{v}}}" for k, v in macros.items()]
    (FIG / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(macros)


if __name__ == "__main__":
    main()
