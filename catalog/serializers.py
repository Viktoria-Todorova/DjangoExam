from rest_framework import serializers
from .models import Catalog

class CatalogSerializer(serializers.ModelSerializer):
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'title', 'writer', 'genre_display', 'quantity']
