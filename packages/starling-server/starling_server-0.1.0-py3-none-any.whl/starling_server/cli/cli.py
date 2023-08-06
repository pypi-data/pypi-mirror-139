# cli.py - Command Line Interface
# Richard Lyon, 20 Feb 2022

import os
import shutil
from datetime import datetime
import asyncio


import yaml
from cleo import Command, Application

from starling_server.config import CONFIG, CONFIG_FOLDER, TOKENS_FOLDER, TOKENS_FILEPATH
from starling_server.starling.api import api_get_accounts


class InitCommand(Command):
    """
    Initialise Starling Server configuration file from access tokens

    init
    """
    def handle(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.handle_async())

    async def handle_async(self):
        if not self.confirm("WARNING: This will reset configuration data. Continue?", False):
            return

        os.makedirs(CONFIG.saveFolderPath(), exist_ok=True)

        # get tokens from files
        if not TOKENS_FOLDER.is_dir():
            os.mkdir(TOKENS_FOLDER)
            self.line(f"<error>no tokens folder</error>")
            self.line(f"<error>created tokens folder at {TOKENS_FOLDER}</error>")
            self.line("<error>create a file for each token in tokens folder and rerun 'init'</error>")
            self.line("Done")
            return

        tokens = []
        tokens_files = os.listdir(TOKENS_FOLDER)
        for token_file in tokens_files:
            file_path = TOKENS_FOLDER / token_file
            file = open(file_path, "r")
            tokens.append(file.read().strip())
            file.close()

        # build a dictionary of Starling account name and id for each token
        token_dict = {}
        for token in tokens:
            account_info = await api_get_accounts(token)
            for account in account_info.accounts:
                token_dict[account.name.lower()] = {"account_id": account.accountUid, "token": token}

        # save to yaml file, backing up any previous version
        if TOKENS_FILEPATH.is_file():
            backup_name = TOKENS_FILEPATH.stem + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".yaml"
            backup_filepath = CONFIG_FOLDER / backup_name
            shutil.copy(TOKENS_FILEPATH, backup_filepath)
            self.line(f"<info>Backed up tokens file to {backup_filepath}</info>")

        with open(TOKENS_FILEPATH, 'w') as file:
            yaml.dump(token_dict, file)
            self.line(f"<info>Created tokens file at {TOKENS_FILEPATH}</info>")

        self.line("Done.")


app = Application()
app.add(InitCommand())


def cli():
    app.run()


if __name__ == "__main__":
    cli()
