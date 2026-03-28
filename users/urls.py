from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import RegisterView, CustomLoginView, ProfileView, CheckUsernameView, ProfileEditView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/user/login/'), name='logout-cbv'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('check-username/', CheckUsernameView.as_view(), name='check-username'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit-profile'),

]
