import os

# assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'
basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.split(basedir)[0]


class Config:
    PORT = 8080
    SECRET_KEY = os.environ.get('SECRET', 'secret')
    SQL_URI = 'sqlite:///app.db'
    BASEDIR = basedir
    LOG_FOLDER = os.path.join(BASEDIR, 'logs')
    LOG_FILENAME = 'app.log'
    LOG_FILE_PATH = os.path.join(LOG_FOLDER, LOG_FILENAME)
    LOGGER_NAME = 'logger'
    TIME_FORMAT = r'%Y-%m-%d %H:%M:%S'


class TestConfig(Config):
    SQL_URI = 'sqlite:///test.db'


# env = os.environ['APP_ENV'].upper()
# if env == 'TEST':
#     app_config = TestConfig
# elif env == 'PRD':
#     app_config = DockerConfig
# else:
#     app_config = Config
app_config = Config
#
# print(app_config)
#