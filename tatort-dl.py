import os
import string
import urllib.request
from pathlib import Path
from typing import List, Union

import youtube_dl
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
from tvdb_api_client import TVDBClient

env_path = Path('.') / '.env'
load_dotenv(
    dotenv_path=find_dotenv(env_path),
    verbose=True
)

MEDIATHEK_URL = f"https://www.daserste.de"
GANZE_FOLGEN_URL = f"{MEDIATHEK_URL}/unterhaltung/krimi/tatort/videos/index.html"
TATORT_PATH = os.getenv("SAVE_PATH")
ARCHIV_FILE = os.getenv("ARCHIV_FILE")

TVDB_USER_NAME = os.getenv("TVDB_USER_NAME")
TVDB_USER_KEY = os.getenv("TVDB_USER_KEY")
TVDB_API_KEY = os.getenv("TVDB_API_KEY")
TVDB_SERIES_ID = 83214


class TatortDl:

    def hook(self, d):
        if d["status"] == "finished":
            archive_file = open(ARCHIV_FILE, "a")
            archive_file.write(f"\n{d['filename'].rsplit('/', 1)[1].split('.')[0].strip()}")
            archive_file.close()
            print(f"{d['filename']} Done")

    def get_all_pages(self):
        all_elements = self.soup.find("div", {"class": "entries list"}).find_all("a")
        all_pages = set()
        for e in all_elements:
            all_pages.add(f"{MEDIATHEK_URL}{e['href']}")
        return all_pages

    def get_all_episodes_from_page(self, link):
        episodes_page = BeautifulSoup(urllib.request.urlopen(link), "html.parser")
        all_elements = episodes_page.find("div", {"class": "modMini"}).find_all("h4", {"class": "headline"})
        for e in all_elements:
            self.all_episodes[e.find('a').string.strip()] = {"link": f"{MEDIATHEK_URL}{e.find('a')['href']}"}

    def get_series_information_for_episode(self, title):
        filename = ""
        for episode in self.known_episodes:
            if episode['episodeName'] is not None:
                if title.lower() in episode['episodeName'].lower():
                    tvdb_episode_name = episode['episodeName'].translate(
                        {ord(c): None for c in string.whitespace})
                    season_episode = f"s{episode['airedSeason']}e{str(episode['airedEpisodeNumber']).zfill(2)}"
                    filename = f"{season_episode}_{tvdb_episode_name}"
                    self.all_episodes[title]["season"] = episode['airedSeason']
                    break
        if filename == "":
            print(f"{title} konnte kein Episodennamen zugeordnet werden")
            filename = title
        self.all_episodes[title]["filename"] = filename

    def download_video(self, episode_data):
        archive_file = open(ARCHIV_FILE, "r")
        found = False
        for line in archive_file:
            if episode_data["filename"] in line:
                archive_file.close()
                print(f"{episode_data['filename']} does exist")
                found = True
                break

        if not found:
            archive_file.close()
            if "season" not in episode_data:
                ydl_opts = {'outtmpl': f"{TATORT_PATH}/"
                                       f"0000unsorted/"
                                       f"{episode_data['filename']}.mp4"}
            else:
                ydl_opts = {'outtmpl': f"{TATORT_PATH}/"
                                       f"Season{episode_data['season']}/"
                                       f"{episode_data['filename']}.mp4"}
            ydl_opts["format"] = "best[height<=?1080]"
            ydl_opts["rate-limit"] = "10M"
            ydl_opts["progress_hooks"] = [self.hook]
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            with ydl:
                result = ydl.extract_info(episode_data["link"], download=True)
                print(result)

    def start(self):
        for e in self.all_episodes:
            self.download_video(episode_data=self.all_episodes[e])

    def __init__(self):
        self.tvdb_client = TVDBClient(TVDB_USER_NAME, TVDB_USER_KEY, TVDB_API_KEY)
        self.known_episodes = self.get_episodes_by_series_from_tvdb(TVDB_SERIES_ID)
        self.soup = BeautifulSoup(urllib.request.urlopen(GANZE_FOLGEN_URL), "html.parser")
        self.all_pages = self.get_all_pages()
        self.all_episodes = {}
        for page in self.all_pages:
            self.get_all_episodes_from_page(page)
        for episode in self.all_episodes:
            self.get_series_information_for_episode(episode)

    def get_episodes_by_series_from_tvdb(self, tvdb_id: Union[str, int]) -> List[dict]:
        base_url = self.tvdb_client._urls["series_episodes"].format(id=tvdb_id)
        full_data = self.tvdb_client._get(base_url)
        data = full_data["data"]
        number_of_pages = int(full_data["links"]["last"])
        url = base_url + "?page={page_number}"
        for page_number in range(2, number_of_pages + 1):
            data += self.tvdb_client._get(url.format(page_number=page_number))["data"]
        return data


if __name__ == "__main__":
    g = TatortDl()
    g.start()
