import inspect
import logging

from spotlight.validator import Validator

__all__ = ['BaseInput']

LOGGER = 'api'


def validate(data, rules, raise_if_error=True):
    """Validates data againt spotlight rules validator
    :returns: errors if any
    """
    return Validator().validate(data, rules)


class BaseInput(object):
    """This abstract class is the parent of the inputs's classes"""

    def __init__(self, input_, *args, **kwargs):
        self._input = input_
        self._raise = False
        self.validated = False

    def validate(self, raise_if_error=False):
        errors = self._validate()
        if errors and raise_if_error:
            raise Exception(errors)

        self.validated = True

        return errors

    def _validate(self):
        """This method uses spotlight validator to validate the input against the self RULES
        :returns: An empty dict or a dict with errors
        """
        rules = {}
        errors = {}
        if self.RULES:
            dependencies = {k: v
                            for k, v in self.RULES.items()
                            if (inspect.isclass(v) and issubclass(v, BaseInput))
                                or (isinstance(v, list) and v)}
            rules = {k: v
                     for k, v in self.RULES.items()
                     if not inspect.isclass(v)
                        and not isinstance(v, list)}
            errors = validate(self._input, rules)
            for field_name, input_class in dependencies.items():
                #can be a list or another input class
                if isinstance(input_class, list):
                    #TODO: allow multiple types
                    input_class = input_class[0]
                    new_list = []
                    for value in self._input[field_name]:
                        input_instance = input_class(value)
                        new_list.append(input_instance)
                        errors = {**errors, **input_instance.validate()}
                    self._input[field_name] = new_list
                else:
                    input_instance = input_class(self._input[field_name])
                    self._input[field_name] = input_instance
                    errors = {**errors, **input_instance.validate()}
        else:
            logging.getLogger(LOGGER).error('No rules defined for input {}'.format(__name__))

        return errors

    def keys(self):
        return list(self._input.keys())

    def __setitem__(self, item, value):
        self._input[item] = value

    def __getitem__(self, item):
        return self._input[item]

    def __delitem__(self, item):
        del self._input[item]
