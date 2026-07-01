import factory

from product.models import Category, Product

# mesmo que fazer Category.objects.create(...) * 50
class CategoryFactory(factory.django.DjangoModelFactory): # para criar uma categoria com informações para teste
    title = factory.Faker("pystr")
    slug = factory.Faker("pystr")
    description = factory.Faker("pystr")
    active = factory.Iterator([True, False]) # alterna entre T e F

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory): # para criar os produtos
    price = factory.Faker("pyint") # sera INTs
    category = factory.LazyAttribute(CategoryFactory) # só cria quando necessario, invoca a classe de cima
    # mais comum usar >> category = factory.SubFactory(CategoryFactory)
    description = factory.Faker("pystr")
    title = factory.Faker("pystr")

    @factory.post_generation # roda depois do produto criado
    def category(self, create, extracted, **kwargs):
        if not create: # se há objeto
            return

        if extracted: # transforma em instancia os valores passados
            for category in extracted:
                self.category.add(category) # produto.category.add(cat1) ...

    class Meta:
        model = Product