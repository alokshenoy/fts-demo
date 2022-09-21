from dataclasses import fields
from rest_framework import serializers
from .models import product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = product
        exclude = ["fts_vector_name", "fts_vector_pd", "fts_vector_all"]