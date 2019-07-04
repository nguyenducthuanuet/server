import logging
from .base import fake
from boilerplate.helpers.faker.provider import Provider
from .user_provider import UserProvider
_logger = logging.getLogger(__name__)
__author__ = 'Kien'

fake.add_provider(Provider)
fake.add_provider(UserProvider)
