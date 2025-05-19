from django.db import models


#models
class Category(models.Model):
    title = models.CharField(max_length=20)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    mainImage = models.ImageField(upload_to="Products")
    name = models.CharField(max_length=264)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='PreviewText')
    details = models.TextField(max_length=1000, verbose_name="Description")
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    # slug = models.SlugField()


    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

