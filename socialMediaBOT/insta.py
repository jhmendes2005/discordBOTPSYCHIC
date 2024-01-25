import instaloader
import json
import time

class InstagramNotifier:
    def __init__(self):
        self.username = 'psychicdesigner'
        self.loader = instaloader.Instaloader()
        self.profile = instaloader.Profile.from_username(self.loader.context, self.username)
        self.last_post_file = './socialMediaBOT/data/last_post.json'
        self.fixed_posts_count = 3  # Número de posts fixados

    def get_last_post(self):
        try:
            with open(self.last_post_file, 'r') as file:
                last_post = json.load(file)
        except FileNotFoundError:
            last_post = None
        return last_post

    def save_last_post(self, shortcode):
        with open(self.last_post_file, 'w') as file:
            json.dump({'shortcode': shortcode}, file)

    def get_latest_post(self):
        # Carrega o estado anterior
        last_post = self.get_last_post()

        # Obtém os posts mais recentes excluindo os posts fixados
        recent_posts = list(self.profile.get_posts())
        recent_posts = recent_posts[self.fixed_posts_count:]

        # Verifica se há um novo post
        if last_post is None or recent_posts[0].shortcode != last_post.get('shortcode'):
            return recent_posts[0]
        else:
            return None

    def extract_post_info(self, post):
        post_info = {
            'Caption': post.caption,
            'Data de Publicação': post.date_utc,
            'Número de Curtidas': post.likes,
            'Número de Comentários': post.comments,
            'Link do Post': f'https://www.instagram.com/p/{post.shortcode}/'
        }
        return post_info

    def main_insta(self):
        latest_post = self.get_latest_post()
        if latest_post is not None:
            post_info = self.extract_post_info(latest_post)
            self.save_last_post(latest_post.shortcode)
            return post_info
        else:
            return None