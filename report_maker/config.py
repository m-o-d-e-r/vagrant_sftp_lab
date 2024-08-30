from report_maker.singleton import Singleton


class Config(Singleton):
    CERT_PROVIDER_HOST: str
    CERT_PROVIDER_PORT: str | int


config_obj = Config()
