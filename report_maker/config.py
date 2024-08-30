from report_maker.singleton import Singleton


class Config(Singleton):
    CERT_PROVIDER_HOST: str
    CERT_PROVIDER_PORT: str | int
    VM_USER: str = "admin"


config_obj = Config()
