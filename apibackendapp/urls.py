# Default router is a class that automatically creates URLs for ViewSets
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register(r'employees', views.EmployeeViewSet)
router.register(r'department', views.DepartmentViewSet)
router.register(r'projects', views.ProjectViewSet)

# SignupAPIView and LoginAPIView are APIViews, not ViewSets
urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("login/", views.LoginAPIView.as_view(), name="user-login"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]

urlpatterns += router.urls