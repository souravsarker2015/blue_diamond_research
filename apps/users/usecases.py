from django.db.models import Q
from apps.core.use_cases import BaseUseCase
from apps.users.models import User
from oauth2_provider.oauth2_validators import AccessToken


class TokenDetailsUseCase(BaseUseCase):

    def __init__(self, filters: dict):
        self._filters = filters

    def execute(self):
        return self._factory()

    def _factory(self):
        self._token = AccessToken.objects.filter(**self._filters).first()
        return self._token


class TokenDeleteUseCase(BaseUseCase):

    def __init__(self, token_instance):
        self._token_instance = token_instance

    def execute(self):
        return self._delete_token()

    def _delete_token(self):
        if self._token_instance:
            print("Deleting token--------------------------------->>>>>>")
            print(self._token_instance)
            self._token_instance.delete()
            return True
        else:
            return False


class UserCreateUseCase(BaseUseCase):

    def __init__(self, user_data):
        self._user_data = user_data

    def execute(self):
        return self._create_user()

    def _create_user(self):
        self._user = User.objects.create(**self._user_data)
        return self._user


class UserUpdateUseCase(BaseUseCase):

    def __init__(self, user_instance, update_data):
        self._user_instance = user_instance
        self._update_data = update_data

    def execute(self):
        return self._update_user()

    def _update_user(self):
        if self._user_instance:
            for key, value in self._update_data.items():
                setattr(self._user_instance, key, value)
            self._user_instance.save()
            return self._user_instance
        else:
            return None


class UserExistsUseCase(BaseUseCase):

    def __init__(self, filters: dict):
        self._filters = filters

    def execute(self):
        return self._factory()

    def _factory(self):
        self._exists = User.objects.filter(**self._filters).exists()
        return self._exists


class UserListUseCase(BaseUseCase):

    def execute(self):
        return self._factory()

    def _factory(self):
        self._users = User.objects.all()
        return self._users


class UserDetailsUseCase(BaseUseCase):

    def __init__(self, filters: dict):
        self._filters = filters

    def execute(self):
        return self._factory()

    def _factory(self):
        self._user = User.objects.filter(**self._filters).first()
        return self._user


class UserPasswordSetUseCase(BaseUseCase):

    def __init__(self, user_instance, password: str):
        self._user_instance = user_instance
        self._password = password

    def execute(self):
        return self._update_user_password()

    def _update_user_password(self):
        if self._user_instance is not None:
            self._user_instance.set_password(self._password)
            self._user_instance.save()
            return self._user_instance
        else:
            return None
