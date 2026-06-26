import pytest

from product.factories import ProductFactory
from product.factories import CategoryFactory

@pytest.fixture
def product_created():
    return ProductFactory(price=99)

@pytest.mark.django_db
def test_product(product_created):
    assert product_created.price == 99
    assert product_created.categories != None

# =============================================================== #

@pytest.fixture
def category_created():
    return CategoryFactory(title='eletronico', description='descricao_teste', active=False)

@pytest.mark.django_db
def test_category(category_created):
    assert category_created.title == 'eletronico'
    assert len(category_created.description) >= 10
    assert category_created.active == False
