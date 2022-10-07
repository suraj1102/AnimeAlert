import datetime
import requests
import sys
from bs4 import BeautifulSoup
from csv_editor import CSVEditor

sys.dont_write_bytecode = True


class WebScraper():
    def __init__(self, episode_in_db, aniDB_link):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        }

        self.episode_in_db = episode_in_db
        self.aniDB_link = aniDB_link

        self.today_date = str(datetime.date.today()).split('-')
        self.today_date = datetime.date(int(self.today_date[0]), int(self.today_date[1]),
                                        int(self.today_date[2]))

    def get_all_episodes_dates(self):
        self.page = requests.get(self.aniDB_link, headers=self.headers)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

        eplist_table = self.soup.find('table', class_='eplist')

        self.epiodes_and_airdate = {}

        for tr in eplist_table.find_all('tr'):
            for episodeNo_td, airdate_td in zip(tr.find_all('td', class_='id eid'),
                                                tr.find_all('td', class_='date airdate')):
                try:
                    self.epiodes_and_airdate[int(episodeNo_td.text.strip())] = airdate_td.text.strip()
                except:
                    pass

    def check_latest_episode(self):
        result = None

        for episode, date in self.epiodes_and_airdate.items():
            if episode > self.episode_in_db:
                ep_date = date.split('.')[::-1]
                ep_date = datetime.date(int(ep_date[0]), int(ep_date[1]), int(ep_date[2]))
                if self.today_date >= ep_date:
                    self.episode_in_db = episode
                    result = episode

        return result

# alert = WebScraper(2, 'https://anidb.net/anime/15421')
# alert.get_all_episodes_dates()
# print(alert.check_latest_episode())

# peopleEditor = CSVEditor('people_data', 'email', 'name', 'anime')

# peopleEditor.add_entry('suboxone6969@gmail.com', 'Subodh', ['Enen no Shouboutai Ni no Shou',
#     'Jujutsu Kaisen'])

# peopleEditor.add_entry('josephanthonygopay@gmail.com', 'Joseph', ['Enen no Shouboutai Ni no Shou',
#     'Tonikaku Kawaii'])

# peopleEditor.add_entry('aaronsv2005@gmail.com', 'Aaron', ['Enen no Shouboutai Ni no Shou',
#     'Black Clover'])

# peopleEditor.add_entry('mahdimikyas1429@gmail.com', 'Mahdo', ['Enen no Shouboutai Ni no Shou',
#     'Haikyuu!! To the Top'])


# animeEditor = CSVEditor('anime_data', 'anime', 'episode', 'aniDB_ID')
# animeEditor.add_entry('Enen no Shouboutai Ni no Shou', '12', 'https://anidb.net/anime/15335')
# animeEditor.add_entry('Tonikaku Kawaii', '7', 'https://anidb.net/anime/15421')
# animeEditor.add_entry('Black Clover', '7', 'https://anidb.net/anime/12665')
