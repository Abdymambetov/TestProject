from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.models import Product, Category, Tag
from main.serializers import ProductSerializers, ProductValidateSerializer, CategorySerializers, TagSerializers
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
# Create your views here.



class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    lookup_field = 'id'



class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    pagination_class = PageNumberPagination

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)



class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    lookup_field = 'id'

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)



class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST) 
        # or status.HTTP_406_NOT_ACCEPTABLE

        #1) Get data from body
        title = serializer.validated_data.get('title')
        price = serializer.validated_data.get('price')
        amount = serializer.validated_data.get('quantity')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
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



@api_view(['GET', 'POST'])
def products_view(request):
    print(request.user)
    if request.method == 'GET':
        products = Product.objects.all()
        # list_ = [model_to_dict(product) for product in products]
        serializer = ProductSerializers(instance=products, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST) 
        # or status.HTTP_406_NOT_ACCEPTABLE

        #1) Get data from body
        title = serializer.validated_data.get('title')
        price = serializer.validated_data.get('price')
        amount = serializer.validated_data.get('quantity')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
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
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
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





