import os

# Set the default to 'dev' in case the environment variable is not set
ENVIRONMENT = os.getenv('DJANGO_ENV', 'dev')
from .settings_dev import *
# if ENVIRONMENT == 'prod':
#     from .settings_prod import *
# else:
#     from .settings_dev import *