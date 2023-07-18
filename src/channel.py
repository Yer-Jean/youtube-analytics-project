import json

from src.api_mixin import APIMixin


class Channel(APIMixin):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id: str = channel_id
        # Получаем данные канала для дальнейшей инициализации класса Channel
        # channel_info можно убрать из self, но он используется в print_info()
        self.channel_info = \
            self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # Инициализируем атрибуты класса Channel полученными данными
        self.id: str = self.channel_info['items'][0]['id']
        self.title: str = self.channel_info['items'][0]['snippet']['title']
        self.description: str = self.channel_info['items'][0]['snippet']['description']
        self.url: str = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count: int = int(self.channel_info['items'][0]['statistics']['subscriberCount'])
        self.video_count: int = int(self.channel_info['items'][0]['statistics']['videoCount'])
        self.view_count: int = int(self.channel_info['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_id: str):
        print(f'\nНельзя изменить значение channel_id на "{new_id}"\n')

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel_info)

    def to_json(self, file_path: str) -> None:
        """Записывает в json-файл значения атрибутов экземпляра Channel"""
        data = self.__dict__                # Берем все атрибуты в формате словаря
        del data['_Channel__channel_id']    # Удаляем ненужный словарь
        del data['channel_info']            # Удаляем еще один ненужный словарь
        with open(file_path, 'w') as file:  # Записываем в файл только необходимые данные
            json.dump(data, file, indent=2, ensure_ascii=False)
