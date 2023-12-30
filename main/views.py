from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.models import Product
from main.serializers import ProductSerializers
# Create your views here.


@api_view(['GET'])
def products_view(request):
    products = Product.objects.all()
    # list_ = [model_to_dict(product) for product in products]
    serializer = ProductSerializers(products, many=True)
    return Response(data=serializer.data)




@api_view(['GET'])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    product = Product.objects.get(id=id)
    # list_ = [model_to_dict(product) for product in products]
    serializer = ProductSerializers(product, many=False)
    return Response(data=serializer.data)



@api_view(['GET'])
def test_view(request):
    dict_ = {
        'text': 'hello world',
        'int': 1000,
        'float': 9.9,
        'bool': False,
        'dict': {
            'dict_child': {
                'int': 10
            }
        },
        'list': [1,2,3,4, 'Beka']
    }
    return Response(data=dict_)



