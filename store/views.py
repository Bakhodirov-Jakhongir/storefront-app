from django.db.models.aggregates import Count
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers, status
from rest_framework.views import APIView
from . models import Collection, Product
from . serializers import ProductSerializer , CollectionSerializer
from rest_framework.generics import ListCreateAPIView
# Create your views here.

class ProductList(ListCreateAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('collection').all()

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}

    # def get(self , request):
    #     query_set = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(query_set , many=True , context = {'request':request})
    #     return Response(serializer.data)
    
    # def post(self , request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.save()
    #     return Response(serializer.data , status=status.HTTP_201_CREATED)


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


class CollectionList:
    def get(self , request , id):
        collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')) , pk=id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self , request , id):
        collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')) , pk=id)
        serializer = CollectionSerializer(collection , data=request.data)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self , request , id):
        collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')) , pk=id)
        if collection.products.count() > 0:
            return Response({'error':'Collection cannot be deleted because it includes one or more products.'} , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete();   
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
