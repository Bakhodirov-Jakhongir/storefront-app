from django.shortcuts import  get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers, status
from . models import Product
from . serializers import ProductSerializer

# Create your views here.

#all products
@api_view(['GET' , 'POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection')
        serializer = ProductSerializer(query_set , many=True , context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        # serializer.validated_data 
        return Response(serializer.data , status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

#retrieve single product
@api_view(['GET' , 'PUT' , 'PATCH' , 'DELETE'])
def product_detail(request,id):
        product = get_object_or_404(Product , pk=id)
        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        elif request.method == 'PUT' or request.method == 'PATCH':
            serializer = ProductSerializer(product , data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if product.orderitems.count() > 0:
                return Response({'error' : 'product can not deleted!'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)     
    
@api_view()
def collection_detail(request , pk):
    return Response('ok')


