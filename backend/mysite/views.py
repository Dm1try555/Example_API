from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Car
from .serializers import ProductSerializer, CarSerializer

def hello_world(request):
    return HttpResponse("Hello, World!")

@api_view(["GET"])
def hello_dima(request):
    return Response({"message": "Hello, Dima!"})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CarViewSet(mixins.CreateModelMixin,  #  POST
                     mixins.RetrieveModelMixin,  #  GET /id/
                     mixins.ListModelMixin,  #  GET
                     mixins.DestroyModelMixin,  #  DELETE
                     viewsets.GenericViewSet): #basic class
    queryset = Car.objects.all()
    serializer_class = CarSerializer
