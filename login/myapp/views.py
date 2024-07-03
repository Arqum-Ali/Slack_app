import jwt
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from .serializers import EmailSerializer,MainUserSerializer
from django.contrib.auth.models import User

@api_view(['POST','GET'])
def sendmail(request):
    if request.method == 'POST':
        # Handle POST request logic here
        data = request.data
        serializer = EmailSerializer(data=data)
        
        if serializer.is_valid(raise_exception=False):
            email_of_user = serializer.validated_data.get('email')
            
            # Check if the email already exists in the CustomUser model
            if User.objects.filter(email=email_of_user).exists():
                return Response({'status': 400, 'message': 'The email already exists'})
            else:
                # Generate a token with the email embedded
                token = generate_token(email_of_user)

                # Send the email with the token embedded
                send_email(email_of_user, token)

                return Response({'status': 200, 'payload': serializer.data, 'message': 'The email has been sent with token'})
        else:
            return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong in sending email'})

def generate_token(email):
    # Define payload with email and expiration time
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }

    # Generate the token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
def send_email(email, token):
    subject = "Email must be verified"
    verification_link = f'http://localhost:3000/register_password/{token}'
    message = f'Click on the link to verify: {verification_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    print("Email sent to:", email)

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("hello")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)







@api_view(['POST'])
def adduser(request):
    data = request.data
    serializer = MainUserSerializer(data=data)

    if not serializer.is_valid(raise_exception=False):  # Handle validation errors
        return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong in saving user'})
    
    # Now that validation is done, you can safely access serializer.data
    print(serializer.validated_data, "in view")
    
    if User.objects.filter(email=serializer.validated_data['email']).exists():
        return Response({'status': 400, 'message': 'You already have an account'})
    else:
        password = make_password(request.data.get('password'))
        print("password1", password)
        serializer.validated_data['password'] = password
        serializer.save()
        print("password", password)
        return Response({'status': 200, 'payload': serializer.data, 'message': 'user saved successfully'})
