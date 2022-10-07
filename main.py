#!/usr/local/bin/python3

import smtplib
import sys
from csv_editor import CSVEditor
from web_scraper import WebScraper

sys.dont_write_bytecode = True


global AnimeAlert
class AnimeAlert():
    def __init__(self):
        self.animeEditor = CSVEditor('anime_data', 'anime', 'episode', 'aniDB_ID')
        self.peopleEditor = CSVEditor('people_data', 'email', 'name', 'anime')


    def update_DB(self):
        self.anime_data = self.animeEditor.get_all_entries()

        self.anime_name = self.anime_data['anime']
        self.links = self.anime_data['aniDB_ID']
        self.episodes_in_DB = self.anime_data['episode']

        self.latest_episodes = []

        for i in range(len(self.links)):
            web_stuff = WebScraper(int(self.episodes_in_DB[i]), self.links[i])
            web_stuff.get_all_episodes_dates()
            latest_episode = web_stuff.check_latest_episode()

            if latest_episode != None:
                self.animeEditor.update_entry(self.anime_name[i], episode = latest_episode)
                self.latest_episodes.append(latest_episode)

            else:
                latest_episode = self.episodes_in_DB[i]
                self.latest_episodes.append(latest_episode)


    def new_episode_anime(self):
        self.anime_to_alert = []

        for i in range(len(self.anime_name)):
            if int(self.episodes_in_DB[i]) < int(self.latest_episodes[i]):
                self.anime_to_alert.append(self.anime_name[i])


    def who_to_mail(self):
        self.people_data = self.peopleEditor.get_all_entries()
        self.names = self.people_data['name']
        self.emails = self.people_data['email']


        for i in range(len(self.people_data['email'])):
            email = self.people_data['email'][i]
            for anime in self.people_data['anime'][i]:
                if anime in self.anime_to_alert:
                    self.send_mail(email, anime)


    def send_mail(self, email, anime):
        name = self.names[self.emails.index(email)]
        episode = self.latest_episodes[self.anime_name.index(anime)]

        subject = f'Anime Alert - {anime}'
        body = f"Hey {name}, \nepisode {episode} of {anime} just dropped!"

        msg = f"Subject: {subject}\n\n{body}".encode('utf-8')

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

        self.server.login('suraj.dayma11@gmail.com', 'soenlnftxnesonyz')

        self.server.sendmail(
        'suraj.dayma11@gmail.com',
        email,
        msg
        )
        print(f'EMAIL SENT TO {name.upper()}, {anime, episode}')

        self.server.quit()

def main():
    global AnimeAlert
    AnimeAlert = AnimeAlert()
    AnimeAlert.update_DB()
    AnimeAlert.new_episode_anime()
    AnimeAlert.who_to_mail()

if __name__ == '__main__':
    main()
