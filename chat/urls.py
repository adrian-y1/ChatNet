from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Chat Messaging
    path('', views.index, name="index"),
    path("chat/<str:username>/", views.chat_room, name="room"),
    path('chat/suggestions', views.suggestions, name="suggestions"),
    path("chat/profile/<int:user_id>", views.profile, name="profile"),
    path("chat/friends_list", views.friends_list, name="friends_list"),

    # Pagination API Endpoints
    path('chat/<str:username>/messages', views.paginate_msg, name="paginatemsg"),
    path('global_messages', views.paginate_global_msg, name="paginate_g_msg"),

    # User API Endpoints
    path('all_users', views.fetch_suggestions, name='all_users'),
    path('all_friends', views.fetch_friends, name='all_friends'),

    # Friend Requests
    path('incoming', views.incoming_requests, name="incoming"),
    path('outgoing', views.outgoing_requests, name="outgoing"),

    # Authentication
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='chat/password_reset.html'), name="reset_password"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='chat/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='chat/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='chat/password_reset_complete.html'), name="password_reset_complete"),

    # Error Catching
    path('error', views.error_handling, name="error")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
