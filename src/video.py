from src.api_mixin import APIMixin


class Video(APIMixin):
    """Класс для видео-ролика с ютуб-канала"""

    def __init__(self, video_id: str):
        self.__video_id: str = video_id
        self.video_info = self.get_service().videos().list(part='snippet,statistics', id=self.__video_id).execute()
        try:
            self.title: str = self.video_info['items'][0]['snippet']['title']
        except IndexError:
            self.title: str = None
            self.url: str = None
            self.view_count: int = None
            self.like_count: int = None
        else:
            self.url: str = 'https://www.youtube.com/watch?v=' + self.__video_id
            self.view_count: int = int(self.video_info['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(self.video_info['items'][0]['statistics']['likeCount'])

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
