from flask import session
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
import shelve
from ForumForm import Form
import datetime
from datetime import datetime

class ForumPost:
    def __init__(self):
        self.__username = ''
        self.__post_subject = ''
        self.__category = ''
        self.__post_message = ''
        self.__reply_message = ''
        self.__reply_category = ''
        self.__upvote = 0
        self.__downvote = 0
        self.__edited = False
        self.__datetime = datetime.now()
        self.__reply_count = 0

    # Mutator
    def set_username(self, username):
        self.__username = username

    def set_post_subject(self, post_subject):
        self.__post_subject = post_subject

    def set_category(self, category):
        self.__category = category

    def set_post_message(self, post_message):
        self.__post_message = post_message

    def set_reply_message(self, reply_message):
        self.__reply_message = reply_message

    def set_reply_category(self,reply_category):
        self.__reply_category = reply_category

    def set_upvote(self, upvotes):
        self.__upvotes = upvotes

    def set_downvote(self, downvotes):
        self.__downvotes = downvotes

    def set_edited(self):
        self.__edited = True

    def set_date_time(self, datetime):
        self.__datetime = datetime
        self.__datetime = self.__datetime.strftime("%d %b %Y, %X")

    def set_reply_count(self,reply_count):
        self.__reply_count = reply_count

    # Accessor
    def get_username(self):
        return self.__username

    def get_post_subject(self):
        return self.__post_subject

    def get_category(self):
        return self.__category

    def get_post_message(self):
        return self.__post_message

    def get_reply_message(self):
        return self.__reply_message

    def get_reply_category(self):
        return self.__reply_category

    def get_upvote(self):
        return self.__upvotes

    def get_downvote(self):
        return self.__downvotes

    def get_edited(self):
        return self.__edited

    def get_date_time(self):
        return self.__datetime

    def get_reply_count(self):
        return self.__replycount

class ForumPinnedPostsCounter(ForumPost):
    def __init__(self):
        super().__init__()
        self.__post_id = ''

    def set_post_id(self):
        # Use with -> Don't need to close db
        try:
            with shelve.open('forumdb','r') as db:
                if len(db['PinnedPosts']) == 0:
                    post_id = 0
                else:
                    post_id = list(db['PinnedPosts'].keys())[-1]
        except:
            post_id = 0

        post_id += 1
        self.__post_id = post_id

    def get_post_id(self):
        return self.__post_id

    def set_post_reply_id(self, post_reply_id):
        self.__post_reply_id = post_reply_id

    def get_post_reply_id(self):
        return self.__post_reply_id


class ForumUHCPostCounter(ForumPost):
    def __init__(self):
        super().__init__()
        self.__post_id = ''

    def set_post_id(self):
        with shelve.open('forumdb','r') as db:
            if len(db['UHC']) == 0:
                post_id = 0
            else:
                post_id = list(db['UHC'].keys())[-1]

        post_id += 1
        self.__post_id = post_id

    def get_post_id(self):
        return self.__post_id

    def set_post_reply_id(self, post_reply_id):
        self.__post_reply_id = post_reply_id

    def get_post_reply_id(self):
        return self.__post_reply_id
