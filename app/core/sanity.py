def sanity_check(control_users, control_conv, treat_users, treat_conv):
    warnings = []
    if control_users < 100 or treat_users < 100:
        warnings.append("Малая выборка (< 100)")
    if control_conv > control_users or treat_conv > treat_users:
        warnings.append("Конверсий больше, чем пользователей")
    ratio = treat_users / control_users if control_users > 0 else 0
    if not (0.95 <= ratio <= 1.05):
        warnings.append(f"Нарушен сплит: ratio={ratio:.2f}")
    if (control_conv / max(control_users, 1)) > 0.9:
        warnings.append("Baseline > 90% — возможно неверная метрика")
    return {"warnings": warnings, "ok": len(warnings) == 0}
