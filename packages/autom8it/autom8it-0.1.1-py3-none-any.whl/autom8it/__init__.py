import abc
import yaml
from time import sleep
from quickbe import Log
from cerberus import Validator
from importlib import import_module


class AutomationTask:

    def __init__(self, task_data: dict, timeout: int = 900, check_done_interval: int = 5):
        validator = Validator(self.validation_schema)
        validator.allow_unknown = True
        if validator.validate(task_data):
            self._task_data = task_data
            self._check_done_interval = check_done_interval
            self._timeout = timeout
        else:
            for error in validator.errors:
                Log.error(error)
            raise ValueError(f'There are {len(validator.errors)} in task data.')

    @property
    @abc.abstractmethod
    def task_type(self) -> str:
        pass

    """
    https://docs.python-cerberus.org/en/stable/validation-rules.html#
    Validation schema example
        {
            'name': {
                'required': True, 
                'type': 'string'
            }, 
            'age': {
                'type': 'integer'
                'min': 18,
                'max': 120
            }
            'gender': {
                'type': 'string',
                'allowed': ['male', 'female', 'unknown']
        }
    """
    @property
    @abc.abstractmethod
    def validation_schema(self) -> dict:
        pass

    @abc.abstractmethod
    def do(self):
        pass

    @abc.abstractmethod
    def is_done(self) -> bool:
        pass

    def get_task_attribute(self, key: str, default=None):
        return self._task_data.get(key, default)

    def run(self):
        sw_id = Log.start_stopwatch(msg=self.task_type)
        Log.debug(f"Task returned: {self.do()}")
        while not self.is_done() and self._timeout > Log.stopwatch_seconds(stopwatch_id=sw_id, print_it=False):
            sleep(self._check_done_interval)


def run_yaml(file_path: str):
    with open(file_path, "r") as f:
        run_def = yaml.safe_load(f)
    run(run_def=run_def)


def run_yaml(file_path: str):
    with open(file_path, "r") as f:
        run_def = yaml.safe_load(f)
    run(run_def=run_def)


TASK_CLASS_KEY = 'class'
TASK_PARAMETERS_KEY = 'parameters'


def run(run_def: dict):
    main_sw_id = Log.start_stopwatch(msg='Run')
    for task_name, task_def in run_def.items():
        if TASK_CLASS_KEY in task_def:
            task = get_task_instance(class_name=task_def[TASK_CLASS_KEY], parameters=task_def[TASK_PARAMETERS_KEY])
            first_row = f'*   Task {task_name} ({task.task_type}) is starting *'
            Log.info(msg="*" * len(first_row))
            Log.info(msg=first_row)
            Log.info(msg="*" * len(first_row))
            Log.info(f'Task parameters: {task_def[TASK_PARAMETERS_KEY]}')
            task_sw_id = Log.start_stopwatch(msg=first_row)
            task.run()
            Log.info(
                f'*** Task {task.task_type} finished after '
                f'{Log.stopwatch_seconds(stopwatch_id=task_sw_id, print_it=False)} seconds ***'
            )
        else:
            raise SyntaxError(f'Missing {TASK_CLASS_KEY} definition.')
    Log.info(f'Process finished after {Log.stopwatch_seconds(stopwatch_id=main_sw_id, print_it=False)} seconds.')


def get_task_instance(class_name: str, parameters: dict) -> AutomationTask:
    task_cls = get_class_by_name(class_name=class_name, requested_type=AutomationTask)
    return task_cls(parameters)


def get_class_by_name(class_name: str, requested_type: object = None):

    try:
        module_path, c_name = class_name.rsplit('.', 1)
        module = import_module(module_path)
        result = getattr(module, c_name)
        if requested_type is not None and not issubclass(result, requested_type):
            raise ValueError(f'Class {result} does not match type {requested_type}.')
        return result
    except (ImportError, AttributeError) as e:
        raise ImportError(class_name)
