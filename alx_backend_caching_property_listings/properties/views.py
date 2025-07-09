from rest_framework.generics import ListAPIView
from .serializers import PropertySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from . utils import get_all_properties


@method_decorator(cache_page(60 * 15), name='get')
class PropertyListView(ListAPIView):
    """
    View to list all property listings.
    """
    serializer_class = PropertySerializer
    
    def get_queryset(self):
        """
        Returns a queryset of all properties, either from cache or database.
        """
        return get_all_properties()
