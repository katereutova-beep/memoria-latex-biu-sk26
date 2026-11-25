def orders(t):
    """Orders per month: ramp from 25 toward 200 (saturating growth)."""
    return 25 + 175 * (1 - np.exp(-t / 14.0))


def fixed_costs(t):
    salaries = np.where(t < HIRE3_MONTH, 32_000, 48_000)          # 2 then 3 staff
    marketing = np.where(t < HIRE3_MONTH, 6_000, 8_000)
    return salaries + marketing + 4_500 + 3_500 + 2_000  # rent, GPU/software, other
