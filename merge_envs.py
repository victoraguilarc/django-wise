# -*- coding: utf-8 -*-

import os
from typing import Sequence

ROOT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PRODUCTION_DOTENVS_DIR_PATH = os.path.join(ROOT_DIR_PATH, '.envs', 'stage')
production_env_file_paths = [
    os.path.join(PRODUCTION_DOTENVS_DIR_PATH, 'django'),
    os.path.join(PRODUCTION_DOTENVS_DIR_PATH, 'postgres'),
]
DOTENV_FILE_PATH = os.path.join(ROOT_DIR_PATH, '.env')


def merge(output_file_path: str, merged_file_paths: Sequence[str], append_linesep: bool = True) -> None:
    """It joins the environment files in .env file."""
    with open(output_file_path, 'w') as output_file:
        for merged_file_path in merged_file_paths:
            with open(merged_file_path, 'r') as merged_file:
                merged_file_content = merged_file.read()
                output_file.write(merged_file_content)
                if append_linesep:
                    output_file.write(os.linesep)


def main():  # noqa: D103
    merge(DOTENV_FILE_PATH, production_env_file_paths)


if __name__ == '__main__':
    main()
