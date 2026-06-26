# order\serializers\order_serializer.py

from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True) # Esse campo será enviado na resposta, mas o usuário não pode enviá-lo na requisição. E com vários objetos.

    products_id = serializers.PrimaryKeyRelatedField( 
        queryset=Product.objects.all(), write_only=True, many=True
    ) # espera uma requisição assim: {"user": 1,"products_id": [1, 3, 5]}

    total = serializers.SerializerMethodField() # campo calculado -> retorna soma

    def get_total(self, instance):
        total = sum(product.price for product in instance.product.all()) # instance é o ped. atual
        return total # soma todos os preços dos produtos

    class Meta: # configuração
        model = Order
        fields = ["product", "total", "user", "products_id" ] # campos expostos (de prodcura) da api
        extra_kwargs = {"product": {"required": False}} # torna o campo opcional para evitar erros

    def create(self, validated_data): # [validated_data] tem os dados já validados dict{list[]}
        product_data = validated_data.pop("products_id") # remove os produtos agora só list[]
        user_data = validated_data.pop("user") # remove o usuário e atribui variavel

        order = Order.objects.create(user=user_data) # pega a var. e salva em order
        for product in product_data: # se tiver itens ele adiciona os produtos ao pedido (N:N)
            order.product.add(product)

        return order