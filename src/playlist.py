import datetime

import isodate

from src.api_mixin import APIMixin


class PlayList(APIMixin):

    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id
        # Получаем информацию о плейлисте по его id
        self.playlist_info = self.get_service().playlists().list(id=self.__playlist_id,
                                                                 part='snippet',
                                                                 ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.__playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    def get_videos_info_from_playlist(self):
        # Получаем объект, содержащий информацию о видеороликах в плейлисте playlist_id
        videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                         part='contentDetails',
                                                         maxResults=50,
                                                         ).execute()
        # Собираем все id видеороликов из плейлиста в список
        videos_ids: list[str] = [video['contentDetails']['videoId'] for video in videos['items']]
        # Получаем и возвращаем информацию и статистику по видеороликам
        return self.get_service().videos().list(part='contentDetails,statistics',
                                                id=','.join(videos_ids)
                                                ).execute()

    @property
    def total_duration(self):
        duration = datetime.timedelta()  # Создаём объект для хранения длительности времени плейлиста
        # Получаем информацию о видеороликах в плейлисте
        videos = self.get_videos_info_from_playlist()
        for video in videos['items']:
            # Из каждого видеоролика получаем длительность времени
            duration += isodate.parse_duration(video['contentDetails']['duration'])
        return duration

    def show_best_video(self):
        # Получаем информацию о видеороликах в плейлисте
        videos = self.get_videos_info_from_playlist()
        max_like = 0
        best_video_url = ''
        # Ищем видеоролик с максимальным количеством лайков
        for video in videos['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like:
                max_like = like_count
                best_video_url = 'https://youtu.be/' + video['id']
        return best_video_url
