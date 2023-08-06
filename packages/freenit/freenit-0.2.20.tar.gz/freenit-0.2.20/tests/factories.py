import factory
from passlib.context import CryptContext

from freenit.config import getConfig

config = getConfig()
auth = config.get_user()
UserModel = auth.UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(factory.Factory):
    class Meta:
        model = UserModel

    id = factory.Faker("uuid4")
    email = factory.Faker("email")
    hashed_password = pwd_context.hash("Sekrit")
    is_verified = True
    is_superuser = False
    is_active = True


class SuperUser(User):
    is_superuser = True


class UnverfiedUser(User):
    is_verified = False


class InactiveUser(User):
    is_active = True
