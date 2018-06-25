from ..core import Core
import json
import os


json_path = os.path.realpath(__file__).replace('.py', '.json')

# TODO: Some way to do this at launch
with open(json_path, encoding='utf-8') as data_file:
    config = json.loads(data_file.read())

core = Core(config=config)
