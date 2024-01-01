from rest_framework import serializers
from main.models import Product, Category, Tag, Review




class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = 'id name'.split()



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields = 'id text stars'.split()

# class TagsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model= Tag
#         fields = 'id name'.split()

class ProductSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    tags = serializers.SerializerMethodField()
    filtered_reviews = ReviewSerializers(many=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'text', 'price']
        # fields = '__all__'
        fields = 'id title category tags price quantity filtered_reviews rating'.split()

    def get_tags(self, product):
        # первый способ:
        # list_ = []
        # for tag in product.tags.all():
        #     list_.append(tag.name)
        # return list_
        # второй способ:
        return [tag.name for tag in product.tags.all()]
