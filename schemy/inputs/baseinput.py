import inspect
from spotlight.validator import Validator

__all__ = ['BaseInput']


class BaseInput(object):
    """This abstract class is the parent of the inputs's classes"""

    def __init__(self, input_, *args, **kwargs):
        self._input = input_
        self._raise = False

    def validate(self, raise_if_error=False):
        errors = self._validate()
        if errors and raise_if_error:
            raise Exception(errors)
        return errors

    def _validate(self):
        """This method uses spotlight validator to validate the input against the self RULES
        :returns: An empty dict or a dict with errors
        """
        rules = {}
        errors = {}
        if self.RULES:
            dependencies = {k: v for k, v in self.RULES.items() if inspect.isclass(v) and issubclass(v, BaseInput)}
            rules = {k: v for k, v in self.RULES.items() if not inspect.isclass(v)}
            errors = Validator().validate(self._input, rules)
            for field_name, input_class in dependencies.items():
                input_instance = input_class(self._input[field_name])
                errors = {**errors, **input_instance.validate()}
                self._input[field_name] = input_instance
        else:
            # log this!
            print('No rules defined for input {}'.format(__name__))

        return errors

    def keys(self):
        return list(self._input.keys())

    def __setitem__(self, item, value):
        self._input[item] = value

    def __getitem__(self, item):
        return self._input[item]
