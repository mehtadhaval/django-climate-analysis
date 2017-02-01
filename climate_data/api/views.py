from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from climate_data.api.serializers import RequestSerializer
from climate_data.models import Request


class ClimateDataRequestView(ListCreateAPIView):
    queryset = Request.objects.all().order_by('-created').prefetch_related('region')
    serializer_class = RequestSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('region', 'status', 'type')
