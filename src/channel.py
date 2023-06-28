class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel_info: list = []


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel_info)
