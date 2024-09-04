from argparse import ArgumentParser
from os import getenv
from sys import argv, stderr

from .bot import Bot


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
    args = parser.parse_args()

    bot = Bot()
    if (token := getenv("PETTHECORD_TOKEN")) is not None:
        bot.run(token)
    elif (token_path := getenv("PETTHECORD_TOKEN_FILE")) is not None:
        with open(token_path) as f:
            token = f.read()
        bot.run(token, args.host, args.port)
    else:
        print(f"{argv[0]}: Neither PETTHECORD_TOKEN nor PETTHECORD_TOKEN_FILE are set", file=stderr)
