def get_dashboard_url(user):

    if user.is_superuser:
        return "/dashboard/admin/"

    if user.role == "DOCTOR":
        return "/dashboard/doctor/"

    if user.role == "PATIENT":
        return "/dashboard/patient/"

    return "/"