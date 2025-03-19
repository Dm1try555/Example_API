from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Car
from .serializers import ProductSerializer, CarSerializer

def hello_world(request):
    return HttpResponse("Hello, World!")

@swagger_auto_schema(
    methods=["get"],
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Ваше имя", type=openapi.TYPE_STRING),
        openapi.Parameter('age', openapi.IN_QUERY, description="Ваш возраст", type=openapi.TYPE_INTEGER)
    ]
)
@api_view(["GET"])
def hello_dima(request):
    name = request.query_params.get('name', 'World')  # Получаем query параметр 'name', по умолчанию 'World'
    age = request.query_params.get('age', '18')  # Получаем query параметр 'age', по умолчанию '18'
    return Response({"message": f"Hello, {name, age}!"})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CarViewSet(mixins.CreateModelMixin, #  POST
                     mixins.RetrieveModelMixin, #  GET /id/
                     mixins.ListModelMixin,#  GET
                     mixins.DestroyModelMixin,  #  DELETE
                     viewsets.GenericViewSet): #basic class
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('brand', openapi.IN_QUERY, description="Фильтр по марке автомобиля", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        # Получаем query параметр 'brand'
        brand = request.query_params.get('brand', None)
        if brand:
            self.queryset = self.queryset.filter(brand=brand)
        return super().list(request, *args, **kwargs)