from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# AbstractBaseUser로 CustomUser 만들면 CustomUserManager로 관리
# 커스텀하기 위해 UserManager을 사용하지 않고 BaseUserManager 사용
class CustomUserManager(BaseUserManager):
    # 필수 (Docs참고, Customizing authentication in Django)
    def create_user(self, username, password, **kwargs):  # username, password, 기타(dict형)을 파라미터로 받음
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

    def create_normaluser(self, username, password, **kwargs):
        self.create_user(username, password, **kwargs)

    # 필수 (Docs참고, Customizing authentication in Django)
    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        self.create_user(username, password, **kwargs)


# AbstractBaseUser: Django가 기본 제공하는 User모델을 대체하기 위해 사용되는 추상 클래스
# PermissionMixin: User 모델에 대한 권한을 부여하기 위해 사용되는 클래스
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'  # 인증시 username 필드로 유저 식별

    username = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()  # CustomUser는 CustomUserManager를 사용함

    @property  # is_staff를 속성처럼 사용
    def is_staff(self):
        return self.is_superuser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile", null=True)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname
