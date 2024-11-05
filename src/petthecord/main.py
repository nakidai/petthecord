from argparse import ArgumentParser
from os import getenv
from sys import argv, stderr

from .runner import PetTheCord


def main() -> None:
    parser = ArgumentParser(
        prog="petthecord",
        description="Web API for petting any user you want"
    )
    parser.add_argument(
        "-p", "--port",
        default=8000,
        type=int,
        metavar="PORT",
        help="Bind port"
    )
    parser.add_argument(
        "-i", "--host",
        default="127.0.0.1",
        metavar="HOST",
        help="Bind IP"
    )
    parser.add_argument(
        "-o", "--origin",
        default="https://ptc.pwn3t.ru",
        metavar="PATH",
        help="Root of the bot"
    )
    parser.add_argument(
        "-d", "--cache-dir",
        default="/var/cache/petthecord",
        metavar="PATH",
        help="Directory for cache storing"
    )
    parser.add_argument(
        "-n", "--no-cache",
        action="store_true",
        default=False,
        help="Turn off the cache"
    )
    parser.add_argument(
        "-l", "--cache-lifetime",
        default=86400,
        type=int,
        metavar="TIME",
        help="Lifetime of cached avatar in seconds"
    )
    parser.add_argument(
        "-s", "--cache-gc-delay",
        default=14400,
        type=int,
        metavar="TIME",
        help="Delay between cache's garbage collector runs in seconds"
    )
    args = parser.parse_args()

    bot = PetTheCord(
        args.host,
        args.port,
        args.origin,
        not args.no_cache,
        args.cache_dir,
        args.cache_lifetime,
        args.cache_gc_delay
    )
    if (token := getenv("PETTHECORD_TOKEN")) is not None:
        bot.run(token, root_logger=True)
    elif (token_path := getenv("PETTHECORD_TOKEN_FILE")) is not None:
        with open(token_path) as f:
            token = f.read()
        bot.run(token, root_logger=True)
    else:
        print(f"{argv[0]}: Neither PETTHECORD_TOKEN nor PETTHECORD_TOKEN_FILE are set", file=stderr)
