import json # usado com dumps, load, etc.

from django.urls import reverse # para procurar url pelo nome: "/api/v1/orders/" -> reverse("orders")
from rest_framework import status # para cod. https -> 404, 200, etc. == assert response.status_code == 200
from rest_framework.test import APIClient, APITestCase # faz requisições, classe base para testes de API.

#* arquivos do projeto ::
from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory
# from product.models import Product


class TestOrderViewSet(APITestCase): # especifica para APIs REST (cria bancos temp., limp dados, fornece cli. http)

    client = APIClient() # simula um cliente (nav., app) ex.: response = self.client.post(...)

    def setUp(self): # executa antes de cada teste
        self.category = CategoryFactory(title="technology") # cria categoria especifica
        self.product = ProductFactory( # cria produto especifico
            title="mouse", price=100, category=[self.category], description='...' # category=[self.category] -> pega o argumento de antes, nesse caso categoria: technology 
        )
        self.order = OrderFactory(product=[self.product]) # (product=[self.product], pega arg. de antes

    def test_order(self):
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})) # gera: /api/v1/order/

        self.assertEqual(response.status_code, status.HTTP_200_OK) # resp = 200
        order_data = json.loads(response.content) # pega o conteúdo e converte em dict #* também pode ser: order_data = response.data

        self.assertEqual( # verifica se o 1º produto do 1º pedido tem o título == mouse
            order_data[0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data[0]["product"][0]["price"], # -> onde procura
            self.product.price # -> o que procura
        )
        self.assertEqual(
            order_data[0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data[0]["product"][0]["description"], self.product.description
        )
        self.assertEqual(
            order_data[0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self): # verifica se api cria um pedido
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": user.id}) # gera: { "products_id": [1], "user": 5 }

        response = self.client.post( # mesmo que: POST /api/v1/order/ { "products_id": [1], "user": 5 }
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # ve se foi criado

        created_order = Order.objects.get(user=user)