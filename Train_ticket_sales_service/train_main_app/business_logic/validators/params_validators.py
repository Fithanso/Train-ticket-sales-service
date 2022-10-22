from datetime import datetime

from ..abstract import ParamValidator
from ...functions import all_keys_exist


class ExistenceValidator(ParamValidator):

    @staticmethod
    def validate(model, search_data):
        result = model.objects.filter(**search_data)

        return bool(result)


class KeysExistValidator(ParamValidator):

    @staticmethod
    def validate(data_dict, needed_keys):
        return all_keys_exist(data_dict, needed_keys)


class DateFormatValidator(ParamValidator):

    @staticmethod
    def validate(date_str: str, format_str: str) -> bool:
        try:
            datetime.strptime(date_str, format_str)
        except:
            return False

        return True
