from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils import get_dashboard_url
from doctors.models import Doctor, Speciality

User = get_user_model()


def home(request):
    return render(request, "core/home.html", {
        "total_doctors": Doctor.objects.filter(is_active=True).count(),
        "specialities": Speciality.objects.all(),
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect(get_dashboard_url(user))

        return render(
            request,
            "accounts/login.html",
            {"error": "Identifiants incorrects."}
        )

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        un = request.POST.get("username", "").strip()
        em = request.POST.get("email", "").strip()
        fn = request.POST.get("first_name", "").strip()
        ln = request.POST.get("last_name", "").strip()
        pw = request.POST.get("password", "")
        pw2 = request.POST.get("password2", "")

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not username or not password:
            return render(request, "accounts/register.html",
                          {"error": "Nom d'utilisateur et mot de passe obligatoires."})

        if password != password2:
            return render(request, "accounts/register.html",
                          {"error": "Mots de passe différents."})

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html",
                          {"error": "Nom d'utilisateur déjà pris."})

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role="PATIENT"
        )

        # 🔥 FIX IMPORTANT POUR TEST (302 attendu)
        return redirect("login")

    return render(request, "accounts/register.html")

# def register_view(request):
#     # if request.method == "POST":

#     username = request.POST.get("username", "").strip()
#     password = request.POST.get("password", "")

#     # -------------------------
#     # MODE TEST CI (simple)
#     # -------------------------
#     if "password2" not in request.POST:
#         if username and password:
#             User.objects.create_user(
#                 username=username,
#                 password=password
#             )
#             return redirect("login")

#         return render(request, "accounts/register.html")


#         # -------------------------
#         # MODE FORMULAIRE COMPLET
#         # -------------------------
#     #     email = request.POST.get("email", "").strip()
#     #     first_name = request.POST.get("first_name", "").strip()
#     #     last_name = request.POST.get("last_name", "").strip()
#     #     password2 = request.POST.get("password2", "")

#     #     if password != password2:
#     #         return render(request, "accounts/register.html", {
#     #             "error": "Mots de passe différents."
#     #         })

#     #     if User.objects.filter(username=username).exists():
#     #         return render(request, "accounts/register.html", {
#     #             "error": "Nom d'utilisateur déjà pris."
#     #         })

#     #     User.objects.create_user(
#     #         username=username,
#     #         email=email,
#     #         first_name=first_name,
#     #         last_name=last_name,
#     #         password=password
#     #     )

#     #     return redirect("login")

#     # return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def doctors_view(request):
    q = request.GET.get("q", "").strip()
    sid = request.GET.get("speciality", "").strip()

    docs = Doctor.objects.filter(
        is_active=True
    ).select_related("user", "speciality")

    if q:
        docs = docs.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)
        )

    if sid:
        docs = docs.filter(speciality__id=sid)

    return render(
        request,
        "doctors/list.html",
        {
            "doctors": docs,
            "specialities": Speciality.objects.all(),
            "query": q,
            "selected_speciality": sid
        }
    )