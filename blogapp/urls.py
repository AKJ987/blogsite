from django.urls import path
from blogapp import views
urlpatterns = [
    path('accounts/register', views.UserRegistrationView.as_view(), name='reg'),
    path('accounts/signin', views.LoginView.as_view(), name='signin'),
    path('home', views.IndexView.as_view(), name='home'),
    path('users/profile', views.ProfileCreationView.as_view(), name='profile'),
    path('users/signout', views.signout, name='signout'),
    path('users/viewprofile', views.ViewMyProfileView.as_view(), name='viewprofile'),
    path('users/passwordreset', views.PasswordResetView.as_view(), name='passreset'),
    path('users/profile/change/<int:user_id>', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('users/blog', views.BlogCreateView.as_view(), name='blog_create'),
    path('posts/comment/<int:post_id>', views.add_comment, name='add_comment'),
    path('posts/like/add/<int:post_id>', views.add_like, name='add_like')
]