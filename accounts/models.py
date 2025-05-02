from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    avatar = models.TextField(default='/media/avatars/default-avatar.png')
    name_user = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_superuser
    
    class Meta:
        db_table = 'users'