from django.urls import path

from . import views

app_name = "materials"

urlpatterns = [
    path("", views.material_list, name="list"),
    path("save/", views.material_save, name="save"),
    path("upload/", views.material_upload, name="upload"),
    path("upload/<int:pk>/", views.material_preview, name="preview"),
    path("upload/<int:pk>/apply/", views.material_apply, name="apply"),
    path("upload/<int:pk>/cancel/", views.material_cancel, name="cancel"),
    path("upload/<int:pk>/issues.xlsx", views.material_issues, name="issues"),
    path("download.xlsx", views.material_download, name="download"),
    path("history.xlsx", views.material_history, name="history"),
    path("template.xlsx", views.material_template, name="template"),
]
