import pytest

from order.factories import UserFactory
from order.factories import OrderFactory

@pytest.fixture
def user_created():
    return UserFactory(email='joaosilva@teste.com')

@pytest.mark.django_db
def test_user(user_created):
    assert user_created.email == 'joaosilva@teste.com'
    assert user_created.username != None

# =============================================================== #

@pytest.fixture
def order_created():
    return OrderFactory()

@pytest.mark.django_db
def test_order(order_created):
    assert order_created.user != None
    assert order_created.product != None
