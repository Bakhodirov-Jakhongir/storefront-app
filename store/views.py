from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.

#all products
@api_view()
def product_list(request):
    return Response('ok')
    
#retrieve single product
@api_view()
def product_detail(request,id):
    return Response(id)