from aiogram.filters import BaseFilter
from aiogram.types import Message

class NameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            #split name by spaces
            name = message.text.split(' ')
            #create result for handler
            result = {'name': []}
            for word in name:
                if word.isalpha():
                    result['name'].append(word)
                else:
                    await message.answer("ФИО не может содержать цифры")
                    return False
            return result
                
        await message.answer('Отправьте ФИО')
        return False
        
