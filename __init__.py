# Imports
from flask import Flask, render_template, request, redirect, url_for, session, g
# from flask_login import login_required, LoginManager
import shelve

# Donation Imports
from donateMoney import donateMoney
from donateItem import donateItem
from Donate import DonateMoney, DonateItem

# Customer Support Imports
from ForumForm import createForumPost, updateForumPost, staff_createForumPost
from Forum import ForumPost, ForumPinnedPostsCounter, ForumAnnoucementsPostCounter, ForumUHCPostCounter

# Account Management Imports
from Forms import CreateUserForm, LoginForm
from User import User
from datetime import timedelta

# Report Generation Imports
from Staff_RG_manual_upload import ManualUploadForm
import csv
import datetime
from Staff_RG_costs import Data

app = Flask(__name__)
# Jinja for loop lib
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


# ================================================== Customer Side ================================================== #

# Home
@app.route("/")
def home():
    return render_template('customer/index.html')


# Transaction Processing (Donations)
@app.route("/donate")
def donate():
    return render_template('customer/TP/Donate.html')


@app.route("/donate/history")
def donateHistory():
    # Displaying Donation History
    donorsM_dict = {}
    donorsI_dict = {}
    try:
        db = shelve.open("donorChoices", "r")

        # If only Money donations are created and Items are empty
        if "Money" in db and "Items" not in db:
            # Money History
            donorsM_dict = db["Money"]
            donorsM_list = []
            for key in donorsM_dict:
                donorM = donorsM_dict.get(key)
                donorsM_list.append(donorM)
            return render_template('customer/TP/donationHistory.html', donorsI_list='', donorsM_list=donorsM_list)

        # If only Item donations are created and Money is empty
        if "Money" not in db and "Items" in db:
            # Item History
            donorsI_dict = db["Items"]
            donorsI_list = []
            for key in donorsI_dict:
                donorI = donorsI_dict.get(key)
                donorsI_list.append(donorI)
            return render_template('customer/TP/donationHistory.html', donorsI_list=donorsI_list, donorsM_list='')

        # Once both item and money donations has been made
        if "Money" in db and "Items" in db:
            # Money History
            donorsM_dict = db["Money"]
            donorsM_list = []
            for key in donorsM_dict:
                donorM = donorsM_dict.get(key)
                donorsM_list.append(donorM)

            # Item History
            donorsI_dict = db["Items"]
            donorsI_list = []
            for key in donorsI_dict:
                donorI = donorsI_dict.get(key)
                donorsI_list.append(donorI)

            return render_template('customer/TP/donationHistory.html', donorsI_list=donorsI_list,
                                   donorsM_list=donorsM_list)
        db.close()

    except:
        return render_template('customer/TP/donationHistoryEmpty.html')


@app.route("/donate/details")
def donateDetails():
    return render_template('customer/TP/donateDetails.html')


@app.route("/donate/details/money", methods=['GET', 'POST'])
def donate_Money():
    # Monetary Donations
    donate_money = donateMoney(request.form)
    if request.method == "POST" and donate_money.validate():
        donor_moneychoices = {}

        dbMC = shelve.open("donorChoices", "c")

        try:
            donor_moneychoices = dbMC["Money"]
        except:
            print("Error in retrieving Donors MC from donorMoneyChoices")

        donor = DonateMoney(donate_money.donateToWho.data, donate_money.moneyAmount.data,
                            donate_money.cardInfo_Name.data,
                            donate_money.cardInfo_Number.data, donate_money.cardInfo_CVV.data,
                            donate_money.cardInfo_DateExpiry.data, donate_money.cardInfo_YearExpiry.data)
        donor.set_moneyID()

        if request.form.get('Cancel') == 'Cancel':
            donor.set_status("Pending")
        if request.form.get('Confirm') == 'Confirm':
            donor.set_status("Confirmed")
        # print(donor.get_status())

        donor_moneychoices[donor.get_moneyID()] = donor

        dbMC["Money"] = donor_moneychoices

        dbMC.close()

        return redirect(url_for('donateHistory'))

    return render_template('customer/TP/donateMoney.html', form=donate_money)


@app.route("/donate/details/item", methods=['GET', 'POST'])
def donate_Item():
    # Item Donations
    donate_item = donateItem(request.form)
    if request.method == "POST":
        donor_itemchoices = {}

        dbIM = shelve.open("donorChoices", "c")

        try:
            donor_itemchoices = dbIM["Items"]
        except:
            print("Error in retrieving Donors IM from donorChoices")

        donor = DonateItem(donate_item.donateToWho.data, donate_item.itemName.data, donate_item.itemName.data,
                           donate_item.itemWeight.data, donate_item.itemHeight.data, donate_item.itemLength.data,
                           donate_item.itemWidth.data, donate_item.collectionType.data, donate_item.collectionDate.data,
                           donate_item.collectionMonth.data, donate_item.collectionTime.data,
                           donate_item.pickupAddress1.data, donate_item.pickupAddress2.data,
                           donate_item.pickupAddress3.data, donate_item.pickupPostalCode.data)
        donor.set_itemID()

        if request.form.get('Cancel') == 'Cancel':
            donor.set_status("Pending")
        if request.form.get('Confirm') == 'Confirm':
            donor.set_status("Confirmed")
        # print(donor.get_status())

        donor_itemchoices[donor.get_itemID()] = donor

        dbIM["Items"] = donor_itemchoices

        dbIM.close()

        return redirect(url_for('donateHistory'))

    return render_template('customer/TP/donateItem.html', form=donate_item)


@app.route("/donate/details/confirmation/<string:id>", methods=['GET', 'POST'])
def donate_Confirmation(id):
    if request.method == 'POST':
        donation_dict = {}

        db = shelve.open('donorChoices', 'w')
        if id[0] == "M":
            donation_dict = db['Money']
            donor = donation_dict.get(id)

            # Change status with respect to choice
            if request.form.get('Delete') == 'Delete':
                donor.set_status("Archive")

            elif request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")

            db["Money"] = donation_dict

        elif id[0] == "I":
            donation_dict = db['Items']
            donor = donation_dict.get(id)

            # Change status with respect to choice
            if request.form.get('Delete') == 'Delete':
                donor.set_status("Archive")

            elif request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")
            print(donor.get_status())

            db['Items'] = donation_dict

        else:
            print("No such ID")

        db.close()
        return redirect(url_for('donateHistory'))

    else:
        return render_template('customer/TP/donateConfirmation.html')


@app.route("/donate/itemupdate/<string:id>", methods=['GET', 'POST'])
def donate_ItemUpdate(id):
    update_donate_item = donateItem(request.form)
    if request.method == 'POST':
        donors_dict = {}

        dbUP = shelve.open('donorChoices', 'w')
        donors_dict = dbUP['Items']

        donor = donors_dict.get(id)

        # Item Specifications
        donor.set_item_weight(update_donate_item.itemWeight.data)
        donor.set_item_height(update_donate_item.itemHeight.data)
        donor.set_item_length(update_donate_item.itemLength.data)
        donor.set_item_width(update_donate_item.itemWidth.data)

        # Collection Details
        donor.set_date(update_donate_item.collectionDate.data)
        donor.set_month(update_donate_item.collectionMonth.data)
        donor.set_time(update_donate_item.collectionTime.data)
        donor.set_collection_type(update_donate_item.collectionType.data)

        # If Collection is pickup
        donor.set_address1(update_donate_item.pickupAddress1.data)
        donor.set_address2(update_donate_item.pickupAddress2.data)
        donor.set_address3(update_donate_item.pickupAddress3.data)
        donor.set_postal_code(update_donate_item.pickupPostalCode.data)

        dbUP['Items'] = donors_dict
        dbUP.close()

        return redirect(url_for('donateHistory'))

    else:
        donors_dict = {}

        dbUP = shelve.open('donorChoices', 'r')
        donors_dict = dbUP["Items"]
        dbUP.close()

        donor = donors_dict.get(id)

        # Item Specifications
        update_donate_item.itemWeight.data = donor.get_item_weight()
        update_donate_item.itemHeight.data = donor.get_item_height()
        update_donate_item.itemLength.data = donor.get_item_length()
        update_donate_item.itemWidth.data = donor.get_item_width()

        # Collection Details
        update_donate_item.collectionDate.data = donor.get_date()
        update_donate_item.collectionMonth.data = donor.get_month()
        update_donate_item.collectionTime.data = donor.get_time()
        update_donate_item.collectionType.data = donor.get_collection_type()

        # If Collection is pickup
        update_donate_item.pickupAddress1.data = donor.get_address1()
        update_donate_item.pickupAddress2.data = donor.get_address2()
        update_donate_item.pickupAddress3.data = donor.get_address3()
        update_donate_item.pickupPostalCode.data = donor.get_postal_code()

        return render_template('customer/TP/donateItemUpdate.html', form=update_donate_item)


# Customer Support
@app.route('/forum/login', methods=['GET', 'POST'])
def forum_login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        b = users_dict[key]
        if b.get_username() == create_login_form.username.data and b.get_password() == create_login_form.password.data:
            session["username"] = b.get_username()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            return redirect(url_for('create_forum_post'))

    return render_template('customer/AM/login.html')


@app.route("/forum")
def forum():
    pinned_posts_dict = {}
    announcements_dict = {}
    uhc_dict = {}
    db = shelve.open('forumdb', 'c')
    pinned_posts_dict = db['PinnedPosts']
    announcements_dict = db['Announcements']
    uhc_dict = db['UHC']
    db.close()

    pinned_posts_list = []
    announcements_list = []
    uhc_list = []
    for key in pinned_posts_dict:
        post = pinned_posts_dict.get(key)
        pinned_posts_list.append(post)
    for key in announcements_dict:
        post = announcements_dict.get(key)
        announcements_list.append(post)
    for key in uhc_dict:
        post = uhc_dict.get(key)
        uhc_list.append(post)
    return render_template('customer/CS/Forum.html', pinned_posts_list=pinned_posts_list,
                           announcements_list=announcements_list,
                           uhc_list=uhc_list)


@app.route("/forum/createforumpost", methods=['GET', 'POST'])
def create_forum_post():
    try:
        session_username = session["username"]
    except:
        return redirect(url_for('forum_login'))
    else:
        create_forum_post_form = createForumPost(request.form)
        if request.method == 'POST' and create_forum_post_form.validate():
            uhc_dict = {}
            db = shelve.open('forumdb', 'c')

            try:
                uhc_dict = db['UHC']
            except:
                print("Error in retrieving data from forumdb.")

            post = ForumUHCPostCounter()
            post.set_forum_uhc_post_id()
            post.set_username(session_username)
            post.set_category('Unified Help Community')
            post.set_post_subject(create_forum_post_form.post_subject.data)
            post.set_post_message(create_forum_post_form.post_message.data)
            post.set_date_time(post.get_date_time())
            uhc_dict[post.get_forum_uhc_post_id()] = post

            db['UHC'] = uhc_dict
            db.close()
            return redirect(url_for('forum_uhc_posts'))

    return render_template('customer/CS/createForumPost.html', form=create_forum_post_form,
                           session_username=session_username)


@app.route("/forum/pinned_posts")
def forum_pinned_posts():
    pinned_posts_dict = {}
    db = shelve.open('forumdb', 'c')
    pinned_posts_dict = db['PinnedPosts']
    db.close()

    pinned_posts_list = []
    for key in pinned_posts_dict:
        post = pinned_posts_dict.get(key)
        pinned_posts_list.append(post)
    category = pinned_posts_list[0].get_category()
    return render_template('customer/CS/overview-forum-category.html', list=pinned_posts_list, category=category)


# Specific Forum Post ID - Pinned Posts
@app.route("/forum/pinned_posts/<int:forum_pinned_posts_id>", methods=['GET', 'POST'])
def forum_pinned_posts_post(forum_pinned_posts_id):
    pinned_posts_dict = {}
    db = shelve.open('forumdb', 'c')
    pinned_posts_dict = db['PinnedPosts']

    pinned_posts_list = []

    post = pinned_posts_dict.get(forum_pinned_posts_id)
    pinned_posts_list.append(post)
    post_id = post.get_forum_pinned_post_id
    post_subject = post.get_post_subject()
    post_author = post.get_username()
    post_datetime = post.get_date_time()
    post_message = post.get_post_message()
    post_edited = post.get_edited()
    category = pinned_posts_list[0].get_category()
    db.close()
    return render_template('customer/CS/forum-post.html', list=pinned_posts_list, category=category,
                           post_subject=post_subject,
                           post_author=post_author,
                           post_datetime=post_datetime, post_message=post_message, post_id=post_id,
                           post_edited=post_edited)


@app.route("/forum/pinned_posts/update/<int:forum_pinned_posts_id>", methods=['GET', 'POST'])
def forum_pinned_posts_post_update(forum_pinned_posts_id):
    forum_pinned_posts_form_update = createForumPost(request.form)
    if request.method == 'POST':
        pinned_posts_dict = {}
        db = shelve.open('forumdb', 'w')
        pinned_posts_dict = db['PinnedPosts']

        post = pinned_posts_dict.get(forum_pinned_posts_id)
        post.set_post_message(forum_pinned_posts_form_update.post_message.data)
        post.set_edited()
        db['PinnedPosts'] = pinned_posts_dict
        db.close()
        return redirect(url_for('forum_pinned_posts_post', forum_pinned_posts_id=post.get_forum_pinned_post_id()))
    else:
        pinned_posts_dict = {}
        db = shelve.open('forumdb', 'r')
        pinned_posts_dict = db['PinnedPosts']
        db.close()

        post = pinned_posts_dict.get(forum_pinned_posts_id)
        post_id = post.get_forum_pinned_post_id()
        post_subject = post.get_post_subject()
        forum_pinned_posts_form_update.post_message.data = post.get_post_message()
        category = post.get_category()
        return render_template('customer/CS/forum-post_update.html', form=forum_pinned_posts_form_update,
                               category=category, post_id=post_id, post_subject=post_subject)


@app.route('/forum/pinned_posts/delete/<int:forum_pinned_posts_id>', methods=['GET', 'POST'])
def forum_pinned_posts_post_delete(forum_pinned_posts_id):
    pinned_posts_dict = {}
    db = shelve.open('forumdb', 'w')
    pinned_posts_dict = db['PinnedPosts']

    pinned_posts_dict.pop(forum_pinned_posts_id)

    db['PinnedPosts'] = pinned_posts_dict
    db.close()

    return redirect(url_for('forum_pinned_posts'))


@app.route("/forum/announcements")
def forum_announcements_posts():
    announcements_dict = {}
    db = shelve.open('forumdb', 'c')
    announcements_dict = db['Announcements']
    db.close()

    announcements_list = []
    for key in announcements_dict:
        post = announcements_dict.get(key)
        announcements_list.append(post)
    category = announcements_list[0].get_category()
    return render_template('customer/CS/overview-forum-category.html', list=announcements_list, category=category)


# Specific Forum Post ID - Announcements
@app.route("/forum/announcements/<int:forum_announcements_post_id>")
def forum_announcements_posts_post(forum_announcements_post_id):
    announcements_dict = {}
    db = shelve.open('forumdb', 'c')
    announcements_dict = db['Announcements']
    db.close()

    announcements_list = []
    post = announcements_dict.get(forum_announcements_post_id)
    announcements_list.append(post)
    post_subject = post.get_post_subject()
    post_author = post.get_username()
    post_datetime = post.get_date_time()
    post_message = post.get_post_message()
    category = announcements_list[0].get_category()
    post_edited = post.get_edited()
    return render_template('customer/CS/forum-post.html', list=announcements_list, category=category,
                           post_subject=post_subject,
                           post_author=post_author,
                           post_datetime=post_datetime, post_message=post_message, post_edited=post_edited)


@app.route("/forum/announcements/update/<int:forum_announcements_post_id>", methods=['GET', 'POST'])
def forum_announcements_posts_post_update(forum_announcements_post_id):
    forum_announcements_form_update = createForumPost(request.form)
    if request.method == 'POST':
        announcements_dict = {}
        db = shelve.open('forumdb', 'w')
        announcements_dict = db['Announcements']

        post = announcements_dict.get(forum_announcements_post_id)
        post.set_post_message(forum_announcements_form_update.post_message.data)
        post.set_edited()
        db['Announcements'] = announcements_dict
        db.close()
        return redirect(url_for('forum_announcements_posts_post',
                                forum_announcements_post_id=post.get_forum_announcements_post_id()))
    else:
        announcements_dict = {}
        db = shelve.open('forumdb', 'r')
        announcements_dict = db['Announcements']
        db.close()

        post = announcements_dict.get(forum_announcements_post_id)
        post_id = post.get_forum_announcements_post_id()
        post_subject = post.get_post_subject()
        forum_announcements_form_update.post_message.data = post.get_post_message()
        category = post.get_category()
        return render_template('customer/CS/forum-post_update.html', form=forum_announcements_form_update,
                               category=category, post_id=post_id, post_subject=post_subject)


@app.route('/forum/announcements/delete/<int:forum_announcements_post_id>', methods=['GET', 'POST'])
def forum_announcements_post_delete(forum_announcements_post_id):
    announcements_dict = {}
    db = shelve.open('forumdb', 'w')
    announcements_dict = db['Announcements']

    announcements_dict.pop(forum_announcements_post_id)

    db['Announcements'] = announcements_dict
    db.close()

    return redirect(url_for('forum_announcements_posts'))


@app.route("/forum/uhc")
def forum_uhc_posts():
    uhc_dict = {}
    db = shelve.open('forumdb', 'c')
    uhc_dict = db['UHC']
    db.close()

    uhc_list = []
    for key in uhc_dict:
        post = uhc_dict.get(key)
        uhc_list.append(post)
    category = uhc_list[0].get_category()
    return render_template('customer/CS/overview-forum-category.html', list=uhc_list, category=category)


# Specific Forum Post ID - UHC
@app.route("/forum/uhc/<int:forum_uhc_post_id>")
def forum_uhc_posts_post(forum_uhc_post_id):
    uhc_dict = {}
    db = shelve.open('forumdb', 'c')
    uhc_dict = db['UHC']
    db.close()

    uhc_list = []
    post = uhc_dict.get(forum_uhc_post_id)
    uhc_list.append(post)
    post_subject = post.get_post_subject()
    post_author = post.get_username()
    post_datetime = post.get_date_time()
    post_message = post.get_post_message()
    category = uhc_list[0].get_category()
    post_edited = post.get_edited()
    return render_template('customer/CS/forum-post.html', list=uhc_list, category=category, post_subject=post_subject,
                           post_author=post_author,
                           post_datetime=post_datetime, post_message=post_message, post_edited=post_edited)


@app.route("/forum/uhc/update/<int:forum_uhc_post_id>", methods=['GET', 'POST'])
def forum_uhc_post_update(forum_uhc_post_id):
    forum_uhc_form_update = updateForumPost(request.form)
    if request.method == 'POST':
        uhc_dict = {}
        db = shelve.open('forumdb', 'w')
        uhc_dict = db['UHC']

        post = uhc_dict.get(forum_uhc_post_id)
        post.set_post_message(forum_uhc_form_update.post_message.data)
        post.set_edited()
        db['UHC'] = uhc_dict
        db.close()
        return redirect(url_for('forum_uhc_posts_post', forum_uhc_post_id=post.get_forum_uhc_post_id()))
    else:
        uhc_dict = {}
        db = shelve.open('forumdb', 'r')
        uhc_dict = db['UHC']
        db.close()

        post = uhc_dict.get(forum_uhc_post_id)
        post_id = post.get_forum_uhc_post_id()
        post_subject = post.get_post_subject()
        forum_uhc_form_update.post_message.data = post.get_post_message()
        category = post.get_category()
        return render_template('customer/CS/forum-post_update.html', form=forum_uhc_form_update,
                               category=category, post_id=post_id, post_subject=post_subject)


@app.route('/forum/uhc/delete/<int:forum_uhc_post_id>', methods=['GET', 'POST'])
def forum_uhc_post_delete(forum_uhc_post_id):
    uhc_dict = {}
    db = shelve.open('forumdb', 'w')
    uhc_dict = db['UHC']

    uhc_dict.pop(forum_uhc_post_id)

    db['UHC'] = uhc_dict
    db.close()

    return redirect(url_for('forum_uhc_posts'))


# Account Management

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('account.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from account.db.")

        user = User(create_user_form.username.data, create_user_form.email.data, create_user_form.gender.data,
                    create_user_form.password.data, create_user_form.confirm_password.data)
        user.set_date_time(user.get_date_time())
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        session['user_created'] = user.get_username()

        return redirect(url_for('profile'))
    return render_template('customer/AM/CreateAccount.html', form=create_user_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        b = users_dict[key]
        if b.get_username() == create_login_form.username.data and b.get_password() == create_login_form.password.data:
            session["username"] = b.get_username()
            session["email"] = b.get_email()
            session["gender"] = b.get_gender()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            return redirect(url_for('profile'))

    return render_template('customer/AM/login.html')


@app.route('/profile')
def profile():
    if "username" in session:
        username = session["username"]
        email = session["email"]
        gender = session["gender"]
        return render_template('customer/AM/profile.html', username=username, email=email, gender=gender)
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('account.db', 'c')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_username(update_user_form.username.data)
        user.set_email(update_user_form.email.data)
        user.set_gender(update_user_form.gender.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_username()

        return redirect(url_for('retrieve_users'))
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('customer/index.html')


@app.route('/retrieveusers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('account.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('staff/AM/unlock_delete_acc.html', count=len(users_list), users_list=users_list)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('account.db', 'c')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_username(update_user_form.username.data)
        user.set_email(update_user_form.email.data)
        user.set_gender(update_user_form.gender.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_username()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('account.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.username.data = user.get_username()
        update_user_form.email.data = user.get_email()
        update_user_form.gender.data = user.get_gender()
        update_user_form.password.data = user.get_password()
        update_user_form.confirm_password.data = user.get_confirm_password()

        return render_template('customer/AM/updateAccount.html', form=update_user_form)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('account.db', 'w')
    users_dict = db['Users']

    user = users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    session['user_deleted'] = user.get_username()

    return redirect(url_for('retrieve_users'))


# ================================================== Staff Side ================================================== #


@app.route('/staff_home')
def staff_home():
    return render_template('staff/home.html', user_name="General Kenobi")


# ------------ Account Management ------------ #
@app.route("/staff_profile")
def staff_profile():
    return render_template('staff/AM/staff_profile.html')


@app.route("/account_management")
def account_management():
    return render_template('staff/AM/unlock_delete_acc.html')


@app.route('/retrieve')
def retrieve():
    users_dict = {}
    db = shelve.open('account.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('staff/AM/unlock_delete_acc.html', count=len(users_list), users_list=users_list)


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('account.db', 'c')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_username(update_user_form.username.data)
        user.set_email(update_user_form.email.data)
        user.set_gender(update_user_form.gender.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_username()

        return redirect(url_for('retrieve'))
    else:
        users_dict = {}
        db = shelve.open('account.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.username.data = user.get_username()
        update_user_form.email.data = user.get_email()
        update_user_form.gender.data = user.get_gender()
        update_user_form.password.data = user.get_password()
        update_user_form.confirm_password.data = user.get_confirm_password()

        return render_template('staff/AM/updateAccount.html', form=update_user_form)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    users_dict = {}
    db = shelve.open('account.db', 'w')
    users_dict = db['Users']

    user = users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    session['user_deleted'] = user.get_username()

    return redirect(url_for('retrieve'))


# ------------ Transaction Processing ------------ #

@app.route("/incoming_items")
def incoming_item():
    return render_template('staff/TP/incoming_item.html')


# ------------ Customer Support ------------ #

@app.route("/staff_forum")
def staff_forum():
    pinned_posts_dict = {}
    announcements_dict = {}
    uhc_dict = {}
    db = shelve.open('forumdb', 'c')
    pinned_posts_dict = db['PinnedPosts']
    announcements_dict = db['Announcements']
    uhc_dict = db['UHC']
    db.close()

    pinned_posts_list = []
    announcements_list = []
    uhc_list = []
    for key in pinned_posts_dict:
        post = pinned_posts_dict.get(key)
        pinned_posts_list.append(post)
    for key in announcements_dict:
        post = announcements_dict.get(key)
        announcements_list.append(post)
    for key in uhc_dict:
        post = uhc_dict.get(key)
        uhc_list.append(post)
    return render_template('staff/CS/staff_forum.html', pinned_posts_list=pinned_posts_list,
                           announcements_list=announcements_list,
                           uhc_list=uhc_list)


@app.route("/staff_forum/createforumpost", methods=['GET', 'POST'])
def create_staff_forum_post():
    create_forum_post_form = staff_createForumPost(request.form)
    if request.method == 'POST' and create_forum_post_form.validate():
        # users_dict = {}
        pinned_posts_dict = {}
        announcements_dict = {}
        uhc_dict = {}
        db = shelve.open('forumdb', 'c')

        # users_db = shelve.open('account.db', 'r')
        # users_db = users_db['Users']
        # users_db.close()

        # session_username = session['username']

        try:
            pinned_posts_dict = db['PinnedPosts']
            announcements_dict = db['Announcements']
            uhc_dict = db['UHC']

        except:
            print("Error in retrieving data from forumdb.")

        # if len(session_username) == 0:
        #     redirect(url_for('login')
        # else:

        if create_forum_post_form.category.data == 'Pinned Posts':
            post = ForumPinnedPostsCounter()
            post.set_forum_pinned_post_id()
            post.set_username(create_forum_post_form.username.data)
            post.set_category(create_forum_post_form.category.data)
            post.set_post_subject(create_forum_post_form.post_subject.data)
            post.set_post_message(create_forum_post_form.post_message.data)
            post.set_date_time(post.get_date_time())
            pinned_posts_dict[post.get_forum_pinned_post_id()] = post
            db['PinnedPosts'] = pinned_posts_dict
            return redirect(url_for('forum_pinned_posts'))

        elif create_forum_post_form.category.data == 'Announcements':
            post = ForumAnnoucementsPostCounter()
            post.set_forum_announcements_post_id()
            post.set_username(create_forum_post_form.username.data)
            post.set_category(create_forum_post_form.category.data)
            post.set_post_subject(create_forum_post_form.post_subject.data)
            post.set_post_message(create_forum_post_form.post_message.data)
            post.set_date_time(post.get_date_time())
            announcements_dict[post.get_forum_announcements_post_id()] = post
            db['Announcements'] = announcements_dict
            return redirect(url_for('forum_announcements_posts'))

        elif create_forum_post_form.category.data == 'Unified Help Community':
            post = ForumUHCPostCounter()
            post.set_forum_uhc_post_id()
            post.set_username(create_forum_post_form.username.data)
            post.set_category(create_forum_post_form.category.data)
            post.set_post_subject(create_forum_post_form.post_subject.data)
            post.set_post_message(create_forum_post_form.post_message.data)
            post.set_date_time(post.get_date_time())
            uhc_dict[post.get_forum_uhc_post_id()] = post
            db['UHC'] = uhc_dict
            return redirect(url_for('forum_uhc_posts'))
        db.close()
    return render_template('customer/CS/createForumPost.html', form=create_forum_post_form)


# ------------ Report Generation ------------ #

@app.route("/dashboard")
def dashboard():
    return render_template('staff/RG/dashboard.html')


@app.route("/cost_analysis")
def cost_analysis():
    # cc_dict = {}
    # cap_dict = {}
    # fre_dict = {}
    # isc_dict = {}
    # ac_dict = {}
    # uc_dict = {}
    # costs_db = shelve.open('costs.db', 'c')
    #
    # try:
    #     cc_dict = costs_db['Campaign Costs']
    #     cap_dict = costs_db['CAP Costs']
    #     fre_dict = costs_db['FRE Costs']
    #     isc_dict = costs_db['ISC Costs']
    #     ac_dict = costs_db['AC Costs']
    #     uc_dict = costs_db['UC Costs']
    #
    # except:
    #     print("error in retrieving data from costs.db")
    #
    # with open("Staff_RG_costs.csv", 'r') as costs_data_file:
    #     reader = csv.DictReader(costs_data_file)
    #     for row in reader:
    #         # ------ Creating and Storing Campaign Costs Objects ----- #
    #         ccON = Data(row['Month'], row['Year'], 'Campaign Costs: Online', row['Campaign Costs:Online'])
    #         cc_dict[ccON.get_data_id()] = ccON
    #
    #         ccOFF = Data(row['Month'], row['Year'], 'Campaign Costs: Offline', row['Campaign Costs: Offline'])
    #         cc_dict[ccOFF.get_data_id()] = ccOFF
    #         costs_db['Campaign Costs'] = cc_dict
    #
    #         # ------ Creating and Storing ISC Objects ----- #
    #         ISC = Data(row['Month'], row['Year'], 'Inventory Storage Costs', row['Inventory Storage Costs'])
    #         isc_dict[ISC.get_data_id()] = ISC
    #         costs_db['ISC Costs'] = isc_dict
    #
    #         # ------ Creating and Storing CAP Objects ----- #
    #         CAP_supplies = Data(row['Month'], row['Year'], 'Charitable Programs: Supplies', row['Charitable Programs: Supplies'])
    #         cap_dict[CAP_supplies.get_data_id()] = CAP_supplies
    #
    #         CAP_manpower = Data(row['Month'], row['Year'], 'Charitable Programs: Manpower', row['Charitable Programs: Manpower'])
    #         cap_dict[CAP_manpower.get_data_id()] = CAP_manpower
    #
    #         CAP_vr = Data(row['Month'], row['Year'], 'Charitable Programs: Venue Rental', row['Charitable Programs: Venue Rental'])
    #         cap_dict[CAP_vr.get_data_id()] = CAP_vr
    #         costs_db['CAP Costs'] = cap_dict
    #
    #         # ------ Creating and Storing FRE Objects ----- #
    #         FRE_catering = Data(row['Month'], row['Year'], 'Fund-raising Expenses: Catering', row['Fund-raising Expenses: Catering'])
    #         fre_dict[FRE_catering.get_data_id()] = FRE_catering
    #
    #         FRE_vr = Data(row['Month'], row['Year'], 'Fund-raising Expenses: Venue Rental', row['Fund-raising Expenses: Venue Rental'])
    #         fre_dict[FRE_vr.get_data_id()] = FRE_vr
    #
    #         FRE_marketing = Data(row['Month'], row['Year'], 'Fund Raising Expenses: Marketing', row['Fund Raising Expenses: Marketing'])
    #         fre_dict[FRE_marketing.get_data_id()] = FRE_marketing
    #         costs_db['FRE Costs'] = fre_dict
    #
    #         # ------ Creating and Storing AC Objects ----- #
    #         AC_ES = Data(row['Month'], row['Year'], 'Administration Costs: Employee Salaries', row['Administration Costs: Employee Salaries'])
    #         ac_dict[AC_ES.get_data_id()] = AC_ES
    #
    #         AC_ET = Data(row['Month'], row['Year'], 'Administration Costs: Employee Training', row['Administration Costs: Employee Training'])
    #         ac_dict[AC_ET.get_data_id()] = AC_ET
    #
    #         AC_OS = Data(row['Month'], row['Year'], 'Administration Costs: Office Supplies', row['Administration Costs: Office Supplies'])
    #         ac_dict[AC_OS.get_data_id()] = AC_OS
    #
    #         AC_LF = Data(row['Month'], row['Year'], 'Administration Costs: Legal Fees', row['Administration Costs: Legal Fees'])
    #         ac_dict[AC_LF.get_data_id()] = AC_LF
    #         costs_db['AC Costs'] = ac_dict
    #
    #         # ------ Creating and Storing UC Objects ----- #
    #         UC_water = Data(row['Month'], row['Year'], 'Utilities Costs: Water', row['Utilities Costs: Water'])
    #         uc_dict[UC_water.get_data_id()] = UC_water
    #
    #         UC_electricity = Data(row['Month'], row['Year'], 'Utilities Costs: Electricity', row['Utilities Costs: Electricity'])
    #         uc_dict[UC_electricity.get_data_id()] = UC_electricity
    #         costs_db['UC Costs'] = uc_dict
    #
    # costs_db.close()
    #
    # # Retrieve Costs for each category and sub-category
    # costs_db = shelve.open('costs.db', 'r')
    # cc_dict = costs_db['Campaign Costs']
    # cap_dict = costs_db['CAP Costs']
    # fre_dict = costs_db['FRE Costs']
    # isc_dict = costs_db['ISC Costs']
    # ac_dict = costs_db['AC Costs']
    # uc_dict = costs_db['UC Costs']
    # costs_db.close()
    #


    return render_template('staff/RG/cost_analysis.html')


@app.route("/upload_insert_data")
def upload_insert_data():
    return render_template('staff/RG/upload_insert_data.html')


@app.route("/detailed_analysis")
def detailed_analysis():
    return render_template('staff/RG/detailed_analysis.html')


@app.route("/upload_dataForm")
def upload_dataForm():
    return render_template('staff/RG/upload_dataForm.html')


@app.route("/manual_insertForm")
def manual_insertForm():
    manual_upload_form = ManualUploadForm(request.form)
    if request.method == 'POST' and manual_upload_form.validate():
        cost_dict = {}
        db = shelve.open('storage.db', 'r')

        try:
            cost_dict = db['cost']
        except:
            print("Error in retrieving Users from storage.db.")

        cost_object = Data(manual_upload_form.month, manual_upload_form.data_field, manual_upload_form.data_value)
        cost_dict["yes"] = cost_object
        db['cost'] = cost_dict

        # Test codes
        cost_dict = db['cost']
        user = cost_dict["yes"]
        db.close()

    return render_template('staff/RG/manual_insertForm.html', form=manual_upload_form)


@app.route("/file_uploadForm")
def file_upload():
    return render_template("staff/RG/file_uploadForm.html")


@app.route("/uploader", methods=["GET", "POST"])
def file_uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save((f.filename))
        return 'file uploaded successfully'


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('staff/error404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
