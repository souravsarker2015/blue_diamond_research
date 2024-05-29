from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.company.api.serializers import CompanySerializer
from apps.company.usecases import AllCompanyListUseCase
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class CompanyCreate(CreateAPIView):
    serializer_class = CompanySerializer
    queryset = AllCompanyListUseCase().execute()

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Company"], )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CompanyListApiView(ListAPIView):
    serializer_class = CompanySerializer
    queryset = AllCompanyListUseCase().execute()

    @swagger_auto_schema(tags=["Company"], )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CompanyRetrieveAPIView(RetrieveAPIView):
    serializer_class = CompanySerializer
    queryset = AllCompanyListUseCase().execute()

    @swagger_auto_schema(tags=["Company"], )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CompanyUpdateApiView(UpdateAPIView):
    serializer_class = CompanySerializer
    queryset = AllCompanyListUseCase().execute()

    @swagger_auto_schema(tags=["Company"], )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Company"], )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CompanyDestroyAPIView(DestroyAPIView):
    serializer_class = CompanySerializer
    queryset = AllCompanyListUseCase().execute()

    @swagger_auto_schema(tags=["Company"], )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
