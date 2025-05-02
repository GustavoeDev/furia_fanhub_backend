from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.timezone import now

from rest_framework_simplejwt.tokens import RefreshToken

from .auth import Authentication
from .serializers import UserSerializer
from .models import User

from core.utils.exceptions import ValidationError

import uuid

class UserSignInView(APIView, Authentication):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        signin = self.signin(email, password)

        if not signin:
            raise AuthenticationFailed('E-mail ou senha inválidos.')
        
        user = UserSerializer(signin).data
        access_token = RefreshToken.for_user(signin).access_token

        return Response({
            'user': user,
            'access_token': str(access_token),
        })
    
class UserSignUpView(APIView, Authentication):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        name_user = request.data.get('name_user', '')

        if not email or not password or not name_user:
            raise AuthenticationFailed('Campos obrigatórios não preenchidos.')

        signup = self.signup(email, password, name_user)

        if not signup:
            raise AuthenticationFailed('E-mail ou nome de usuário já cadastrado.')
        
        user = UserSerializer(signup).data
        access_token = RefreshToken.for_user(signup).access_token

        return Response({
            'user': user,
            'access_token': str(access_token),
        })


class UserView(APIView):
    def get(self, request):
        User.objects.filter(id=request.user.id).update(last_login=now())

        user = UserSerializer(request.user).data

        return Response({
            'user': user,
        })
    
    def put(self, request):
        name_user = request.data.get('name_user')
        email = request.data.get('email')
        password = request.data.get('password')
        avatar = request.FILES.get('avatar')
        
        data = {
            'name_user': name_user,
            'email': email,
            'avatar': request.user.avatar
        }
        
        # Update avatar
        if avatar:
            content_type = avatar.content_type
            extension = avatar.name.split('.')[-1].lower() 

            if content_type not in ['image/jpeg', 'image/png'] or extension not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Suportamos apenas imagens JPEG e PNG')
            
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'avatars',
                settings.MEDIA_URL + 'avatars'
            )
            
            filename = f'{uuid.uuid4()}.{extension}'
            file = storage.save(filename, avatar)
            avatar_url = storage.url(file)
            data['avatar'] = avatar_url
        
        serializer = UserSerializer(request.user, data=data, partial=True)

        if not serializer.is_valid():
            if avatar:
                storage.delete(filename)
            
            first_error = list(serializer.errors.values())[0][0]
            raise ValidationError(first_error)
        
        old_avatar = request.user.avatar
        if avatar and old_avatar and old_avatar != "/media/avatars/default-avatar.png":
            try:
                old_filename = old_avatar.split('/')[-1]
                storage = FileSystemStorage(
                    settings.MEDIA_ROOT / 'avatars',
                    settings.MEDIA_URL + 'avatars'
                )
                storage.delete(old_filename)
            except Exception as e:
                pass
        
        if password:
            request.user.set_password(password)
        
        serializer.save()
        
        return Response({
            'user': serializer.data
        })