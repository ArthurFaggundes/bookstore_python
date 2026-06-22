import pytest

from ..models import Product


@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        title="Titulo teste",
        description="Descrição de teste",
        price=999
    )

    assert product.title == "Titulo teste"
    assert product.description == "Descrição de teste"
    assert product.price == 999
    assert product.id is not None