from typing import Union

from redis import Redis
import ujson


class BaseStorage:
    """
     An abstract storage class.
     To create your own storage (using, for example, a DB or a file),
      you need to implement all the methods
    """

    def get_user_data(self, user_id: Union[str, int]) -> dict:
        pass

    def set_user_data(self, user_id: Union[str, int], data: dict):
        pass

    def update_user_data(self, user_id: Union[str, int], key: str, value: str):
        pass

    def get_user_state(self, user_id: Union[str, int]) -> str:
        pass

    def set_user_state(self, user_id: Union[str, int], state: str):
        pass


class RedisStorage(Redis, BaseStorage):
    """ Storage based on Redis """

    def __init__(self, host="localhost", port=6379, db=0,
                 username=None, password=None):
        super().__init__(host=host, port=port, db=db,
                         username=username, password=password)

    # DATA

    def get_user_data(self, user_id: Union[str, int]) -> dict:
        if data := self.get(f'{user_id}_data'):
            return ujson.loads(data)
        return {}

    def set_user_data(self, user_id: Union[str, int], data: dict):
        self.set(f'{user_id}_data', ujson.dumps(data))

    def update_user_data(self, user_id: Union[str, int], key: str, value: str):
        data = self.get_user_data(user_id)
        data[key] = value
        self.set_user_data(user_id, data)

    # STATE

    def get_user_state(self, user_id: Union[str, int]) -> str:
        if res := self.get(f'{user_id}_state'):
            return res.decode('utf-8')
        return ''

    def set_user_state(self, user_id: Union[str, int], state):
        self.set(f'{user_id}_state', state)
