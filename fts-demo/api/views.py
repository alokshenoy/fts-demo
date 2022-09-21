from django.shortcuts import render
from django.db.models import Q
from django.db.models.expressions import Window, F
from django.db.models.functions import RowNumber, Greatest
from django.db.models import Value

from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
    TrigramWordSimilarity,
    SearchHeadline
)

import random
import logging

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.db import connections, OperationalError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import product
from .serializers import ProductSerializer

logger = logging.getLogger(__name__)


class Ping(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Health check, select 1 on current db connection
        """
        open_connections = connections.all()
        if not open_connections:
            logger.debug("Failed to get DB conn")
            return Response(status=500)
        conn = random.choice(open_connections)
        try:
            cursor = conn.cursor()
            cursor.execute("select 1")
            health_check = cursor.fetchone()[0]
            if health_check != 1:
                logger.debug("Health query failed")
                return Response(status=500)
        except OperationalError:
            logger.exception("Ping failure")
            return Response(status=500)
        return Response({}, status=200)


class APIPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "page_size": self.page_size,
                "total_objects": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page_number": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


# Create your views here.
class Like(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = APIPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_dict = self.request.GET
        query = query_dict.get("query")
        print("Query: ", query)
        if query:
            paragraphs = product.objects.filter(Q(product_name__contains=query)|Q(product_description__contains=query))

        else:
            paragraphs = product.objects.all()

        return paragraphs


class ProductDescription(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = APIPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_dict = self.request.GET
        query = query_dict.get("query")
        use_vector = query_dict.get("use_vector", False)
        print("Query: ", query)
        if query:
            query = SearchQuery(query, search_type="plain")
            rank = SearchRank(
                F("fts_vector_pd"),
                query,
                cover_density=False,
                normalization=Value(2),
            )

            if use_vector == "True":
                return product.objects.filter(fts_vector_pd=query).annotate(rank=rank).order_by("-rank")
            else:
                return product.objects.filter(product_description__search=query).annotate(headline=SearchHeadline("product_description", query, start_sel="****", stop_sel="****", highlight_all=True))
        else:
            return product.objects.all()

class ProductName(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = APIPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_dict = self.request.GET
        query = query_dict.get("query")
        use_vector = query_dict.get("use_vector", "False")
        print("Query: ", query)
        if query:
            query = SearchQuery(query, search_type="plain")
            if use_vector == "True":
                return product.objects.filter(fts_vector_name=query)
            else:
                return product.objects.filter(product_name__search=query)
        else:
            return product.objects.all()


class Product(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = APIPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_dict = self.request.GET
        query = query_dict.get("query")
        use_vector = query_dict.get("use_vector", "False")
        print("Query: ", query)
        if query:
            query = SearchQuery(query, search_type="plain")
            rank = SearchRank(
                F("fts_vector_all"),
                query,
                cover_density=False,
                normalization=Value(2),
            )
            if use_vector == "True":
                return product.objects.filter(fts_vector_all=query).annotate(rank=rank).order_by("-rank")
            else:
                return product.objects.filter(Q(product_description__search=query) | Q(product_name__search=query) | Q(brand__search=query))
        else:
            return product.objects.all()



class ProductPhrase(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = APIPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_dict = self.request.GET
        query = query_dict.get("query")
        use_vector = query_dict.get("use_vector", "False")
        print("Query: ", query)
        if query:
            query = SearchQuery(query, search_type="phrase")
            rank = SearchRank(
                F("fts_vector_all"),
                query,
                cover_density=False,
                normalization=Value(2),
            )
            if use_vector == "True":
                return product.objects.filter(fts_vector_all=query).annotate(rank=rank).order_by("-rank")
            else:
                return product.objects.filter(product_description__search=query)
        else:
            return product.objects.all()

class ProductTrigram(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = APIPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_dict = self.request.GET
        query = query_dict.get("query")
        use_vector = query_dict.get("use_vector", "False")
        print("Query: ", query)
        if query:
            trigram_similarity = Greatest(
                TrigramWordSimilarity(query, "product_name"),
                TrigramWordSimilarity(query, "product_description"),
                TrigramWordSimilarity(query, "brand"),
            )
            return product.objects.all().annotate(similarity=trigram_similarity).filter(similarity__gte=0.3).order_by("-similiarity")

        else:
            return product.objects.all()
