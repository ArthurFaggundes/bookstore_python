import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient() # pode fazer get, post, pull, etc.

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user) # gera um token de autenticação
        token.save() # envia: Authorization: Token c5ab741b29dfae34c81...

        self.product = ProductFactory(
            title="pro controller",
            price=200.00,
        )

    def test_get_all_product(self): # verifica se api consegue lisatr os produtos
        token = Token.objects.get(user__username=self.user.username) # acessa campo relacionado
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key) # add: Authorization: Token abc123
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)

        self.assertEqual(product_data["results"][0]["title"], self.product.title)
        self.assertEqual(product_data["results"][0]["price"], self.product.price)
        self.assertEqual(product_data["results"][0]["active"], self.product.active)

    def test_create_product(self):
        token = Token.objects.get(user__username=self.user.username) # precisa para ñ dar erro 401
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        category = CategoryFactory()
        data_prod = json.dumps(
            {"title": "notebook", "price": 800.00, "categories_id": [category.id]} # gera ID
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data_prod,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="notebook") # pega o prod. que tem o título tal

        self.assertEqual(created_product.title, "notebook")
        self.assertEqual(created_product.price, 800.00)
