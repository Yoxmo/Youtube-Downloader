from time import sleep
from progressbar import progressbar
import pytube as pyt
from pytube import Playlist
import os
from moviepy.editor import *
import re

def removeSpecialCharacteres(string):
    characteresEspecials = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.', ',', ';', "'", '~','#']
    for c in characteresEspecials:
        if c in string:
            string = string.replace(c, '')
    return string

def readPlaylists():
    playlists = []
    for line in open("playlist.txt"):
        li=line.strip()
        if not li.startswith("#"):
            playlists.append(li)
    return playlists

def downloadPlaylist(link):
    pl = Playlist(link)
    nomePlaylist = pl.title
    if not os.path.exists(nomePlaylist):    # Verifica se o diretorio ja existe
        os.mkdir(nomePlaylist)              # Cria o diretorio


    musicasLocal = [s.replace(".mp3", "") for s in os.listdir(nomePlaylist)]
    videos = pl.videos
    print("Lendo playlist " + nomePlaylist)
    playlistNomes = [v.title for v in videos]
    playlistNomes = [removeSpecialCharacteres(n) for n in playlistNomes]
    
    dif = list(set(playlistNomes) - set(musicasLocal))
    #print(dif)
    if len(dif) > 0:
        print('Baixando')
        for video in progressbar(videos, redirect_stdout=True):
            titulo = removeSpecialCharacteres(video.title)   # Remove os characteres especiais
            if titulo in dif:
                video.streams.filter(only_audio=True).first().download(nomePlaylist)    # Download do video
                convert = AudioFileClip(nomePlaylist + '/' + titulo + ".mp4")
                convert.write_audiofile(nomePlaylist + '/' + titulo + ".mp3", verbose=False, logger=None)   # Converte o video para audio
                os.remove(nomePlaylist + '/' + titulo + ".mp4")                                         # Remove o video
                print("Baixou: " + titulo)
    else:
        print("Playlist atualizada" )
        
        
links = readPlaylists()

for link in links:
    downloadPlaylist(link)
    sleep(1)