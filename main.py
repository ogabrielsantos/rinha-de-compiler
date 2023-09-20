import json
from os.path import isfile

from nodes import File
from utils import to_ast_node

DEFAULT_INPUT_FILE = "/var/rinha/source.rinha.json"


if __name__ == "__main__":
    input_file = DEFAULT_INPUT_FILE if isfile(DEFAULT_INPUT_FILE) else "./source.rinha.json"

    with open(input_file) as file:
        data = json.load(file, object_hook=to_ast_node)

        file = File(**data)
        file.expression.execute()
