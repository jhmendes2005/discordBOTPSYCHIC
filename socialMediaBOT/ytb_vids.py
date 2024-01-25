from googleapiclient.discovery import build
import json
import time

class YouTubeNotifier:
    def __init__(self):
        self.api_key = 'AIzaSyBMyEUxCf9UYdfkQSBgUt-4L4tmbbWfcVU'
        self.channel_id = 'UCHXf9U6X0yAKBpbleYMedqw'
        self.last_video_file = './socialMediaBOT/data/last_video.json'
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_last_video(self):
        try:
            with open(self.last_video_file, 'r') as file:
                last_video = json.load(file)
        except FileNotFoundError:
            last_video = None
        return last_video

    def save_last_video(self, video_id):
        with open(self.last_video_file, 'w') as file:
            json.dump({'video_id': video_id}, file)

    def get_latest_video(self):
        # Carrega o estado anterior
        last_video = self.get_last_video()

        try:
            # Obtém a lista de uploads do canal
            response = self.youtube.channels().list(
                part='contentDetails',
                id=self.channel_id
            ).execute()

            # Verifica se a chave 'items' está presente na resposta
            if 'items' in response and response['items']:
                # Obtém a playlist de uploads do canal
                uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

                # Obtém os vídeos mais recentes na playlist de uploads
                response = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=uploads_playlist_id,
                    maxResults=1
                ).execute()

                # Verifica se a chave 'items' está presente na segunda resposta
                if 'items' in response and response['items']:
                    latest_video_id = response['items'][0]['contentDetails']['videoId']

                    # Verifica se há um novo vídeo
                    if last_video is None or latest_video_id != last_video.get('video_id'):
                        return latest_video_id
                else:
                    print("Erro: 'items' não encontrado na segunda resposta.")

        except KeyError as e:
            print(f"Erro ao obter vídeos: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        return None


    def extract_video_info(self, video_id):
        video_info = self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()['items'][0]['snippet']

        return {
            'Título': video_info['title'],
            'Descrição': video_info['description'],
            'Data de Publicação': video_info['publishedAt'],
            'Link do Vídeo': f'https://www.youtube.com/watch?v={video_id}'
        }

    def main_ytb(self):
        latest_video_id = self.get_latest_video()
        if latest_video_id is not None:
            video_info = self.extract_video_info(latest_video_id)
            self.save_last_video(latest_video_id)
            return video_info
        else:
            return None