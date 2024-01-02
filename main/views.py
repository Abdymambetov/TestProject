from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.models import Product
from main.serializers import ProductSerializers
# Create your views here.


@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        # list_ = [model_to_dict(product) for product in products]
        serializer = ProductSerializers(products, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        #1) Get data from body
        title = request.data.get('title')
        price = request.data.get('price')
        amount = request.data.get('quantity')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')
        #2) Create product by this data
        product = Product.objects.create(
            title=title,
            price=price,
            quantity=amount,
            category_id=category_id,
        )
        product.tags.set(tags)
        product.save()
        return Response(data=ProductSerializers(product).data,
                        status=status.HTTP_201_CREATED)




@api_view(['GET', 'DELETE', 'PUT'])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # list_ = [model_to_dict(product) for product in products]
        serializer = ProductSerializers(product, many=False)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        #1) Get data from body
        title = request.data.get('title')
        price = request.data.get('price')
        amount = request.data.get('quantity')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')
        
        #2) Create product by this data
        product.title = title
        product.price = price
        product.quantity = amount
        product.category_id = category_id
        product.tags.set(tags)
        product.save()
        return Response(data=ProductSerializers(product).data,
                        status=status.HTTP_201_CREATED)



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



