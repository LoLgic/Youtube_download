from pytube import YouTube
from Error import DownloadError
import requests
import os

import urllib.error

# Clase para gestionar la descarga de videos de YouTube
class VideoDownloader:
    def __init__(self):
        self.video_link = ""
        self.file_path = ""
        self.download_format = ""
        
    # Método para establecer la URL del video a descargar    
    def set_url(self, link):
        self.video_link = link
    
    # Método para establecer la ruta de descarga del video
    def set_download_path(self, path):
        self.file_path = path
        
    # Método para establecer la calidad del video a descargar
    def set_quality(self, format):
        self.download_format = format
        
    # Método para obtener el objeto de video de YouTube
    def video_yt(self):
        try:  
            self.youtube_video = YouTube(self.video_link) 
            return self.youtube_video 
        except Exception as e:
            errorLink = 'regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*'
            if str(e) == errorLink:
                raise DownloadError("Ingrese una URL de video válida.")
            else:
                raise DownloadError(str(e))
            
            
    # Método para obtener las resoluciones disponibles del video    
    def get_available_resolutions(self):
        try:
            video = self.video_yt()
            streams = video.streams
            video_streams = streams.filter(type='video', file_extension='mp4')
            resolutions = sorted(set(stream.resolution for stream in video_streams if int(stream.resolution[:-1]) >= 360), key=self.resolution_key)
            return list(["mp3"] + resolutions)
        except urllib.error.URLError as e:
            raise DownloadError("No estás conectado a internet. Revisa tu conexión.")
            
    # Método auxiliar para ordenar las resoluciones        
    def resolution_key(self, resolution):
        return int(resolution[:-1])

    # Método para descargar la carátula del video
    def download_front_cover(self):
        video = self.video_yt()
        thumbnail_url = video.thumbnail_url
        response = requests.get(thumbnail_url)
        img_filename = f'{video.streams[0].title}.jpg'
        img_path = os.path.join(self.file_path, img_filename)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)

    # Método para formatear la información del video descargado
    def format_download_info(self):
        video = self.video_yt()
        duration = self.format_duration(video.length)
        return f"{video.title} - {video.author} \nDuration: {duration}"
    
    # Método auxiliar para formatear la duración del video
    def format_duration(self, duration):
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    # Método para limpiar el nombre de archivo
    def clean_filename(self, filename):
        invalid_chars = '<>:"/\\|?*'
        translation_table = str.maketrans('','',invalid_chars)
        return filename.translate(translation_table) or 'safe_title.mp3'
        
    # Método para descargar el video    
    def download_video(self):
        try:
            video = self.video_yt()
            mp3_name = self.clean_filename(f'{video.streams[0].title}.mp3')
            resolution = self.download_format
            if resolution == "mp3":
                video_stream = video.streams.filter(only_audio=True).first()
                video_stream.download(output_path=self.file_path, filename=mp3_name)
            else:
                if resolution:
                    video_stream = video.streams.filter(res=resolution, file_extension='mp4').first()
                    video_stream.download(output_path=self.file_path)
                else:
                    video_stream = video.streams.filter(only_audio=True).first()
                    video_stream.download(output_path=self.file_path, filename=mp3_name)
        except urllib.error.URLError as e:
            raise DownloadError("No estás conectado a internet. Revisa tu conexión.")