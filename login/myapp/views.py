import jwt
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from .serializers import *
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




from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Channel, ChannelMember
from .serializers import ChannelSerializer, ChannelMemberSerializer



class ChannelCreateView(generics.CreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        channel = serializer.save()
        ChannelMember.objects.create(user=self.request.user, channel=channel)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'channel': response.data,
            'member': ChannelMemberSerializer(ChannelMember.objects.get(user=request.user, channel_id=response.data['id'])).data
        }, status=status.HTTP_201_CREATED)
    




class AddMemberView(generics.CreateAPIView):
    queryset = ChannelMember.objects.all()
    serializer_class = ChannelMemberSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        channel_id = request.data.get('channel_id')
        member, created = ChannelMember.objects.get_or_create(user_id=user_id, channel_id=channel_id)
        if created:
            return Response(self.get_serializer(member).data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Member already in channel'}, status=status.HTTP_400_BAD_REQUEST)





class ChannelMemberListView(generics.ListAPIView):
    serializer_class = ChannelMembergetSerializer

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']  # Assuming you pass channel_id in URL params or query params
        return ChannelMember.objects.filter(channel_id=channel_id)
    



class ChannelDeleteView(generics.DestroyAPIView):
    queryset = Channel.objects.all()
    lookup_url_kwarg = 'channel_id'  # URL keyword argument for channel ID
    lookup_field = 'id'  # Field to use for looking up the channel

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Channel deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class ChannelUpdateView(generics.UpdateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_url_kwarg = 'channel_id'  # URL keyword argument for channel ID
    lookup_field = 'id'  # Field to use for looking up the channel

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    




@api_view(['POST','GET'])
def invite_user(request):
    if request.method == 'POST':
        user=request.user
        # Handle POST request logic here
        data = request.data
        serializer = EmailSerializer(data=data)
        
        if serializer.is_valid(raise_exception=False):
            email_of_user = serializer.validated_data.get('email')
            
            # Check if the email already exists in the CustomUser model
            if User.objects.filter(email=email_of_user).exists():
                return Response({'status': 400, 'message': 'The user already have an acount '})
            else:
                # Generate a token with the email embedded
                token = generate_token(email_of_user)

                # Send the email with the token embedded
                send_email(email_of_user, token,user)

                return Response({'status': 200, 'payload': serializer.data, 'message': 'The email has been sent with token'})
        else:
            return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong in sending email'})
def send_email(email, token,user):
    subject = f'You are invited by the {user} in the slack'
    verification_link = f'http://localhost:3000/register_password/{token}'
    message = f'Click on the link to verify: {verification_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    print("Email sent to:", email)

