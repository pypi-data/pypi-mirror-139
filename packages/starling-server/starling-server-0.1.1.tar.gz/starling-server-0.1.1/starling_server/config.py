from typing import Tuple

import yaml

from config_path import ConfigPath

CONFIG = ConfigPath('starling_server', 'rjlyon.com', ".json")

CONFIG_FOLDER = CONFIG.saveFolderPath()
TOKENS_FOLDER = CONFIG.saveFolderPath() / "tokens"
TOKENS_FILENAME = "config.yaml"
TOKENS_FILEPATH = CONFIG_FOLDER / TOKENS_FILENAME


def get_tokens() -> dict:
    try:
        with open(TOKENS_FILEPATH) as file:
            return yaml.safe_load(file)
    except:
        raise Exception(f"Can't find starling config file '{TOKENS_FILEPATH}'")


def get_token_account__from_name(name: str) -> Tuple[str, str]:
    tokens = get_tokens()
    if name.lower() in tokens:
        token = tokens[name.lower()]["token"]
        account_id = tokens[name.lower()]["account_id"]
        return token, account_id

    raise KeyError(f"No token for '{name}'")
