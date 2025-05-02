from .models import User
from django.contrib.auth.hashers import check_password

class Authentication:
    def signin(self, email: str, password: str) -> User | bool:
        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            return user
        
        return False
    
    def signup(self, email: str, password: str, name_user: str) -> User | bool:
        if User.objects.filter(email=email).exists():
            return False

        user = User(
            email=email,
            name_user=name_user,
        )

        user.set_password(password)
        user.save()

        return user
        