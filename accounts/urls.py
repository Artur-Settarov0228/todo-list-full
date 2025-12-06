from django.urls import path
from .views import RegisterView, LoginView,  LogoutView, ProfileView, PasswordChangeView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),  # ✅ Foydalanuvchini ro‘yxatdan o‘tkazish endpoint
    path('auth/login/', LoginView.as_view()),        # ✅ Foydalanuvchi login qiladigan endpoint
    path('auth/logout/', LogoutView.as_view()),      # ✅ Foydalanuvchi tokenini o‘chirib logout qiladigan endpoint, headerda Authorization: Token <token> bo‘lishi kerak
    path('auth/profile/', ProfileView.as_view()),
    path('auth/change-password/', PasswordChangeView.as_view()),

]
