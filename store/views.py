import decimal
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers, status
from rest_framework.views import APIView
from . models import Product
from . serializers import ProductSerializer

# Create your views here.

class ProductList(APIView):
    def get(self , request):
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set , many=True , context = {'request':request})
        return Response(serializer.data)
    
    def post(self , request):
        serializer = ProductSerializer(data=request.data)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self , request , id):
        product = get_object_or_404(Product , pk = id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self , request , id):
        product = get_object_or_404(Product , pk = id)
        serializer = ProductSerializer(product , data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def delete(self , request , id):
        product = get_object_or_404(Product , pk = id)
        if product.orderitems.count() > 0:
            return Response({'error' : 'product can not deleted!'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     

    
@api_view()
def collection_detail(request , pk):
    return Response('ok')


