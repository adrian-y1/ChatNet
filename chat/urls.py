from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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
    path('change_password', views.change_password, name="change_password"),

    # Error Catching
    path('error', views.error_handling, name="error")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
