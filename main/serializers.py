from rest_framework import serializers
from main.models import Product, Category, Tag, Review
from rest_framework.exceptions import ValidationError



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
    
class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=8, max_length=100)
    price = serializers.FloatField(min_value=1)
    quantity = serializers.IntegerField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))


    def validate_category_id(self, category_id):
        categories = Category.objects.filter(id=category_id)
        if len(categories) == 0:
            raise ValidationError(f'Category with id({category_id}) does not exists')
        return category_id
    
    def validate_tags(self, tags):
        tags_db = Tag.objects.filter(id__in=tags)
        if len(tags) != len(tags_db):
            raise ValidationError("Tag does not exists")
        return tags