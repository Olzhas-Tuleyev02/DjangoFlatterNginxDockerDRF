from django.views.generic import ListView, DetailView
from .models import Service, Category
from rest_framework import permissions

# Custom Permissions
class IsProviderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow providers to edit their own services.
    Customers can only view.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'PROVIDER'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.provider == request.user


# Web views (These are not required by the prompt, but I will update them for consistency)
class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(category=self.object.category).exclude(id=self.object.id).order_by('?')[:4]
        return context

# API views
from django.core.cache import cache
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import CategorySerializer, ServiceSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsProviderOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'city']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'rating']

    def get_queryset(self):
        # Allow filtering by provider for the /api/v1/providers/ endpoint
        provider_id = self.request.query_params.get('provider_id')
        if provider_id:
            return Service.objects.filter(provider_id=provider_id, is_active=True)
        
        # Return all active services for the general list
        return Service.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)
