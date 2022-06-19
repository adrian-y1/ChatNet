import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import chat.routing

# This means when a connection is made to the Channels development server, the ProtocolTypeRouter will first see if the connection is WebSocket (ws or wss),
# and if it is, it will be given to AuthMiddlewareStack
# The AuthMiddlewareStack will populate the connection's scope with a reference to the currently authenticated user, similar to to request objects inside of view.
# The URLRouter will examine the HTTP path of the connection to route it to a particular consumer based on the provided url patterns
application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})