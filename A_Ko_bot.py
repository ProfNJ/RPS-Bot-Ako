import tweepy
import time
import random

from keys import *

print('Did you know?', flush=True)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
#Keywords
Kwords = {'rock': 1, 'paper': 2, 'scissors': 3}
#Upload Images
s_pic = api.media_upload('start.jpg')
w_pic = api.media_upload('win.jpg')
l_pic = api.media_upload('loss.jpg')
t_pic = api.media_upload('tie.png')

FILE_NAME = 'last.txt'

def judge(key, roll):
    if (key == 1 and roll == 2) or (key == 2 and roll == 3) or (key == 3 and roll == 1):
        return 1
    elif (key == 2 and roll == 1) or (key == 3 and roll == 2) or (key == 1 and roll == 3):
        return 2
    else:
        return 3

def get_lastseen(file_name):
    f_read = open(file_name, 'r')
    lastseen = int(f_read.read().strip())
    f_read.close()
    return lastseen

def set_lastseen(lastseen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(lastseen))
    f_write.close()
    return


def find_key(value):
    return next((k for k, v in Kwords.items() if v == value), None)

def reply():
    print('checking for tweets...', flush=True)
    lastseen = get_lastseen(FILE_NAME)
    mentions = api.mentions_timeline(lastseen, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        lastseen = mention.id
        set_lastseen(lastseen, FILE_NAME)
        if 'duel me' in mention.full_text.lower():
            print('got a challenge!')
            print('accepting duel...')
            api.update_status('@' + mention.user.screen_name + ' It was a mistake to challenge me. Reply with Rock, Scissors, or Paper.', mention.id, media_ids = [s_pic.media_id])
        elif any(x in mention.full_text.lower().split() for x in Kwords):
            #Check if mention is a reply to a challenge acceptance
            rep = mention.in_reply_to_status_id
            if rep is not None:
                #check the first throw
                toss = next((x for x in Kwords if x in mention.full_text.lower().split()), False)
                key = Kwords.get(toss, 0)
                print(key)
                #A-ko throws
                roll = random.randint(1,3)
                print(roll)
                #See who wins
                d = judge(key, roll)
                print('replying with result')
                if (d == 1):
                    api.update_status('@' + mention.user.screen_name + ' Hiya! I play... ' + find_key(roll) + "! \n" + "Victory, as expected.", mention.id, media_ids = [w_pic.media_id])
                elif (d == 2):
                    api.update_status('@' + mention.user.screen_name + ' Hiya! I play... ' + find_key(roll) + "! \n" + "No way... I lost?", mention.id, media_ids = [l_pic.media_id])
                else:
                    api.update_status('@' + mention.user.screen_name + ' Hiya! I play... ' + find_key(roll) + "! \n" + "A tie. I spared you this time.", mention.id, media_ids = [t_pic.media_id]) 




while True:
    reply()
    time.sleep(10)