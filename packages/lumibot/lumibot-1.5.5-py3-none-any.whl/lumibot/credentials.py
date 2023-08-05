class InteractiveBrokersConfig:
    SOCKET_PORT = 7497  #7497  # 4002
    CLIENT_ID = 888
    IP = "127.0.0.1"

class AlpacaConfig:
    API_KEY = "PKNKI8VFH6PUC3G1JYUD"
    API_SECRET = "giRxjb9Gnriolo0xNbNruqMZr81Y1T68K5f3sREs"

    """ If no endpoint is specified, the following paper trading
    endpoint will be used by default"""
    ENDPOINT = "https://paper-api.alpaca.markets"

    VERSION = "v2"  # By default v2
    USE_POLYGON = False  # By dfault set to False


class AlphaVantageConfig:
    API_KEY = "JFA1T96521EMIZAV"
