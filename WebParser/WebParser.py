import re
import emoji
import requests
from bs4 import BeautifulSoup
from instagrapi import Client


class TextProcessor:
    def __init__(self):
        pass

    def remove_emoji_from_text(self, text):
        return emoji.demojize(text, delimiters=("", ""))

    def remove_indents_from_text(self, text):
        return ' '.join(text.split())


class PostParser:
    def __init__(self):
        self.text_processor_object = TextProcessor()

        self.current_social_network = ''
        self.current_parsing_url = ''

    def parse_sc_post(self, social_media, post_URL):
        self.current_social_network = social_media
        self.current_parsing_url = post_URL

        if social_media == 'VKONTAKTE':
            return self._parse_vkontakte_post()
        elif social_media == 'INSTAGRAM':
            return self._parse_instagram_post()
        elif social_media == 'TELEGRAM':
            return self._parse_telegram_post()
        else:
            return self._parse_unknown_sc_post()

    def _parse_vkontakte_post(self):
        request = requests.get(self.current_parsing_url)
        request.encoding = 'UTF-8'

        parsed_post = BeautifulSoup(request.text, features='html.parser')
        html_text = parsed_post.find('div', class_='pi_text')

        emoji_tags = html_text.find_all('img', class_='emoji')
        for emoji_tag in emoji_tags:
            html_text.find('img', class_='emoji').replaceWith(' ' + emoji_tag['alt'] + ' ')

        post_text = html_text.text
        post_text = self.text_processor_object.remove_emoji_from_text(post_text)
        post_text = self.text_processor_object.remove_indents_from_text(post_text)

        return post_text

    def _parse_instagram_post(self):
        instagram_web_api = Client()
        instagram_web_api.login('login', 'password')

        media_pk = instagram_web_api.media_pk_from_url(self.current_parsing_url)
        post_info = instagram_web_api.media_info(media_pk)
        post_text = dict(post_info)["caption_text"]

        post_text = self.text_processor_object.remove_emoji_from_text(post_text)
        post_text = self.text_processor_object.remove_indents_from_text(post_text)

        return post_text

    def _parse_telegram_post(self):
        request = requests.get(self.current_parsing_url)
        request.encoding = 'UTF-8'

        parsed_post = BeautifulSoup(request.text, features='html.parser')
        post_text = parsed_post.find('meta', property='og:description').get('content')

        post_text = self.text_processor_object.remove_emoji_from_text(post_text)
        post_text = self.text_processor_object.remove_indents_from_text(post_text)

        return post_text

    def _parse_unknown_sc_post(self):
        return self.current_social_network + ' has not been found.'
