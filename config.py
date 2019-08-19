class Config(object):
    DEBUG = False
    MONGODB_DB = "iky-ai2"
    MONGODB_HOST = "172.28.9.75"
    MONGODB_PORT = 27017
    MONGODB_USERNAME = "None"
    MONGODB_PASSWORD = "None"



class NonDebug(Config):
    DEBUG = False

class Development(Config):
    DEBUG = True


class Production(Config):
    # MongoDB Database Details
    MONGODB_DB = "daap-ai-analytics"
    MONGODB_HOST = "mongodb"
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ""
    MONGODB_USERNAME = ""

    # Web Server details
    WEB_SERVER_PORT = 8001