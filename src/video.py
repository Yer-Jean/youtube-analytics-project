from src.api_mixin import APIMixin


class Video(APIMixin):
    """Класс для видео-ролика с ютуб-канала"""

    def __init__(self, video_id: str):
        self.__video_id: str = video_id
        video_info = self.get_service().videos().list(part='snippet,statistics', id=self.__video_id).execute()
        try:
            self.title: str = video_info['items'][0]['snippet']['title']
        except IndexError:
            self.title: str | None = None         # Можно сделать так (правильнее): self.title: str = '
            self.url: str | None = None
            self.view_count: int | None = None    # Можно сделать так (правильнее): self.view_count: int = 0
            self.like_count: int | None = None
        else:
            self.url: str = 'https://www.youtube.com/watch?v=' + self.__video_id
            self.view_count: int = int(video_info['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(video_info['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return f'{self.title}'

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id: str = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
