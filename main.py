import signal, traceback, logging, os, requests, sys, pytube, pyfiglet
from colorama import init
from termcolor import colored,cprint
from time import sleep
from pathlib import Path
from pytube.cli import on_progress

# after compliling with pyinstaller apparently quit() isnt a thing
def quit():
    sys.exit()

init(strip=not sys.stdout.isatty())

pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'

def handler(signum, frame):
    print(colored("\n\nGoodbye!", "red"))
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def try_site(url):
    request = requests.get(url)
    return False if pattern in request.text else True

def getAllLinks(playList):
    #allLinks = []
    #youtubeLink = 'https://www.youtube.com'
    pl = pytube.Playlist(playList)
    #for linkprefix in pl.video_urls():
    #    allLinks.append(youtubeLink + linkprefix)
    return pl.video_urls

os.system('color')
cprint(pyfiglet.figlet_format('YT Downloader', font='slant'),
       'green', attrs=['bold'])
print(colored('                          By WifiRouter', 'cyan', attrs=['bold']))
print("")
print(colored('What would you like to download today?', 'magenta'))
print(colored(' [1] ', 'blue'), colored('Single Video', 'cyan'))
print(colored(' [2] ', 'blue'), colored('Playlist', 'cyan'))
print("")
while True:
    try:
        sel = int(input(colored('Enter selection (1-2) >> ', 'white', attrs=['dark'])))
    except ValueError:
        print(colored('Must be a number.', 'red'))
    else:
        if sel not in (1, 2):
            print(colored('Invalid option. Please type 1 or 2.', 'red'))
        else:
            break
if sel == 1:
    while True:
        link_url = input(colored('Enter video URL >> ', 'white', attrs=['dark']))
        print(colored('Searching for your video...', 'yellow'))
        if (try_site(link_url) == False):
            print(colored('Video not found!', 'red'))
        else:
            yt = pytube.YouTube(link_url)
            vid = yt.streams.first()
            print(colored('Video found!', 'green'))
            print(colored(vid.title, 'blue'))
            break
    sleep(0.2)
    downloads_path = str(Path.home() / "Downloads")
    print(colored('Default path:', 'white', attrs=['dark']), colored(downloads_path, 'white'))
    while True:
        try:
            sel = input(colored('Specify custom path? (y/n) >> ', 'white', attrs=['dark']))
        except ValueError:
            print(colored('Please type y or n.', 'red'))
        else:
            if sel not in ("y", "n"):
                print(colored('Invalid option. Please type y or n.', 'red'))
            else:
                break
    if sel == "y":
        while True:
            path = input(colored('Enter new path >> ', 'white', attrs=['dark']))
            if os.path.exists(path):
                break
            else:
                print(colored("Couldn't find that folder!", 'red'))
    else:
        path = downloads_path
    print(colored("Downloading . . .", 'cyan'))
    yt=pytube.YouTube(link_url, on_progress_callback=on_progress)
    yt.streams.get_highest_resolution().download(path)
    os.startfile(path)
    sleep(0.5)
    print(colored("\nDownload complete!", 'green', attrs=['bold']))
    os.system("pause")
    quit()

if sel == 2:
    while True:
        link_url = input(colored('Enter playlist URL >> ', 'white', attrs=['dark']))
        print(colored('Searching for your playlist...', 'yellow'))
        p = pytube.Playlist(link_url)
        try:
            for url in p.video_urls[:1]:
                balls = url
        except Exception as e:
            print(colored('Playlist not found!', 'red'))
        else:
            print(colored('Playlist! found!', 'green'))
            print(colored(p.title, 'blue'))
            break
    sleep(0.2)
    downloads_path = str(Path.home() / "Downloads")
    print(colored('Default path:', 'white', attrs=['dark']), colored(downloads_path, 'white'))
    while True:
        try:
            sel = input(colored('Specify custom path? (y/n) >> ', 'white', attrs=['dark']))
        except ValueError:
            print(colored('Please type y or n.', 'red'))
        else:
            if sel not in ("y", "n"):
                print(colored('Invalid option. Please type y or n.', 'red'))
            else:
                break
    if sel == "y":
        while True:
            path = input(colored('Enter new path >> ', 'white', attrs=['dark']))
            if os.path.exists(path):
                break
            else:
                print(colored("Couldn't find that folder!", 'red'))
    else:
        path = downloads_path
    print(colored("Downloading . . .", 'cyan'))
    #for video in p.videos:
    #    video.streams.first().download(path)
    linkArray = getAllLinks(link_url)
    for link in linkArray:
        yt=pytube.YouTube(link, on_progress_callback=on_progress)
        vid = yt.streams.first()
        print(colored("\nDownloading", 'yellow'), colored(vid.title, 'yellow'))
        yt.streams.get_highest_resolution().download(path)
    sleep(0.5)
    print(colored("\nDownload complete!", 'green', attrs=['bold']))
    os.startfile(path)
    os.system("pause")
    quit()
    
