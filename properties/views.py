from rest_framework.generics import ListAPIView
from .models import Property
from .serializers import PropertySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 15), name='get')
class PropertyListView(ListAPIView):
    """
    View to list all property listings.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

   
