from django.shortcuts import  get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from . models import Product
from . serializers import ProductSerializer

# Create your views here.

#all products
@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set , many=True)
    return Response(serializer.data)

#retrieve single product
@api_view()
def product_detail(request,id):
        product = get_object_or_404(Product , pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

