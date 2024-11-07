from typing import Final


class Defaults:
    class Network:
        PORT: Final = 8000
        HOST: Final = "127.0.0.1"
        ORIGIN: Final = "https://ptc.pwn3t.ru"


    class Cache:
        CACHING: Final = True
        PATH: Final = "/var/cache/petthecord"
        LIFETIME: Final = 86400
        GC_DELAY: Final = 14400


    SHARDS_COUNT: Final = 1
