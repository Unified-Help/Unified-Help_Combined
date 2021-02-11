import shelve


# print(db['1'])
# a = list(db["1"].keys())
# b=a[-1]
# print(b)

# db = shelve.open('forumdb','c')
# postReplyDict = db['PinnedPostsPostReply']
# print(postReplyDict.get_username())
# print(db['PostReply'])
# db.close


# forumdb db needed for forums
db = shelve.open('forumdb', 'c')
db['PinnedPosts'] = {}
db.close()

db = shelve.open('forumdb', 'c')
db['UHC'] = {}
db.close()

db = shelve.open('forumdb', 'c')
db['PinnedPostsPostReply'] = {}
db.close()

db = shelve.open('forumdb', 'c')
db['UHCPostsPostReply'] = {}
db.close()

# db = shelve.open('account', 'c')
# db['Users'] = {}
# db.close()

# db = shelve.open('forumdb', 'c')
# print(db['UHCPostsPostReply'])
# db.close()
#
# db = shelve.open('forumdb', 'c')
# print(db['PinnedPostsPostReply'])
# db.close()

# db = shelve.open('forumdb', 'c')
# post_dict = db['UHC']
# for key in post_dict:
#     post = post_dict[key]
#     print(post.get_post_message())
# db.close()
#
# db = shelve.open('forumdb', 'c')
# print(db['UHC'])
# print(db['PinnedPosts'])
# db.close()
