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
# db = shelve.open('forumdb', 'c')
# db['PinnedPosts'] = {}
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['UHC'] = {}
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['PinnedPostsPostReply'] = {}
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['UHCPostsPostReply'] = {}
# db.close()

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

# db = shelve.open('forumdb', 'c')
# post_dict = db['PinnedPostsPostReply']
# print(f"PinnedPostsPostReply db: {post_dict}")
# for post in post_dict:
#     print(f"post_id: {post}")
#     post_dict1 = post_dict[post]
#     print(f"reply_dict: {post_dict1}")
#     for key in post_dict1:
#         print(f"reply_id: {key}")
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['PinnedPostUpvoteCount'] = {}
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['PinnedPostDownvoteCount'] = {}
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['UHCPostUpvoteCount'] = {}
# db.close()
#
# db = shelve.open('forumdb', 'c')
# db['UHCPostDownvoteCount'] = {}
# db.close()

# db = shelve.open('forumdb', 'c')
# dict = db['PinnedPostsPostReply']
# # dict.pop(3)
# # dict.pop(2)
# # # dict.pop(1)
# # db['PinnedPostsPostReply'] = dict
#
# # for key in dict:
# #     if '2' in dict.keys():
# #         dict.pop(2)
# #     print(key)
# # if '2' in dict.keys():
# #     dict.remove
# print(dict)
# db.close()
