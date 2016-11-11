#encoding:utf-8

import os
import random

from utils import (get_url, download_file, telegram_autoplay_limit,
                   just_send_an_album)


def weighted_random(d):
    r = random.uniform(0, sum(val for val in d.values()))
    s = 0.0
    for k, w in d.items():
        s += w
        if r < s: return k
    return k


def define_channel_for_today():
    channels = {'HistoryPorn': 8,
        'ArchivePorn': 0.5
        # Add something from this list:
        # /r/ADifferentEra
        # /r/BattlePaintings
        # /r/BiographyFilms
        # /r/Castles
        # /r/Colorization
        # /r/ColorizedHistory
        # /r/CombatFootage
        # /r/FortPorn
        # /r/History
        # /r/HistoryNetwork
        # /r/ImagesOfHistory
        # /r/ImaginaryHistory
        # /r/ImaginaryPolitics
        # /r/MapIt
        # /r/MegalithPorn
        # /r/OldIndia
        # /r/OldSchoolCool
        # /r/OldSchoolCreepy
        # /r/Presidents
        # /r/PropagandaPosters
        # /r/RedditThroughHistory
        # /r/RestofHistoryPorn
        # /r/TheWayWeWere
        # /r/WarshipPorn
        # /r/WWIIPics
        # /r/WWIIPlanes
        # /r/ColdWarPosters 
    }
    return weighted_random(channels)


subreddit = define_channel_for_today()
t_channel = '@RedditHistory'


def just_send_message(submission, bot):
    title = submission.title
    link = submission.short_link
    if submission.is_self is True:    
        punchline = submission.selftext
        text = '{}\n\n{}\n\n{}'.format(title, punchline, link)
    else:
        url = submission.url
        text = '{}\n{}\n\n{}'.format(title, url, slink)
    bot.sendMessage(t_channel, text)
    return True


def send_post(submission, bot):
    what, url, ext = get_url(submission)
    title = submission.title
    link = submission.short_link
    text = '{}\n{}'.format(title, link)

    if what == 'text':
        return just_send_message(submission, bot)

    elif what == 'album':
        just_send_message(submission, bot)
        just_send_an_album(t_channel, url, bot)
        return True

    elif what == 'other':
        return just_send_message(submission, bot)

    filename = 'r_history.{}'.format(ext)
    if not download_file(url, filename):
        return just_send_message(submission, bot)
    if os.path.getsize(filename) > telegram_autoplay_limit:
        return just_send_message(submission, bot)

    if what == 'gif':
        f = open(filename, 'rb')
        bot.sendDocument(t_channel, f, caption=text)
        f.close()
        return True

    elif what == 'img':
        f = open(filename, 'rb')
        bot.sendPhoto(t_channel, f, caption=text)
        f.close()
        return True

    else:
        return False