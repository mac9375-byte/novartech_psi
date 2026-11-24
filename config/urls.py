from django.urls import include, path

urlpatterns = [
    path("", include("accounts.urls")),
    path("material-master/", include("materials.urls")),
    path("assy-master/", include("assies.urls")),
]
