from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags= models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    @property
    def filtered_reviews(self):
        return self.reviews.filter(stars__gte=4)
    
    @property
    def rating(self):
        reviews = self.filtered_reviews
        count = reviews.count()
        total = 0
        for i in reviews:
            total += i.stars
        try:
            return total / count
        except ZeroDivisionError:
            return 0
    




STAR_CHOISE = (
    (1,'*'),
    (2,'* *'),
    (3,'* * *'),
    (4,'* * * *'),
    (5,'* * * * *'),
)
class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STAR_CHOISE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text
