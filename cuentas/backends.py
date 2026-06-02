from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameBackend(ModelBackend):
    """Permite iniciar sesión con username o correo electrónico."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        User = get_user_model()
        identificador = username.strip()

        if '@' in identificador:
            try:
                user = User.objects.get(email__iexact=identificador)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username__iexact=identificador)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
