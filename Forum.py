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
        self.__post_reply = {}
        self.__reply_message = ''
        self.__upvotes = 0
        self.__downvotes = 0
        self.__edited = False
        self.__datetime = datetime.now()


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

    def set_upvotes(self, upvotes):
        self.__upvotes = upvotes

    def set_downvotes(self, downvotes):
        self.__downvotes = downvotes

    def set_edited(self):
        self.__edited = True

    def set_date_time(self, datetime):
        self.__datetime = datetime
        self.__datetime = self.__datetime.strftime("%d %b %Y, %H:%M")

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

    def get_upvotes(self):
        return self.__upvotes

    def get_downvotes(self):
        return self.__downvotes

    def get_edited(self):
        return self.__edited

    def get_date_time(self):
        return self.__datetime

class ForumPinnedPostsCounter(ForumPost):
    def __init__(self):
        super().__init__()
        self.__forum_pinned_post_id = ''
        self.__post_reply_id = ''


    def set_forum_pinned_post_id(self):
        # # Use with -> Don't need to close db
        try:
            with shelve.open('forumdb','r') as db:
                if len(db['PinnedPosts']) == 0:
                    forum_pinned_post_id = 0
                else:
                    forum_pinned_post_id = list(db['PinnedPosts'].keys())[-1]
        except:
            forum_pinned_post_id = 0

        forum_pinned_post_id += 1
        self.__forum_pinned_post_id = forum_pinned_post_id

    def get_forum_pinned_post_id(self):
        return self.__forum_pinned_post_id




class ForumAnnoucementsPostCounter(ForumPost):
    def __init__(self):
        super().__init__()
        self.__forum_announcements_post_id = ''

    def set_forum_announcements_post_id(self):
        with shelve.open('forumdb','r') as db:
            if len(db['Announcements']) == 0:
                forum_announcements_post_id = 0
            else:
                forum_announcements_post_id = list(db['Announcements'].keys())[-1]

        forum_announcements_post_id += 1
        self.__forum_announcements_post_id = forum_announcements_post_id

    def get_forum_announcements_post_id(self):
        return self.__forum_announcements_post_id


class ForumUHCPostCounter(ForumPost):
    def __init__(self):
        super().__init__()
        self.__forum_uhc_post_id = ''

    def set_forum_uhc_post_id(self):
        with shelve.open('forumdb','r') as db:
            if len(db['UHC']) == 0:
                forum_uhc_post_id = 0
            else:
                forum_uhc_post_id = list(db['UHC'].keys())[-1]

        forum_uhc_post_id += 1
        self.__forum_uhc_post_id = forum_uhc_post_id

    def get_forum_uhc_post_id(self):
        return self.__forum_uhc_post_id
