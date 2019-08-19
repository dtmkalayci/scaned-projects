# Flask settings
FLASK_SERVER_NAME = 'localhost:5004'
#FLASK_SERVER_NAME = '172.28.9.75:5004'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
DEBUG = False
MONGODB_DB = "iky-ai2"
MONGODB_HOST = "172.28.9.75"
MONGODB_PORT = 27017
MONGODB_USERNAME = ""
MONGODB_USERNAME = ""
MONGODB_URI = "mongodb://172.28.9.75:27017/iky-ai2"