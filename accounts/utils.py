def get_dashboard_url(user):
    if user.is_superuser or getattr(user,'role','') == "ADMIN":
        return "/dashboard/admin/"
    if getattr(user,'role','') == "DOCTOR":
        return "/dashboard/doctor/"
    return "/dashboard/patient/"
