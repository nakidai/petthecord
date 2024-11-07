from argparse import ArgumentParser
from os import getenv
from sys import argv, stderr

from .defaults import Defaults
from .petter import CacheEnvironmentFail, CachedPetter, Petter
from .runner import PetTheCord


def main() -> None:
    parser = ArgumentParser(
        prog="petthecord",
        description="Web API for petting any user you want"
    )
    parser.add_argument(
        "-p", "--port",
        default=Defaults.Network.PORT,
        type=int,
        metavar="PORT",
        help="Bind port"
    )
    parser.add_argument(
        "-i", "--host",
        default=Defaults.Network.HOST,
        metavar="HOST",
        help="Bind IP"
    )
    parser.add_argument(
        "-o", "--origin",
        default=Defaults.Network.ORIGIN,
        metavar="PATH",
        help="Root of the bot"
    )
    parser.add_argument(
        "-d", "--cache-dir",
        default=Defaults.Cache.PATH,
        metavar="PATH",
        help="Directory for cache storing"
    )
    parser.add_argument(
        "-n", "--no-cache",
        action="store_true",
        default=not Defaults.Cache.CACHING,
        help="Turn off the cache"
    )
    parser.add_argument(
        "-l", "--cache-lifetime",
        default=Defaults.Cache.LIFETIME,
        type=int,
        metavar="TIME",
        help="Lifetime of cached avatar in seconds"
    )
    parser.add_argument(
        "-s", "--cache-gc-delay",
        default=Defaults.Cache.GC_DELAY,
        type=int,
        metavar="TIME",
        help="Delay between cache's garbage collector runs in seconds"
    )
    parser.add_argument(
        "-c", "--shards",
        default=Defaults.SHARDS_COUNT,
        type=int,
        metavar="COUNT",
        help="Amount of shards to create"
    )
    args = parser.parse_args()

    if args.no_cache:
        petter = Petter()
    else:
        try:
            petter = CachedPetter(
                args.cache_dir,
                args.cache_lifetime,
                args.cache_gc_delay,
            )
        except CacheEnvironmentFail:
            petter = Petter()

    bot = PetTheCord(
        args.host,
        args.port,
        args.origin,
        petter,
        args.shards,
    )
    if (token := getenv("PETTHECORD_TOKEN")) is not None:
        bot.run(token, root_logger=True)
    elif (token_path := getenv("PETTHECORD_TOKEN_FILE")) is not None:
        with open(token_path) as f:
            token = f.read()
        bot.run(token, root_logger=True)
    else:
        print(f"{argv[0]}: Neither PETTHECORD_TOKEN nor PETTHECORD_TOKEN_FILE are set", file=stderr)
