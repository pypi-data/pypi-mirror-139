# bot-storage
##### _Storage - an object that allows you to save the states and data of users._
##### _The storage.py file describes the abstract class BaseStorage, inheriting from which, you can implement your own storage (eg DBStorage or JSONStorage)._
##### _Such storages, however, will obviously not be more efficient than the already implemented RedisStorage._


## Installation:
```sh
pip install bot-storage
```

## Setting up
`YourProject/tbot/storage.py`
```python
from os import getenv

from bot_storage.storage import RedisStorage


storage = RedisStorage(
    host=getenv('REDIS_HOST', 'localhost'),
    username=getenv('REDIS_USER', None),
    password=getenv('REDIS_PASSWORD', None)
)

```

`YourProject/settings.py`
```python
from tbot.storage import storage


# Your storage for user states & data
BOT_STORAGE = storage
```

## Start Redis
```sh
redis-server
```

## Usage
### For example YourProject/tbot/handlers.py

```python
from telebot import types
from telebot.apihelper import ApiTelegramException
from tbot_base.bot import tbot

from .storage import storage as st


@tbot.message_handler(
    func=lambda msg: st.get_user_state(msg.from_user.id) == 'some_state#'
)
def send_faq_search(msg: types.Message):
    tbot.send_message(chat_id=msg.from_user.id, text='Hello!')
```
