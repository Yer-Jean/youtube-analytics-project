import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv("YT_API_KEY")

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id: str = channel_id
        # Получаем данные канала для дальнейшей инициализации класса Channel
        self.channel_info = \
            Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # Инициализируем атрибуты класса Channel полученными данными
        self.id: str = self.channel_info['items'][0]['id']
        self.title: str = self.channel_info['items'][0]['snippet']['title']
        self.description: str = self.channel_info['items'][0]['snippet']['description']
        self.url: str = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count: str = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count: str = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count: str = self.channel_info['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_id: str):
        print(f'\nНельзя изменить значение channel_id на "{new_id}"\n')

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

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
