import os
import sys
from yt_dlp import YoutubeDL

class VideoDownloader:
    def __init__(self, download_path="Videos"):
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

        # Corrige o caminho para ffmpeg mesmo quando compilado com PyInstaller
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        self.ffmpeg_path = os.path.join(base_path, "ffmpeg/bin")  # aponta para a pasta ffmpeg

    def download_video(self, url):
        # Essas são as configurações para baixar o video pode estar fora de encapsulamento mas não vi motivo
        ydl_opts = {
            'format': 'bv*+ba/best',  # Baixa melhor vídeo e áudio disponíveis
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'ffmpeg_location': self.ffmpeg_path,  # adiciona o caminho
            'addmetadata': True,
            'parse_metadata': [
                '%(title)s:%(artist)s - %(title)s'
            ],
            'postprocessors': [{  # Pós-processamento com FFmpeg
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },                
            {
                    'key': 'FFmpegMetadata',
            },
                {
                    'key': 'EmbedThumbnail',
                }],
            'writethumbnail': True,
            'remote_components': ['ejs:github'],
            'js_runtimes':{'node':{}},  # se der erro de cookies adicione a flag 'cookiefile' : 'cookies.txt então baixe um cookie do youtube dentro da pasta
        }

        # Ve se é uma Url ou apenas um nome
        info = self.fetch_youtube_info(url, ydl_opts)

        # Se for uma Url valida, use ela, caso contrário use a pesquisa
        # Não era suposte precisar mas isso tava dando erro sem
        if isinstance(info, dict) and 'webpage_url' in info:
            link = info['webpage_url']
        else:
            link = url

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])


    def download_playlist(self, url):
        # Configuração para playlist é diferente da singular
        ydl_opts = {
            'format': 'bv*+ba/best',
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'noplaylist': False,
            'ffmpeg_location': self.ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        }

        with YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            for entry in playlist_info['entries']:
                ydl.download([entry['webpage_url']])

    # Aqui ele descobre se é link ou não e então pega todas as informações do video ou do resultado da pesquisa
    def fetch_youtube_info(self, search, ydl_options):
        with YoutubeDL(ydl_options) as ydl:
            if search.startswith("http"):
                return ydl.extract_info(search, download=False)
            else:
                return ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
