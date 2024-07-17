import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from asgiref.sync import sync_to_async

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        print("Entering JWTAuthMiddleware")
        query_string = parse_qs(scope['query_string'].decode())
        token_key = query_string.get('token')

        if token_key:
            print("Token found in query string")
            try:
                access_token = AccessToken(token_key[0])
                user_id = access_token['id']  # Extract 'id' from token
                user = await sync_to_async(User.objects.get)(id=user_id)
                scope['user'] = user
                print(f"Authenticated user: {user.username}")
            except Exception as e:
                print(f"Token authentication failed: {e}")
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
            print("No token found, setting user as AnonymousUser")

        return await super().__call__(scope, receive, send)
