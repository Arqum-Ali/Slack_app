import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from myapp.routing import websocket_urlpatterns
from .hello import JWTAuthMiddleware  # Import your custom JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns
                
            
        ),
    ),
})
