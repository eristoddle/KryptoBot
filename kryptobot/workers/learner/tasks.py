from .celery import app
from ..config import core
import importlib

def title_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def dynamic_import(abs_module_path, class_name):
    module_object = importlib.import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class
