from collections import Counter
from aiogram.filters import BaseFilter
from aiogram.types import Message

class SerialFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text and message.text.startswith('00'):
            filter_result = {
                "correct_serials": [],
                "incorrect_serials": []
            }
            serials = message.text.splitlines()
            for serial in serials:
                if serial.startswith('00-') and serial.removeprefix('00-').isdigit():
                    filter_result["correct_serials"].append(serial)
                else:
                    filter_result["incorrect_serials"].append(serial)
            filter_result['correct_serials'] = Counter(filter_result['correct_serials'])
            return filter_result
        return False
