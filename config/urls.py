from django.urls import include, path

urlpatterns = [
    path("", include("accounts.urls")),
    path("material-master/", include("materials.urls")),
    path("assy-master/", include("assies.urls")),
    path("bom/", include("bom.views")),
    path("safety-stock/", include("safety.views")),
    path("", include("weekly.views")),
    path("", include("psi.views")),
]
