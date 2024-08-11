import argparse
import os

from dotenv import load_dotenv
class Config:
    def __init__(self, env: str):
        self.env = env
        self.SERVER_URL = ""
        self.BOT_TOKEN = ""
        self.load_environment()
        self.set_parameters()

    def load_environment(self):
        filepath = '.env_prod' if self.env == 'prod' else '.env_dev'
        print(filepath)
        if os.path.exists(filepath):
            if self.env == 'prod':
                load_dotenv('.env_prod')
                print("Loaded environment variables from .env_prod")

            else:
                load_dotenv('.env_dev')
                print("Loaded environment variables from .env_dev")
        else:
            raise FileNotFoundError(f"Environment file '{filepath}' not found.")

    def set_parameters(self):
        if self.env == 'prod':
            self.SERVER_URL = os.getenv("SERVER_URL_PROD")
            self.BOT_TOKEN = os.getenv("BOT_TOKEN_PROD")
        else:
            self.SERVER_URL = os.getenv("SERVER_URL_DEV")
            self.BOT_TOKEN = os.getenv("BOT_TOKEN_DEV")

        if self.SERVER_URL is None or self.BOT_TOKEN is None:
            raise EnvironmentError(f"Environment variable  not found")


try:
    parser = argparse.ArgumentParser(description="Configuration")
    parser.add_argument('--env', default='dev', choices=['dev', 'prod'], help="Specify the environment (dev or prod)")
    args = parser.parse_args()
    config = Config(args.env)

except FileNotFoundError as e:
    print(e)
    exit(1)

except EnvironmentError as e:
    print(e)
    exit(1)
