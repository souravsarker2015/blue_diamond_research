from drf_yasg import openapi
from rest_framework.exceptions import APIException


class EmailAlreadyExistsException(APIException):
    status_code = 403
    default_detail = 'Email already exists.'
    default_code = 'email_already_exists'


def company_id_header_params():
    company = openapi.Parameter(
        'company',
        openapi.IN_HEADER,
        description="company",
        type=openapi.IN_HEADER
    )

    return [company]
