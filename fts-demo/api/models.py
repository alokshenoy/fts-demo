from django.db import models
from django.contrib.postgres.search import SearchVectorField


# Create your models here.
# uniq_id,crawl_timestamp,product_url,product_name,product_category_tree,pid,retail_price,discounted_price,image,is_FK_Advantage_product,description,product_rating,overall_rating,brand,product_specifications

class product(models.Model):
    id = models.CharField(primary_key=True, max_length=500)
    product_name = models.CharField(max_length=500, null=True)
    category_tree = models.CharField(max_length=1000, null=True)
    brand = models.CharField(max_length=500, null=True)
    product_description = models.TextField(null=True)
    product_specifications = models.CharField(max_length=10000, null=True)
    fts_vector_name = SearchVectorField(null=True)
    fts_vector_pd = SearchVectorField(null=True)
    fts_vector_all = SearchVectorField(null=True)



