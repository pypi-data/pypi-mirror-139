from django.contrib.auth import get_user_model
import factory
import factory.random
from factory.faker import faker


factory.random.reseed_random(42)

User = get_user_model()
fake = faker.Faker()  # This is to use faker without the factory_boy wrapper


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(lambda obj: f"{obj.first_name}_{obj.last_name}")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name}.{obj.last_name}@example.com".lower()
    )
    password = "goodpass"
