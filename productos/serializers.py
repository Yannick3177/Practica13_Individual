# productos/serializers.py
from rest_framework import serializers
from .models import Categoria, Marca, Producto


# ---------------------------------------------------------
# 1. Serializer para Categorías
# ---------------------------------------------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activa']


# ---------------------------------------------------------
# 2. Serializer para Marcas (¡ESTA ERA LA QUE FALTABA!)
# ---------------------------------------------------------
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'pais_origen']


# ---------------------------------------------------------
# 3. Serializer para Productos
# ---------------------------------------------------------
class ProductoSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar nombres en lugar de IDs
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'sku', 'nombre', 'slug', 'descripcion',
            'categoria', 'categoria_nombre',
            'marca', 'marca_nombre',
            'precio', 'precio_oferta',
            'stock', 'estado', 'destacado', 'creado'
        ]
        read_only_fields = ['id', 'slug', 'creado']

    # Validación anidada (Requisito de la guía)
    def validate(self, data):
        """Valida que el precio de oferta sea menor al precio regular."""
        precio = data.get('precio')
        precio_oferta = data.get('precio_oferta')

        if precio_oferta and precio:
            if precio_oferta >= precio:
                raise serializers.ValidationError({
                    'precio_oferta': 'El precio de oferta debe ser menor al precio regular.'
                })
        return data