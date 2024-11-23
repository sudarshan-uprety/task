import environ
from dotenv import load_dotenv

load_dotenv()
env = environ.Env()
environ.Env.read_env()

# database .env load
DATABASE_CONFIG = {
    **env.db('DATABASE_CREDENTIALS'),
    'CONN_MAX_AGE': env.int('CONN_MAX_AGE')
}
ROOT_URL = env('ROOT_URL')

# mail credential .env load'
# Email settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# debug mode
DEBUG = env.bool('DEBUG')