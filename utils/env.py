import environ
from dotenv import load_dotenv

load_dotenv()
env = environ.Env()
environ.Env.read_env()

DATABASE_CONFIG = {
    **env.db('DATABASE_CREDENTIALS'),
    'CONN_MAX_AGE': env.int('CONN_MAX_AGE')
}
ROOT_URL=env('ROOT_URL')
