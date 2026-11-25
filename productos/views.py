from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from .models import Categoria, Marca, Producto
from .serializers import CategoriaSerializer, MarcaSerializer, ProductoSerializer


def api_dashboard(request):
    """Vista del Dashboard principal (se muestra en la raíz /)"""
    context = {
        'productos_count': Producto.objects.count(),
        'categorias_count': Categoria.objects.count(),
        'marcas_count': Marca.objects.count(),
    }
    return render(request, 'productos/dashboard.html', context)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'categoria']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio', 'creado']

    @action(detail=False, methods=['get'], url_path='destacados')
    def destacados(self, request):
        productos = Producto.objects.filter(destacado=True, estado='activo')
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)