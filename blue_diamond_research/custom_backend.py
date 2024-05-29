from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        company = request.META.get('HTTP_COMPANY')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("****************+++++++++++")
        print(username)
        print(password)
        print(company)

        UserModel = get_user_model()

        user = None
        if '@' in username:
            try:
                user = UserModel.objects.filter(company_id=company, email=username).first()
            except UserModel.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None
