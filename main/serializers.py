from rest_framework import serializers
from main.models import Product


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['id', 'title', 'text', 'price']
        fields = '__all__'
        # fields = 'id title price quantity'.split()
