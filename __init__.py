# Imports
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
# from flask_login import login_required, LoginManager
import shelve

# Donation Imports
from donateMoney import donateMoney
from donateItem import donateItem
from Donate import DonateMoney, DonateItem
import os

# Customer Support Imports
from ForumForm import createForumPost, updateForumPost, staff_createForumPost, ForumPostReply
from Forum import ForumPost, ForumPinnedPostsCounter, ForumUHCPostCounter

# Account Management Imports
from Forms import CreateUserForm
from User import User, Staff
from datetime import timedelta, datetime

# Report Generation Imports
from Staff_RG_manual_upload import ManualUploadForm
import csv
import datetime
from Staff_RG_costs import Data, CampaignCosts, ISC, CapCosts, FreCosts, AdminCosts, UtilitiesCosts, Donations
from Staff_RG_update_history import History
import random
from werkzeug.utils import secure_filename

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
@app.route('/donate/money/login', methods=['GET', 'POST'])
def donate_money_login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        b = users_dict[key]
        if b.get_username() == create_login_form.username.data and b.get_password() == create_login_form.password.data:
            session["username"] = b.get_username()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            return redirect(url_for('donate_Money'))

    return render_template('customer/AM/login.html')


@app.route('/donate/item/login', methods=['GET', 'POST'])
def donate_item_login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        b = users_dict[key]
        if b.get_username() == create_login_form.username.data and b.get_password() == create_login_form.password.data:
            session["username"] = b.get_username()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            return redirect(url_for('donate_Item'))

    return render_template('customer/AM/login.html')


@app.route('/donate/history/login', methods=['GET', 'POST'])
def donate_history_login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        b = users_dict[key]
        if b.get_username() == create_login_form.username.data and b.get_password() == create_login_form.password.data:
            session["username"] = b.get_username()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            return redirect(url_for('donateHistory'))

    return render_template('customer/AM/login.html')


@app.route("/donate")
def donate():
    return render_template('customer/TP/Donate.html')


@app.route("/donate/history")
def donateHistory():
    try:
        SID = session["username"]
    except:
        return redirect(url_for('donate_history_login'))
    else:
        # Displaying Donation History
        donorsMID_dict = {}
        donorsIID_dict = {}
        try:
            db = shelve.open("donorChoices", "r")

            # Display if only Money donations are created and Items are empty
            if "Money" in db and "Items" not in db:
                # Money History
                donorsMID_dict = db["Money"]
                useridsM = [*donorsMID_dict]
                donorsMID_list = []

                if SID in useridsM:
                    donorsList = donorsMID_dict[SID]
                    for i in range(len(donorsList)):
                        donorMID = donorsList[i]
                        donorsMID_list.append(donorMID)

                return render_template('customer/TP/donationHistory.html', donorsIID_list='',
                                       donorsMID_list=donorsMID_list)

            # Display if only Item donations are created and Money is empty
            if "Money" not in db and "Items" in db:
                # Item History
                donorsIID_dict = db["Items"]
                userids = [*donorsIID_dict]
                donorsIID_list = []

                if SID in userids:
                    donorsList = donorsIID_dict[SID]
                    for i in range(len(donorsList)):
                        donorIID = donorsList[i]
                        donorsIID_list.append(donorIID)
                        # print(donorsIID_list)

                return render_template('customer/TP/donationHistory.html', donorsIID_list=donorsIID_list,
                                       donorsMID_list='')

            # Display once both item and money donations has been made
            if "Money" in db and "Items" in db:
                # Money History
                donorsMID_dict = db["Money"]
                useridsM = [*donorsMID_dict]
                donorsMID_list = []

                if SID in useridsM:
                    donorsList = donorsMID_dict[SID]
                    for i in range(len(donorsList)):
                        donorMID = donorsList[i]
                        donorsMID_list.append(donorMID)

                # Item History
                donorsIID_dict = db["Items"]
                useridsI = [*donorsIID_dict]
                donorsIID_list = []

                if SID in useridsI:
                    donorsList = donorsIID_dict[SID]
                    for i in range(len(donorsList)):
                        donorIID = donorsList[i]
                        donorsIID_list.append(donorIID)

                return render_template('customer/TP/donationHistory.html', donorsIID_list=donorsIID_list,
                                       donorsMID_list=donorsMID_list)

            db.close()

        except:
            return render_template('customer/TP/donationHistoryEmpty.html')

    return render_template('customer/TP/donationHistoryEmpty.html')


@app.route("/donate/details")
def donateDetails():
    return render_template('customer/TP/donateDetails.html')


@app.route("/donate/details/money", methods=['GET', 'POST'])
def donate_Money():
    try:
        SID = session["username"]
    except:
        return redirect(url_for('donate_money_login'))
    else:
        SID = session["username"]
        # Monetary Donations
        donate_money = donateMoney(request.form)
        if request.method == "POST" and donate_money.validate():
            donor_moneychoices = {}
            donationinfoM = []
            donationinfoMNest = []
            donorIDnInfo = {}

            dbMC = shelve.open("donorChoices", "c")

            try:
                donor_moneychoices = dbMC["Money"]

                userids = [*donor_moneychoices]
                print(userids)
                print(SID)
                if SID in userids:
                    donationinfoM.append(donor_moneychoices[SID])

                for x in donationinfoM:
                    for y in x:
                        donationinfoMNest.append(y)

            except:
                print("Error in retrieving Donors MC from donorMoneyChoices")

            now = datetime.datetime.now()

            donor = DonateMoney(donate_money.donateToWho.data, donate_money.moneyAmount.data,
                                donate_money.cardInfo_Name.data, donate_money.cardInfo_Number.data,
                                donate_money.cardInfo_CVV.data, donate_money.cardInfo_DateExpiry.data,
                                donate_money.cardInfo_YearExpiry.data, now)
            # Setting the money ID counter
            donoCounter = []
            if "MoneyCounter" not in dbMC:
                dbMC["MoneyCounter"] = donoCounter

            donoCounter = dbMC["MoneyCounter"]
            if len(donoCounter) == 0:
                moneyID = "M1"
            else:
                donateitemid_counter = donoCounter[-1]
                x = donateitemid_counter.split("M")
                num = int(x[1])
                num += 1
                moneyID = "M" + str(num)
            donoCounter.append(moneyID)
            dbMC["MoneyCounter"] = donoCounter

            donor.set_moneyID(moneyID)

            # Setting the donation status "pending" or "confirmed"
            if request.form.get('Cancel') == 'Cancel':
                donor.set_status("Pending")
            if request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")
                donate_amount = donor.get_money_amount()
                dbMC['TotalMAmount'] = donate_amount

            # Storing shelve as {donor ID: [donation info1, donation info2]}
            donationinfoMNest.append(donor)
            donor_moneychoices[SID] = donationinfoMNest

            dbMC["Money"] = donor_moneychoices

            dbMC.close()

            return redirect(url_for('donateHistory'))

        return render_template('customer/TP/donateMoney.html', form=donate_money)


app.config["Item_Donations"] = "static/customer/img/Idonation"
app.config["Allowed_Images_Type"] = ["PNG", "JPG", "JPEG"]


@app.route("/donate/details/item", methods=['GET', 'POST'])
def donate_Item():
    try:
        SID = session["username"]
    except:
        return redirect(url_for('donate_item_login'))
    else:
        SID = session["username"]
        # Item Donations
        donate_item = donateItem(request.form)
        if request.method == "POST" and donate_item.validate():
            donor_itemchoices = {}
            donationinfoI = []
            donationinfoINest = []
            donorIDnInfo = {}

            dbIM = shelve.open("donorChoices", "c")

            try:
                donor_itemchoices = dbIM["Items"]
                print(donor_itemchoices)

                userids = [*donor_itemchoices]
                print(userids)
                print(SID)
                # If user has made a donation before
                if SID in userids:
                    donationinfoI.append(donor_itemchoices[SID])

                for x in donationinfoI:
                    for y in x:
                        donationinfoINest.append(y)

            except:
                print("Error in retrieving Donors IM from donorChoices")

            now = datetime.datetime.now()

            donor = DonateItem(donate_item.donateToWho.data, donate_item.itemType.data, donate_item.itemName.data,
                               donate_item.itemWeight.data, donate_item.itemHeight.data, donate_item.itemLength.data,
                               donate_item.itemWidth.data, donate_item.collectionType.data,
                               donate_item.collectionDate.data, donate_item.collectionMonth.data,
                               donate_item.collectionTime.data, donate_item.pickupAddress1.data,
                               donate_item.pickupAddress2.data, donate_item.pickupAddress3.data,
                               donate_item.pickupPostalCode.data, now)

            # Setting Item Donation ID
            donoCounter = []
            if "ItemCounter" not in dbIM:
                dbIM["ItemCounter"] = donoCounter

            donoCounter = dbIM["ItemCounter"]
            if len(donoCounter) == 0:
                itemID = "I1"
            else:
                donateitemid_counter = donoCounter[-1]
                x = donateitemid_counter.split("I")
                num = int(x[1])
                num += 1
                itemID = "I" + str(num)
            donoCounter.append(itemID)
            dbIM["ItemCounter"] = donoCounter

            donor.set_itemID(itemID)

            # Upload image
            if request.files:
                image = request.files['image']

                donor.set_item_image(image.filename)
                image.save(os.path.join(app.config["Item_Donations"], image.filename))

            # Set Username to object
            donor.set_username(SID)

            # Set Email to object
            useremail = session["email"]
            donor.set_email(useremail)

            # Set Phone Number to object
            userphonenumber = session["contact"]
            donor.set_phonenumber(userphonenumber)

            # Setting the collection status (for staff side)
            donor.set_collection_status("Pending")

            # setting the donation status "pending" or "confirmed"
            if request.form.get('Cancel') == 'Cancel':
                donor.set_status("Pending")
            if request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")

            # Storing shelve as {donor ID: [donation info1, donation info2]}
            donationinfoINest.append(donor)
            donor_itemchoices[SID] = donationinfoINest

            dbIM["Items"] = donor_itemchoices

            dbIM.close()

            return redirect(url_for('donateHistory'))

        return render_template('customer/TP/donateItem.html', form=donate_item)


@app.route("/donate/details/confirmation/<string:id>", methods=['GET', 'POST'])
def donate_Confirmation(id):
    SID = session["username"]
    if request.method == 'POST':
        donation_dict = {}

        db = shelve.open('donorChoices', 'w')
        if id[0] == "M":
            donation_dict = db['Money']
            donoinfoList = donation_dict[SID]
            updatedonoinfo = ""

            for i in range(len(donoinfoList)):
                if donoinfoList[i].get_moneyID() == id:
                    updatedonoinfo = donoinfoList[i]

            donor = updatedonoinfo

            # Change status with respect to choice
            if request.form.get('Delete') == 'Delete':
                donor.set_status("Archive")

            elif request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")

            db["Money"] = donation_dict

        elif id[0] == "I":
            donation_dict = db['Items']
            donoinfoList = donation_dict[SID]
            updatedonoinfo = ""

            for i in range(len(donoinfoList)):
                if donoinfoList[i].get_itemID() == id:
                    updatedonoinfo = donoinfoList[i]

            donor = updatedonoinfo

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
    SID = session["username"]
    update_donate_item = donateItem(request.form)
    if request.method == 'POST':
        donors_dict = {}

        dbUP = shelve.open('donorChoices', 'w')
        donors_dict = dbUP['Items']
        donoinfoList = donors_dict[SID]
        updatedonoinfo = ""

        for i in range(len(donoinfoList)):
            if donoinfoList[i].get_itemID() == id:
                updatedonoinfo = donoinfoList[i]

        donor = updatedonoinfo

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
        donoinfoList = donors_dict[SID]
        updatedonoinfo = ""

        for i in range(len(donoinfoList)):
            if donoinfoList[i].get_itemID() == id:
                updatedonoinfo = donoinfoList[i]

        donor = updatedonoinfo

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

        dbUP.close()

        return render_template('customer/TP/donateItemUpdate.html', form=update_donate_item)


@app.route("/donate/gallery")
def donateGallery():
    # Displaying Donation History
    donorsIID_dict = {}
    try:
        db = shelve.open("donorChoices", "r")

        # If only Item donations are created and Money is empty
        if "Items" in db:
            # Item History
            donorsIID_dict = db["Items"]
            donorsIID_list = []
            unnested_donorsIID_list = []

            # Getting list of all donor objects (donations created) and putting into 1 list
            for key in donorsIID_dict:
                donorinfo_list = donorsIID_dict[key]
                donorsIID_list.append(donorinfo_list)

            # Unnesting the list of donor objects (donations)
            for x in donorsIID_list:
                for y in x:
                    unnested_donorsIID_list.append(y)

            return render_template('customer/TP/donationGallery.html', donorsIID_list=unnested_donorsIID_list)

        db.close()
    except:
        return render_template('customer/TP/donationGalleryEmpty.html')

    return render_template('customer/TP/donationGalleryEmpty.html')


# Customer Support
# This app route is added so that when the user wants to post a forum post, the user needs to be logged in before they can post
@app.route('/forum/login', methods=['GET', 'POST'])
def forum_login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
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
            return redirect(url_for('create_forum_post'))

    return render_template('customer/AM/login.html')


# This app route is added so that when the user wants to upvote/downvote or make a reply to a post, the user needs to be logged in before they can do any of the activity mentioned
@app.route('/forum/login/redirect_to_pinned_post/<int:post_id>', methods=['GET', 'POST'])
def forum_login_redirect_to_pinned_post(post_id):
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
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
            return redirect(url_for('forum_pinned_posts_post', post_id=post_id))

    return render_template('customer/AM/login.html')


# This app route is added so that when the user wants to upvote/downvote or make a reply to a post, the user needs to be logged in before they can do any of the activity mentioned
@app.route('/forum/login/redirect_to_uhc_post/<int:post_id>', methods=['GET', 'POST'])
def forum_login_redirect_to_uhc_post(post_id):
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
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
            return redirect(url_for('forum_uhc_posts_post', post_id=post_id))

    return render_template('customer/AM/login.html')


@app.route("/forum")
def forum():
    pinned_posts_dict = {}
    uhc_dict = {}
    usersDB = {}
    usersDB = shelve.open('account', 'r')
    db = shelve.open('forumdb', 'c')
    users_dict = usersDB['Users']
    pinned_posts_dict = db['PinnedPosts']
    uhc_dict = db['UHC']
    db.close()

    usersList = []
    pinned_posts_list = []
    uhc_list = []

    for key in pinned_posts_dict:
        post = pinned_posts_dict.get(key)
        pinned_posts_list.append(post)
    for key in uhc_dict:
        post = uhc_dict.get(key)
        uhc_list.append(post)
    for key in users_dict:
        post = users_dict.get(key)
        usersList.append(post)
    usersDB.close()
    return render_template('customer/CS/Forum.html', pinned_posts_list=pinned_posts_list, uhc_list=uhc_list,
                           usersList=usersList)


@app.route("/forum/createforumpost", methods=['GET', 'POST'])
def create_forum_post():
    usersDB = {}
    usersDB = shelve.open('account', 'r')
    users_dict = usersDB['Users']

    usersList = []
    for key in users_dict:
        post = users_dict.get(key)
        usersList.append(post)

    try:
        session_username = session["username"]
    except:
        return redirect(url_for('forum_login'))
    else:
        create_forum_post_form = createForumPost(request.form)
        if request.method == 'POST':
            uhc_dict = {}
            pinned_post_dict = {}
            db = shelve.open('forumdb', 'c')

            try:
                uhc_dict = db['UHC']
                pinned_post_dict = db['PinnedPosts']
            except:
                print("Error in retrieving data from forumdb.")

            if create_forum_post_form.category.data == "Unified Help Community" or create_forum_post_form.category_staff.data == "Unified Help Community":
                post = ForumUHCPostCounter()
                post.set_post_id()
                post.set_username(session_username)
                post.set_upvote(0)
                post.set_category('Unified Help Community')
                post.set_post_subject(create_forum_post_form.post_subject.data)
                post.set_post_message(create_forum_post_form.post_message.data)
                post.set_date_time(post.get_date_time())
                uhc_dict[post.get_post_id()] = post
                db['UHC'] = uhc_dict
                db.close()
                return redirect(url_for('forum_uhc_posts'))
            elif create_forum_post_form.category_staff.data == "Pinned Posts":
                post = ForumPinnedPostsCounter()
                post.set_post_id()
                post.set_username(session_username)
                post.set_upvote(0)
                post.set_category("Pinned Posts")
                post.set_post_subject(create_forum_post_form.post_subject.data)
                post.set_post_message(create_forum_post_form.post_message.data)
                post.set_date_time(post.get_date_time())
                pinned_post_dict[post.get_post_id()] = post
                db['PinnedPosts'] = pinned_post_dict
                db.close()
                return redirect(url_for('forum_pinned_posts'))

    return render_template('customer/CS/createForumPost.html', form=create_forum_post_form,
                           session_username=session_username, usersList=usersList)


@app.route("/forum/pinned_posts")
def forum_pinned_posts():
    usersDB = {}
    pinned_posts_dict = {}
    db = shelve.open('forumdb', 'c')
    usersDB = shelve.open('account', 'r')
    users_dict = usersDB['Users']
    pinned_posts_dict = db['PinnedPosts']
    db.close()

    usersList = []
    pinned_posts_list = []
    for key in pinned_posts_dict:
        post = pinned_posts_dict.get(key)
        pinned_posts_list.append(post)
    lenOfPinnedPost = len(pinned_posts_list)
    category = pinned_posts_list[0].get_category()
    for key in users_dict:
        post = users_dict.get(key)
        usersList.append(post)
    return render_template('customer/CS/overview-forum-category.html', list=pinned_posts_list, usersList=usersList,
                           category=category, lenOfPinnedPost=lenOfPinnedPost)


# Specific Forum Post ID - UHC
@app.route("/forum/pinned_posts/<int:post_id>", methods=['GET', 'POST'])
def forum_pinned_posts_post(post_id):
    global pp_upvote_list, pp_downvote_list
    post_reply_retrieve_dict = {}
    user_dict = {}
    pinned_posts_dict = {}
    pp_upvote_dict = {}
    pp_downvote_dict = {}
    db = shelve.open('forumdb', 'c')
    pinned_posts_dict = db['PinnedPosts']
    pp_upvote_dict = db['PinnedPostUpvoteCount']
    pp_downvote_dict = db['PinnedPostDownvoteCount']
    userdb = shelve.open('account', 'r')
    user_dict = userdb['Users']
    pinned_posts_list = []
    user_list = []
    pp_upvote_list = []
    pp_downvote_list = []

    post = pinned_posts_dict.get(post_id)
    session['post_id'] = post_id
    pinned_posts_list.append(post)
    for key in user_dict:
        user = user_dict.get(key)
        user_list.append(user)
    userdb.close()

    if post_id in pp_upvote_dict.keys():
        pp_upvote_list = pp_upvote_dict[post_id]
    if post_id in pp_downvote_dict.keys():
        pp_downvote_list = pp_downvote_dict[post_id]

    # Retrieving Post Replies
    post_reply_retrieve_dict = db['PinnedPostsPostReply']
    post_reply_retrieve_list = []

    if post_id in post_reply_retrieve_dict:
        reply_dict = post_reply_retrieve_dict[post_id]
        for tag in reply_dict:
            reply = reply_dict.get(tag)
            post_reply_retrieve_list.append(reply)

    reply_post_form = ForumPostReply(request.form)
    if request.method == 'POST' and reply_post_form.validate():
        post_reply_dict = {}
        last_id = 0
        try:
            post_reply_dict = db['PinnedPostsPostReply']
        except:
            print("Error in retrieving data from forumdb.")
        id_dict = {}

        if post_id in post_reply_dict:
            id_dict = post_reply_dict[post_id]
            if len(id_dict.keys()) == 0:
                reply_id = 1
                post_reply_details = ForumPinnedPostsCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Pinned Posts")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['PinnedPostsPostReply'] = post_reply_dict
            else:
                for reply_id in id_dict.keys():
                    last_id = reply_id
                reply_id = last_id + 1
                post_reply_details = ForumPinnedPostsCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Pinned Posts")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['PinnedPostsPostReply'] = post_reply_dict
        else:
            if len(id_dict.keys()) == 0:
                reply_id = 1
                post_reply_details = ForumPinnedPostsCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Pinned Posts")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['PinnedPostsPostReply'] = post_reply_dict
            else:
                for reply_id in id_dict.keys():
                    last_id = reply_id
                reply_id = last_id + 1
                post_reply_details = ForumPinnedPostsCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Pinned Posts")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['PinnedPostsPostReply'] = post_reply_dict
        db.close()
        return redirect(url_for('forum_pinned_posts_post', post_id=post_id))

    post_id = post_id
    datetime_now = datetime.datetime.now().strftime("%d %b %Y, %X")
    return render_template('customer/CS/forum-post.html', post_list=pinned_posts_list,
                           user_list=user_list, form=reply_post_form, reply_list=post_reply_retrieve_list,
                           post_id=post_id, pp_upvote_list=pp_upvote_list, pp_downvote_list=pp_downvote_list,
                           datetime_now=datetime_now)


@app.route("/forum/pinned_posts/update/<int:post_id>", methods=['GET', 'POST'])
def forum_pinned_posts_post_update(post_id):
    forum_pinned_posts_form_update = createForumPost(request.form)
    if request.method == 'POST':
        pinned_posts_dict = {}
        db = shelve.open('forumdb', 'w')
        pinned_posts_dict = db['PinnedPosts']
        post = pinned_posts_dict.get(post_id)

        post.set_post_message(forum_pinned_posts_form_update.post_message.data)
        post.set_edited()
        db['PinnedPosts'] = pinned_posts_dict
        db.close()
        return redirect(url_for('forum_pinned_posts_post', post_id=post.get_post_id()))
    else:
        pinned_posts_dict = {}
        pinned_posts_list = []
        db = shelve.open('forumdb', 'r')
        pinned_posts_dict = db['PinnedPosts']
        db.close()

        post = pinned_posts_dict.get(post_id)
        pinned_posts_list.append(post)
        forum_pinned_posts_form_update.post_message.data = post.get_post_message()
        return render_template('customer/CS/forum-post_update.html', form=forum_pinned_posts_form_update,
                               list=pinned_posts_list)


@app.route('/forum/pinned_posts/delete/<int:post_id>', methods=['GET', 'POST'])
def forum_pinned_posts_post_delete(post_id):
    pinned_posts_dict = {}
    reply_dict = {}
    db = shelve.open('forumdb', 'w')
    pinned_posts_dict = db['PinnedPosts']

    pinned_posts_dict.pop(post_id)

    db['PinnedPosts'] = pinned_posts_dict

    reply_dict = db['PinnedPostsPostReply']
    if post_id in reply_dict:
        reply_dict.pop(post_id)
        db['PinnedPostsPostReply'] = reply_dict
    db.close()
    return redirect(url_for('forum_pinned_posts'))


@app.route("/forum/pinned_posts/delete/<int:post_id>/delete_reply/<int:reply_id>", methods=['GET', 'POST'])
def pinned_post_delete_reply(post_id, reply_id):
    reply_dict = {}
    db = shelve.open('forumdb', 'c')
    reply_dict = db['PinnedPostsPostReply']

    id_dict = {}

    if post_id in reply_dict:
        id_dict = reply_dict[post_id]
        if reply_id in id_dict:
            id_dict.pop(reply_id)

    reply_dict[post_id] = id_dict
    db['PinnedPostsPostReply'] = reply_dict
    db.close()
    return redirect(url_for('forum_pinned_posts_post', post_id=post_id))


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
    lenOfUHCPost = len(uhc_list)
    category = uhc_list[0].get_category()
    return render_template('customer/CS/overview-forum-category.html', list=uhc_list, category=category,
                           lenOfUHCPost=lenOfUHCPost)


@app.route("/forum/uhc/<int:post_id>", methods=['GET', 'POST'])
def forum_uhc_posts_post(post_id):
    post_reply_retrieve_dict = {}
    user_dict = {}
    uhc_dict = {}
    uhc_upvote_dict = {}
    uhc_downvote_dict = {}
    db = shelve.open('forumdb', 'c')
    uhc_dict = db['UHC']
    uhc_upvote_dict = db['UHCPostUpvoteCount']
    uhc_downvote_dict = db['UHCPostDownvoteCount']
    userdb = shelve.open('account', 'r')
    user_dict = userdb['Users']
    uhc_list = []
    user_list = []
    uhc_upvote_list = []
    uhc_downvote_list = []

    post = uhc_dict.get(post_id)
    uhc_list.append(post)
    for key in user_dict:
        user = user_dict.get(key)
        user_list.append(user)
    userdb.close()

    if post_id in uhc_upvote_dict.keys():
        uhc_upvote_list = uhc_upvote_dict[post_id]
    if post_id in uhc_downvote_dict.keys():
        uhc_downvote_list = uhc_downvote_dict[post_id]

    # Retrieving Post Replies
    post_reply_retrieve_dict = db['UHCPostsPostReply']
    post_reply_retrieve_list = []

    if post_id in post_reply_retrieve_dict:
        reply_dict = post_reply_retrieve_dict[post_id]
        for tag in reply_dict:
            reply = reply_dict.get(tag)
            post_reply_retrieve_list.append(reply)

    reply_post_form = ForumPostReply(request.form)
    if request.method == 'POST' and reply_post_form.validate():
        post_reply_dict = {}
        last_id = 0
        try:
            post_reply_dict = db['UHCPostsPostReply']
        except:
            print("Error in retrieving data from forumdb.")
        id_dict = {}

        if post_id in post_reply_dict:
            id_dict = post_reply_dict[post_id]
            if len(id_dict.keys()) == 0:
                reply_id = 1
                post_reply_details = ForumUHCPostCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Unified Help Community")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['UHCPostsPostReply'] = post_reply_dict
            else:
                for reply_id in id_dict.keys():
                    last_id = reply_id
                reply_id = last_id + 1
                post_reply_details = ForumUHCPostCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Unified Help Community")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['UHCPostsPostReply'] = post_reply_dict
        else:
            if len(id_dict.keys()) == 0:
                reply_id = 1
                post_reply_details = ForumUHCPostCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Unified Help Community")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['UHCPostsPostReply'] = post_reply_dict
            else:
                for reply_id in id_dict.keys():
                    last_id = reply_id
                reply_id = last_id + 1
                post_reply_details = ForumUHCPostCounter()
                post_reply_details.set_post_reply_id(reply_id)
                post_reply_details.set_date_time(datetime.datetime.now())
                post_reply_details.set_username(session['username'])
                post_reply_details.set_reply_category("Unified Help Community")
                post_reply_details.set_reply_message(reply_post_form.reply_message.data)
                id_dict[post_reply_details.get_post_reply_id()] = post_reply_details
                post_reply_dict[post_id] = id_dict
                db['UHCPostsPostReply'] = post_reply_dict
        db.close()
        return redirect(url_for('forum_uhc_posts_post', post_id=post_id))

    post_id = post_id
    datetime_now = datetime.datetime.now().strftime("%d %b %Y, %X")

    return render_template('customer/CS/forum-post.html', post_list=uhc_list,
                           user_list=user_list, form=reply_post_form, reply_list=post_reply_retrieve_list,
                           post_id=post_id, uhc_upvote_list=uhc_upvote_list, uhc_downvote_list=uhc_downvote_list,
                           datetime_now=datetime_now)


@app.route("/forum/uhc/update/<int:post_id>", methods=['GET', 'POST'])
def forum_uhc_post_update(post_id):
    forum_uhc_form_update = updateForumPost(request.form)
    if request.method == 'POST':
        uhc_dict = {}
        db = shelve.open('forumdb', 'w')
        uhc_dict = db['UHC']

        post = uhc_dict.get(post_id)
        post.set_post_message(forum_uhc_form_update.post_message.data)
        post.set_edited()
        db['UHC'] = uhc_dict
        db.close()
        return redirect(url_for('forum_uhc_posts_post', post_id=post.get_post_id()))
    else:
        uhc_dict = {}
        uhc_list = []
        db = shelve.open('forumdb', 'r')
        uhc_dict = db['UHC']
        db.close()

        post = uhc_dict.get(post_id)
        uhc_list.append(post)
        forum_uhc_form_update.post_message.data = post.get_post_message()
        return render_template('customer/CS/forum-post_update.html', form=forum_uhc_form_update,
                               list=uhc_list)


@app.route('/forum/uhc/delete/<int:post_id>', methods=['GET', 'POST'])
def forum_uhc_post_delete(post_id):
    uhc_dict = {}
    reply_dict = {}
    db = shelve.open('forumdb', 'w')
    uhc_dict = db['UHC']

    uhc_dict.pop(post_id)

    db['UHC'] = uhc_dict

    reply_dict = db['UHCPostsPostReply']
    if post_id in reply_dict:
        reply_dict.pop(post_id)
        db['UHCPostsPostReply'] = reply_dict
    db.close()
    return redirect(url_for('forum_uhc_posts'))


@app.route("/forum/uhc/delete/<int:post_id>/delete_reply/<int:reply_id>", methods=['GET', 'POST'])
def uhc_delete_reply(post_id, reply_id):
    reply_dict = {}
    db = shelve.open('forumdb', 'c')
    reply_dict = db['UHCPostsPostReply']

    id_dict = {}

    if post_id in reply_dict:
        id_dict = reply_dict[post_id]
        if reply_id in id_dict:
            id_dict.pop(reply_id)

    reply_dict[post_id] = id_dict
    db['UHCPostsPostReply'] = reply_dict
    db.close()

    return redirect(url_for('forum_uhc_posts_post', post_id=post_id))


@app.route("/upvote", methods=['POST'])
def upvote():
    upvote = request.form["upvote"]
    upvote = int(upvote)
    category = request.form["category"]
    vote = request.form["vote"]
    vote = int(vote)
    post_id = request.form["post_id"]
    post_id = int(post_id)
    db = shelve.open('forumdb', 'c')
    pinned_post_dict = {}
    uhc_dict = {}
    pinned_post_dict = db['PinnedPosts']
    uhc_dict = db['UHC']
    pp_upvote_dict = db['PinnedPostUpvoteCount']
    pp_downvote_dict = db['PinnedPostDownvoteCount']
    uhc_upvote_dict = db['UHCPostUpvoteCount']
    uhc_downvote_dict = db['UHCPostDownvoteCount']
    list = []
    if category == "1":
        if vote == 1:
            if post_id in pp_upvote_dict.keys():
                list = pp_upvote_dict[post_id]
                if session['username'] in list:
                    pass
                else:
                    list.append(session['username'])
                    pp_upvote_dict[post_id] = list
                    db['PinnedPostUpvoteCount'] = pp_upvote_dict
            else:
                list.append(session['username'])
                pp_upvote_dict[post_id] = list
                db['PinnedPostUpvoteCount'] = pp_upvote_dict

            if post_id in pp_downvote_dict.keys():
                list = pp_downvote_dict[post_id]
                if session['username'] in list:
                    list.remove(session['username'])
                    pp_downvote_dict[post_id] = list
                    db['PinnedPostDownvoteCount'] = pp_downvote_dict
            else:
                pass

        else:
            if post_id in pp_downvote_dict.keys():
                list = pp_downvote_dict[post_id]
                if session['username'] in list:
                    pass
                else:
                    list.append(session['username'])
                    pp_downvote_dict[post_id] = list
                    db['PinnedPostDownvoteCount'] = pp_downvote_dict
            else:
                list.append(session['username'])
                pp_downvote_dict[post_id] = list
                db['PinnedPostDownvoteCount'] = pp_downvote_dict

            if post_id in pp_upvote_dict.keys():
                list = pp_upvote_dict[post_id]
                if session['username'] in list:
                    list.remove(session['username'])
                    pp_upvote_dict[post_id] = list
                    db['PinnedPostUpvoteCount'] = pp_upvote_dict
            else:
                pass

        for post in pinned_post_dict:
            if post == post_id:
                pinned_post_dict[post].set_upvote(upvote)
        db['PinnedPosts'] = pinned_post_dict

        db.close()

        return redirect(url_for('forum_pinned_posts_post', post_id=post_id))

    elif category == "2":
        if vote == 1:
            if post_id in uhc_upvote_dict.keys():
                list = uhc_upvote_dict[post_id]
                if session['username'] in list:
                    pass
                else:
                    list.append(session['username'])
                    uhc_upvote_dict[post_id] = list
                    db['UHCPostUpvoteCount'] = uhc_upvote_dict
            else:
                list.append(session['username'])
                uhc_upvote_dict[post_id] = list
                db['UHCPostUpvoteCount'] = uhc_upvote_dict

            if post_id in uhc_downvote_dict.keys():
                list = uhc_downvote_dict[post_id]
                if session['username'] in list:
                    list.remove(session['username'])
                    uhc_downvote_dict[post_id] = list
                    db['UHCPostDownvoteCount'] = uhc_downvote_dict
            else:
                pass

        else:
            if post_id in uhc_downvote_dict.keys():
                list = uhc_downvote_dict[post_id]
                if session['username'] in list:
                    pass
                else:
                    list.append(session['username'])
                    uhc_downvote_dict[post_id] = list
                    db['UHCPostDownvoteCount'] = uhc_downvote_dict
            else:
                list.append(session['username'])
                uhc_downvote_dict[post_id] = list
                db['UHCPostDownvoteCount'] = uhc_downvote_dict

            if post_id in uhc_upvote_dict.keys():
                list = uhc_upvote_dict[post_id]
                if session['username'] in list:
                    list.remove(session['username'])
                    uhc_upvote_dict[post_id] = list
                    db['UHCPostUpvoteCount'] = uhc_upvote_dict
            else:
                pass

        for post in pinned_post_dict:
            if post == post_id:
                pinned_post_dict[post].set_upvote(upvote)
        db['PinnedPosts'] = pinned_post_dict

        for post in uhc_dict:
            if post == post_id:
                uhc_dict[post].set_upvote(upvote)
        db['UHC'] = uhc_dict
        db.close()

        return redirect(url_for('forum_uhc_posts_post', post_id=post_id))


# Account Management

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == "POST" and create_user_form.validate():
        users_dict = {}
        db = shelve.open('account', 'c')
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from account.")

        user = User(create_user_form.username.data, create_user_form.email.data, create_user_form.contact.data,
                    create_user_form.gender.data,
                    create_user_form.password.data, create_user_form.confirm_password.data)
        user.set_date_time(user.get_date_time())
        user.set_user_id()
        user.set_account_type()

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        session['user_created'] = user.get_username()

        return redirect(url_for('profile'))
    return render_template('customer/AM/CreateAccount.html', form=create_user_form)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    create_login_form = CreateUserForm(request.form)
    users_dict = {}
    db = shelve.open('account', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        b = users_dict[key]
        if b.get_username() == create_login_form.username.data and b.get_password() == create_login_form.password.data:
            session["userid"] = b.get_user_id()
            session["username"] = b.get_username()
            session["email"] = b.get_email()
            session["contact"] = b.get_contact()
            session["password"] = b.get_password()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            print(b.get_date_time())
            b.get_account_type()
            if b.get_account_type() == "Customer":
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('incoming_item'))
    return render_template('customer/AM/login.html')


# Customer Profile
@app.route('/profile')
def profile():
    if "username" in session:
        username = session["username"]
        email = session["email"]
        contact = session["contact"]
        password = session["password"]
        return render_template('customer/AM/profile.html', username=username, email=email, contact=contact,
                               password=password)
    else:
        return redirect(url_for('login'))


# Customer Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('contact', None)
    session.pop('password', None)
    return render_template('customer/index.html')


# Retrieve Customer Database
@app.route('/retrieveusers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('account', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('staff/AM/unlock_delete_acc.html', count=len(users_list), users_list=users_list)


# Update Customer Profile
@app.route('/updateProfile', methods=['GET', 'POST'])
def update_profile():
    update_profile_form = CreateUserForm(request.form)
    if request.method == "POST":
        users_dict = {}
        db = shelve.open('account', 'c')
        users_dict = db['Users']
        print(users_dict)
        print(users_dict.keys())

        user = users_dict.get(session["userid"])
        user.set_username(update_profile_form.username.data)
        user.set_email(update_profile_form.email.data)
        user.set_contact(update_profile_form.contact.data)
        user.set_password(update_profile_form.password.data)
        user.set_confirm_password(update_profile_form.confirm_password.data)

        db['Users'] = users_dict
        db.close()
        session["username"] = update_profile_form.username.data
        session["email"] = update_profile_form.email.data
        session["contact"] = update_profile_form.contact.data
        session.permanent = True

        session['user_updated'] = user.get_username()
        return redirect(url_for('profile'))
    else:
        users_dict = {}
        db = shelve.open('account', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(session["userid"])
        update_profile_form.username.data = user.get_username()
        update_profile_form.email.data = user.get_email()
        update_profile_form.contact.data = user.get_contact()
        update_profile_form.password.data = user.get_password()
        update_profile_form.confirm_password.data = user.get_confirm_password()
    return render_template('customer/AM/EditAccount.html', form=update_profile_form)


# Update Customer Database
@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('account', 'c')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_username(update_user_form.username.data)
        user.set_email(update_user_form.email.data)
        user.set_contact(update_user_form.contact.data)
        user.set_gender(update_user_form.gender.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_username()
        user.get_account_type()
        if user.get_account_type() == "Customer":
            return redirect(url_for('retrieve_users'))
        else:
            return redirect(url_for('retrieve_staff'))
    else:
        users_dict = {}
        db = shelve.open('account', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.username.data = user.get_username()
        update_user_form.email.data = user.get_email()
        update_user_form.contact.data = user.get_contact()
        update_user_form.gender.data = user.get_gender()
        update_user_form.password.data = user.get_password()
        update_user_form.confirm_password.data = user.get_confirm_password()

        return render_template('customer/AM/updateAccount.html', form=update_user_form)


# Delete Customer Database
@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('account', 'w')
    users_dict = db['Users']

    user = users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    session['user_deleted'] = user.get_username()

    return redirect(url_for('retrieve_users'))


# ================================================== Staff Side ================================================== #

# Not Used
@app.route('/staff_home', methods=['GET', 'POST'])
def staff_home():
    return render_template('staff/home.html')


# ------------ Account Management ------------ #

# Create Staff Account
@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_user_form = CreateUserForm(request.form)
    if request.method == "POST" and create_user_form.validate():
        users_dict = {}
        db = shelve.open('account', 'c')
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from account.")

        user = Staff(create_user_form.username.data, create_user_form.email.data, create_user_form.contact.data,
                     create_user_form.gender.data,
                     create_user_form.password.data, create_user_form.confirm_password.data)
        user.set_date_time(user.get_date_time())
        user.set_user_id()
        user.set_account_type()

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        session['user_created'] = user.get_username()

        return redirect(url_for('profile'))
    return render_template('customer/AM/CreateAccount.html', form=create_user_form)


# Create Staff Profile
@app.route("/staffprofile")
def staff_profile():
    if "username" in session:
        username = session["username"]
        email = session["email"]
        contact = session["contact"]
        return render_template('staff/AM/staff_profile.html', username=username, email=email, contact=contact)
    else:
        return redirect(url_for('login'))


# Staff Logout
@app.route('/logout')
def staff_logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('contact', None)
    return render_template('staff/home.html')


# Customer Database
@app.route("/account_management")
def account_management():
    return render_template('staff/AM/unlock_delete_acc.html')


# Retrieve Staff Database
@app.route("/retrievestaff")
def retrieve_staff():
    users_dict = {}
    db = shelve.open('account', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        staff = users_dict.get(key)
        users_list.append(staff)

    return render_template('staff/AM/retrievestaff.html', count=len(users_list), users_list=users_list)


# ------------ Transaction Processing ------------ #

@app.route("/incoming_items")
def incoming_item():
    donorsI_dict = {}
    try:
        db = shelve.open("donorChoices", "r")
        donorsIID_dict = db["Items"]
        donorsIID_list = []
        unnested_donorsIID_list = []

        # Getting list of all donor objects (donations created) and putting into 1 list
        for key in donorsIID_dict:
            donorinfo_list = donorsIID_dict[key]
            donorsIID_list.append(donorinfo_list)

        # Unnesting the list of donor objects (donations)
        for x in donorsIID_list:
            for y in x:
                unnested_donorsIID_list.append(y)

        db.close()

        return render_template('staff/TP/incoming_item.html', donorsIID_list=unnested_donorsIID_list)
    except:
        return render_template('staff/TP/incoming_item.html')


@app.route("/incoming_items/confirmation/<string:id>", methods=['GET', 'POST'])
def incoming_item_confirmation(id):
    if request.method == 'POST':
        donorsI_dict = {}
        db = shelve.open('donorChoices', 'w')

        donorsI_dict = db['Items']
        donorsIID_list = []
        unnested_donorsIID_list = []

        # Getting list of all donor objects (donations created) and putting into 1 list
        for key in donorsI_dict:
            donorinfo_list = donorsI_dict[key]
            donorsIID_list.append(donorinfo_list)

        # Unnesting the list of donor objects (donations)
        for x in donorsIID_list:
            for y in x:
                unnested_donorsIID_list.append(y)

        updatedonoinfo = ""

        for i in range(len(unnested_donorsIID_list)):
            if unnested_donorsIID_list[i].get_itemID() == id:
                updatedonoinfo = unnested_donorsIID_list[i]

        donor = updatedonoinfo

        # Setting the donation collection status to Confirmed
        if request.form.get('Confirm') == 'Confirm':
            donor.set_collection_status("Confirmed")

        db['Items'] = donorsI_dict

        db.close()

        return redirect(url_for('incoming_item'))


@app.route("/incoming_items/archive/<string:id>", methods=['GET', 'POST'])
def incoming_item_archive(id):
    SID = session["username"]
    if request.method == 'POST':
        donorsI_dict = {}
        db = shelve.open('donorChoices', 'w')

        donorsI_dict = db['Items']
        donorsIID_list = []
        unnested_donorsIID_list = []

        # Getting list of all donor objects (donations created) and putting into 1 list
        for key in donorsI_dict:
            donorinfo_list = donorsI_dict[key]
            donorsIID_list.append(donorinfo_list)

        # Unnesting the list of donor objects (donations)
        for x in donorsIID_list:
            for y in x:
                unnested_donorsIID_list.append(y)

        updatedonoinfo = ""

        for i in range(len(unnested_donorsIID_list)):
            if unnested_donorsIID_list[i].get_itemID() == id:
                updatedonoinfo = unnested_donorsIID_list[i]

        donor = updatedonoinfo

        # Setting the donation collection status to Archived
        if request.form.get('Archive') == 'Archive':
            donor.set_collection_status("Archive")

        db['Items'] = donorsI_dict

        db.close()

        return redirect(url_for('incoming_item'))


# ------------ Report Generation ------------ #

@app.route("/dashboard")
def dashboard():
    # ----------------Analytics Overview Cards-------------------#
    now = datetime.datetime.now()
    dbMC = shelve.open("donorChoices", "r")

    # Retrieving amount of money donated from transaction processing
    try:
        donor_moneychoices = dbMC["Money"]
    except:
        print("Error in retrieving Donors MC from donorMoneyChoices")

    donorsIID_list = []
    unnested_donorsIID_list = []

    # Puts all donation objects into a list (unnested_donorsIID_list). This is courtesy of lennon
    for key in donor_moneychoices:
        donorinfo_list = donor_moneychoices[key]
        donorsIID_list.append(donorinfo_list)

    for x in donorsIID_list:
        for y in x:
            unnested_donorsIID_list.append(y)

    overall_donations = 0
    total_year_donations = 0
    total_month_donations = 0
    for i in unnested_donorsIID_list:
        overall_donations += i.get_money_amount()
        # Gets total donation for the year
        if now.strftime("%Y") == i.get_year():
            total_year_donations += i.get_money_amount()
            # Gets total donation for the month
            if now.strftime("%b").upper() == i.get_month():
                total_month_donations += i.get_money_amount()

    # Retrieving number of items donated from transaction processing
    try:
        donor_itemchoices = dbMC["Items"]
    except:
        print("Error in retrieving Donors MC from donorMoneyChoices")

    donor_item_list = []
    unnested_item_list = []

    # Puts all donation objects into a list (unnested_donorsIID_list). This is courtesy of lennon
    for key in donor_itemchoices:
        donorinfo_list = donor_itemchoices[key]
        donor_item_list.append(donorinfo_list)

    for x in donor_item_list:
        for y in x:
            unnested_item_list.append(y)

    overall_items = 0
    total_year_items = 0
    total_month_items = 0
    for i in unnested_item_list:
        overall_items += 1
        if now.strftime("%Y") == i.get_create_year():
            total_year_items += 1
        if now.strftime("%b").upper() == i.get_create_month():
            total_month_items += 1

    dbMC.close()

    # ----------------------------Charts------------------------- #
    donations = {}
    try:
        costs_db = shelve.open('costs.db', 'w')
    except:
        return redirect(url_for("file_upload"))
    # Creating money donation object for online vs offline donation chart
    try:
        with open("Staff_RG_costs.csv", 'r') as costs_data_file:
            reader = csv.DictReader(costs_data_file)
            for row in reader:
                donation = Donations(row['Month'], row['Year'], total_month_donations,
                                     row['Offline Donations'])
                donations[donation.get_data_id()] = donation
                costs_db["donations"] = donations
    except FileNotFoundError:
        return redirect(url_for("file_upload"))
    costs_db.close()

    costs_db = shelve.open('costs.db', 'r')
    donations = costs_db["donations"]
    online_vs_offline = []
    On_vs_Off = {}
    for key in donations:
        cc = donations.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_online()), int(cc.get_offline()), int(cc.get_total())]
            online_vs_offline.append(data)
            # To display overall data on dashboard
            if cc.get_year() not in On_vs_Off.keys():
                On_vs_Off[cc.get_year()] = [cc.get_online(), cc.get_offline(), cc.get_total()]
            else:
                On_vs_Off[cc.get_year()][0] += cc.get_online()
                On_vs_Off[cc.get_year()][1] += cc.get_offline()
                On_vs_Off[cc.get_year()][2] += cc.get_total()
        elif now.year - 1 == int(cc.get_year()):
            if cc.get_year() not in On_vs_Off.keys():
                On_vs_Off[cc.get_year()] = [cc.get_online(), cc.get_offline(), cc.get_total()]
            else:
                On_vs_Off[cc.get_year()][0] += cc.get_online()
                On_vs_Off[cc.get_year()][1] += cc.get_offline()
                On_vs_Off[cc.get_year()][2] += cc.get_total()
        elif now.year - 2 == int(cc.get_year()):
            if cc.get_year() not in On_vs_Off.keys():
                On_vs_Off[cc.get_year()] = [cc.get_online(), cc.get_offline(), cc.get_total()]
            else:
                On_vs_Off[cc.get_year()][0] += cc.get_online()
                On_vs_Off[cc.get_year()][1] += cc.get_offline()
                On_vs_Off[cc.get_year()][2] += cc.get_total()
        elif now.year - 3 == int(cc.get_year()):
            if cc.get_year() not in On_vs_Off.keys():
                On_vs_Off[cc.get_year()] = [cc.get_online(), cc.get_offline(), cc.get_total()]
            else:
                On_vs_Off[cc.get_year()][0] += cc.get_online()
                On_vs_Off[cc.get_year()][1] += cc.get_offline()
                On_vs_Off[cc.get_year()][2] += cc.get_total()
        elif now.year - 4 == int(cc.get_year()):
            if cc.get_year() not in On_vs_Off.keys():
                On_vs_Off[cc.get_year()] = [cc.get_online(), cc.get_offline(), cc.get_total()]
            else:
                On_vs_Off[cc.get_year()][0] += cc.get_online()
                On_vs_Off[cc.get_year()][1] += cc.get_offline()
                On_vs_Off[cc.get_year()][2] += cc.get_total()
    costs_db.close()
    On_vs_Off_overall = []
    IDA_overall = []
    for key, value in On_vs_Off.items():
        data = [key]
        data.extend(value)
        On_vs_Off_overall.append(data)
        if int(key) == int(now.year):
            total_year_donations += value[2]
        overall_donations += value[2]

        IDA_data = [key, value[2]]
        IDA_overall.append(IDA_data)

    for i in online_vs_offline:
        if now.strftime("%b").upper() == i[0]:
            total_month_donations += i[3]

    totals = {}
    totals_overall = {}
    costs_db = shelve.open('costs.db', 'r')
    try:
        totals = costs_db["IDA_this_year"]
        totals_overall = costs_db["IDA_overall"]
    except:
        print("Error retrieving IDA_this_year and IDA_overall from costs.db shelve")

    IDA_this_year = []
    EI_this_year = []
    EI_this_month = 0
    for key, value in totals.items():
        data = [key, total_month_donations]
        data.extend(value)
        IDA_this_year.append(data)

        EI_data = [key, sum(value)]
        EI_this_year.append(EI_data)
        if key == now.strftime("%b").upper():
            EI_this_month = sum(value)

    EI_overall = []
    EI_this_year_overview = 0
    EI_overall_overview = 0
    for key, value in totals_overall.items():
        if now.year == int(key):
            EI_this_year_overview += sum(value)

        data = [key, sum(value)]
        EI_overall.append(data)
        EI_overall_overview += sum(value)
        for i in IDA_overall:
            if i[0] == key:
                i.extend(value)

    costs_db.close()
    return render_template('staff/RG/dashboard.html', total_month_donations=total_month_donations,
                           total_year_donations=total_year_donations,
                           overall_donations=overall_donations, total_month_items=total_month_items,
                           total_year_items=total_year_items, overall_items=overall_items,
                           IDA_this_year=IDA_this_year, IDA_overall=IDA_overall, EI_this_month=EI_this_month,
                           EI_this_year=EI_this_year, EI_overall=EI_overall,
                           EI_this_year_overview=EI_this_year_overview, EI_overall_overview=EI_overall_overview,
                           online_vs_offline=online_vs_offline, On_vs_Off_overall=On_vs_Off_overall)


@app.route("/cost_analysis")
def cost_analysis():
    cc_dict = {}
    cap_dict = {}
    fre_dict = {}
    isc_dict = {}
    ac_dict = {}
    uc_dict = {}
    costs_db = shelve.open('costs.db', 'c')

    try:
        cc_dict = costs_db['Campaign Costs']
        cap_dict = costs_db['CAP Costs']
        fre_dict = costs_db['FRE Costs']
        isc_dict = costs_db['ISC Costs']
        ac_dict = costs_db['AC Costs']
        uc_dict = costs_db['UC Costs']

    except:
        print("error in retrieving data from costs.db")
        try:
            with open("Staff_RG_costs.csv", 'r') as costs_data_file:
                reader = csv.DictReader(costs_data_file)
                for row in reader:
                    # ------ Creating and Storing Campaign Costs Objects ----- #
                    ccON = CampaignCosts(row['Month'], row['Year'], row['Campaign Costs: Online'],
                                         row['Campaign Costs: Offline'])
                    cc_dict[ccON.get_data_id()] = ccON
                    costs_db['Campaign Costs'] = cc_dict

                    # ------ Creating and Storing ISC Objects ----- #
                    isc = ISC(row['Month'], row['Year'], row['Inventory Storage Costs'])
                    isc_dict[isc.get_data_id()] = isc
                    costs_db['ISC Costs'] = isc_dict

                    # ------ Creating and Storing CAP Objects ----- #
                    CAP_supplies = CapCosts(row['Month'], row['Year'], row['Charitable Programs: Supplies'],
                                            row['Charitable Programs: Manpower'],
                                            row['Charitable Programs: Venue Rental'])
                    cap_dict[CAP_supplies.get_data_id()] = CAP_supplies
                    costs_db['CAP Costs'] = cap_dict

                    # ------ Creating and Storing FRE Objects ----- #
                    FRE_catering = FreCosts(row['Month'], row['Year'], row['Fund-raising Expenses: Catering'],
                                            row['Fund-raising Expenses: Venue Rental'],
                                            row['Fund Raising Expenses: Marketing'])
                    fre_dict[FRE_catering.get_data_id()] = FRE_catering
                    costs_db['FRE Costs'] = fre_dict

                    # ------ Creating and Storing AC Objects ----- #
                    AC_ES = AdminCosts(row['Month'], row['Year'], row['Administration Costs: Employee Salaries'],
                                       row['Administration Costs: Employee training'],
                                       row['Administration Costs: Office Supplies'],
                                       row['Administration Costs: Legal Fees'])
                    ac_dict[AC_ES.get_data_id()] = AC_ES
                    costs_db['AC Costs'] = ac_dict

                    # ------ Creating and Storing UC Objects ----- #
                    UC_water = UtilitiesCosts(row['Month'], row['Year'], row['Utilities Costs: Water'],
                                              row['Utilities Costs: Electricity'])
                    uc_dict[UC_water.get_data_id()] = UC_water
                    costs_db['UC Costs'] = uc_dict

        except FileNotFoundError:
            return redirect(url_for("file_upload"))
    costs_db.close()

    # Retrieve Costs from shelve and store in dictionary
    try:
        costs_db = shelve.open('costs.db', 'r')
        cc_dict = costs_db['Campaign Costs']
        cap_dict = costs_db['CAP Costs']
        fre_dict = costs_db['FRE Costs']
        isc_dict = costs_db['ISC Costs']
        ac_dict = costs_db['AC Costs']
        uc_dict = costs_db['UC Costs']
    except FileNotFoundError:
        print("Costs.db cannot be found.")
    except:
        print("Error retrieving data from costs.db")
    costs_db.close()

    now = datetime.datetime.now()

    totals = {}
    totals_overall = {}
    # --------------------- Retrieving and visualizing costs ------------------
    cc_chart_data_1 = []
    cc_chart_data_2 = []
    for key in cc_dict:
        cc = cc_dict.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_1.append(data)
            # To display this year data on  dashboard
            totals_list = [cc.get_total()]
            totals[cc.get_month()] = totals_list
            # To display overall data on dashboard
            if cc.get_year() not in totals_overall.keys():
                totals_overall[cc.get_year()] = [cc.get_total()]
            else:
                totals_overall[cc.get_year()][0] += cc.get_total()
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_2.append(data)
            if cc.get_year() not in totals_overall.keys():
                totals_overall[cc.get_year()] = [cc.get_total()]
            else:
                totals_overall[cc.get_year()][0] += cc.get_total()
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            if cc.get_year() not in totals_overall.keys():
                totals_overall[cc.get_year()] = [cc.get_total()]
            else:
                totals_overall[cc.get_year()][0] += cc.get_total()
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            if cc.get_year() not in totals_overall.keys():
                totals_overall[cc.get_year()] = [cc.get_total()]
            else:
                totals_overall[cc.get_year()][0] += cc.get_total()
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            if cc.get_year() not in totals_overall.keys():
                totals_overall[cc.get_year()] = [cc.get_total()]
            else:
                totals_overall[cc.get_year()][0] += cc.get_total()
    print(totals_overall)
    isc_chart_data_1 = []
    isc_chart_data_2 = []
    for key in isc_dict:
        cc = isc_dict.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_1.append(data)
            # To display this year data on  dashboard
            totals[cc.get_month()].append(cc.get_isc())
            # To display overall data on dashboard
            if len(totals_overall[cc.get_year()]) < 2:
                totals_overall[cc.get_year()].append(cc.get_isc())
            else:
                totals_overall[cc.get_year()][1] += int(cc.get_isc())
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_2.append(data)
            if len(totals_overall[cc.get_year()]) < 2:
                totals_overall[cc.get_year()].append(cc.get_isc())
            else:
                totals_overall[cc.get_year()][1] += int(cc.get_isc())
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            if len(totals_overall[cc.get_year()]) < 2:
                totals_overall[cc.get_year()].append(cc.get_isc())
            else:
                totals_overall[cc.get_year()][1] += int(cc.get_isc())
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            if len(totals_overall[cc.get_year()]) < 2:
                totals_overall[cc.get_year()].append(cc.get_isc())
            else:
                totals_overall[cc.get_year()][1] += int(cc.get_isc())
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            if len(totals_overall[cc.get_year()]) < 2:
                totals_overall[cc.get_year()].append(cc.get_isc())
            else:
                totals_overall[cc.get_year()][1] += int(cc.get_isc())
    print(totals_overall)
    cap_chart_data_1 = []
    cap_chart_data_2 = []
    for key in cap_dict:
        cc = cap_dict.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_1.append(data)
            # To display this year data on  dashboard
            totals[cc.get_month()].append(cc.get_total())
            # To display overall data on dashboard
            if len(totals_overall[cc.get_year()]) < 3:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][2] += (cc.get_total())
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_2.append(data)
            if len(totals_overall[cc.get_year()]) < 3:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][2] += (cc.get_total())
        elif now.year - 2 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 3:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][2] += (cc.get_total())
        elif now.year - 3 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 3:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][2] += (cc.get_total())
        elif now.year - 4 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 3:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][2] += (cc.get_total())

    fre_chart_data_1 = []
    fre_chart_data_2 = []
    for key in fre_dict:
        cc = fre_dict.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_1.append(data)
            # To display this year data on  dashboard
            totals[cc.get_month()].append(cc.get_total())
            # To display overall data on dashboard
            if len(totals_overall[cc.get_year()]) < 4:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][3] += (cc.get_total())
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_2.append(data)
            if len(totals_overall[cc.get_year()]) < 4:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][3] += (cc.get_total())
        elif now.year - 2 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 4:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][3] += (cc.get_total())
        elif now.year - 3 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 4:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][3] += (cc.get_total())
        elif now.year - 4 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 4:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][3] += (cc.get_total())

    ac_chart_data_1 = []
    ac_chart_data_2 = []
    for key in ac_dict:
        cc = ac_dict.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_1.append(data)
            # To display this year data on  dashboard
            totals[cc.get_month()].append(cc.get_total())
            # To display overall data on dashboard
            if len(totals_overall[cc.get_year()]) < 5:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][4] += (cc.get_total())
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_2.append(data)
            if len(totals_overall[cc.get_year()]) < 5:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][4] += (cc.get_total())
        elif now.year - 2 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 5:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][4] += (cc.get_total())
        elif now.year - 3 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 5:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][4] += (cc.get_total())
        elif now.year - 4 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 5:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][4] += (cc.get_total())

    uc_chart_data_1 = []
    uc_chart_data_2 = []
    for key in uc_dict:
        cc = uc_dict.get(key)
        if now.year == int(cc.get_year()):
            # To display costs on cost analysis page
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_1.append(data)
            # To display this year data on  dashboard
            totals[cc.get_month()].append(cc.get_total())
            # To display overall data on dashboard
            if len(totals_overall[cc.get_year()]) < 6:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][5] += (cc.get_total())
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_2.append(data)
            if len(totals_overall[cc.get_year()]) < 6:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][5] += (cc.get_total())
        elif now.year - 2 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 6:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][5] += (cc.get_total())
        elif now.year - 3 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 6:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][5] += (cc.get_total())
        elif now.year - 4 == int(cc.get_year()):
            if len(totals_overall[cc.get_year()]) < 6:
                totals_overall[cc.get_year()].append(cc.get_total())
            else:
                totals_overall[cc.get_year()][5] += (cc.get_total())

    costs_db = shelve.open('costs.db', 'w')
    try:
        costs_db["IDA_this_year"] = totals
        costs_db["IDA_overall"] = totals_overall
    except:
        print("Unable to write IDA_this_year and IDA_overall to costs.db")
    costs_db.close()

    costs_db = shelve.open('costs.db', 'r')
    try:
        totals_overall = costs_db["IDA_overall"]
    except:
        print("Unable to retrieve IDA_overall from costs.db")

    costs_db.close()

    cc_chart_data_3 = []
    isc_chart_data_3 = []
    cap_chart_data_3 = []
    fre_chart_data_3 = []
    ac_chart_data_3 = []
    uc_chart_data_3 = []
    reduced_costs = {}
    for key, value in totals_overall.items():
        CC_data = [key, value[0]]
        cc_chart_data_3.append(CC_data)

        ISC_data = [key, value[1]]
        isc_chart_data_3.append(ISC_data)

        CAP_data = [key, value[2]]
        cap_chart_data_3.append(CAP_data)

        FRE_data = [key, value[3]]
        fre_chart_data_3.append(FRE_data)

        AC_data = [key, value[4]]
        ac_chart_data_3.append(AC_data)

        UC_data = [key, value[5]]
        uc_chart_data_3.append(UC_data)

        # # # Top 5 reduced costs
        # if now.year == key:
        #     cc_current_year = value[0]
        #     isc_current_year = value[1]
        #     cap_current_year = value[2]
        #     fre_current_year = value[3]
        #     ac_current_year = value[4]
        #     uc_current_year = value[5]
        #
        # if now.year - 1 == key:
        #     reduced_costs["Campaign Costs"] = cc_current_year - value[0]
        #     reduced_costs["Inventory Storage Costs"] = isc_current_year - value[1]
        #     reduced_costs["Charitable Program Costs"] = cap_current_year - value[2]
        #     reduced_costs["Fund Raising Expenses"] = fre_current_year - value[3]
        #     reduced_costs["Administration Costs"] = ac_current_year - value[4]
        #     reduced_costs["Utilities Costs"] = uc_current_year - value[5]
        #
        #     sorted_tuples = sorted(reduced_costs.items(), key=lambda item: item[1])
        #     sorted_reduced_costs = {k: v for k, v in sorted_tuples}
        #     print(sorted_reduced_costs)

    return render_template('staff/RG/cost_analysis.html', cc_data=cc_chart_data_1, cc_data1=cc_chart_data_2,
                           cc_data2=cc_chart_data_3,
                           isc_data=isc_chart_data_1, isc_data1=isc_chart_data_2, isc_data2=isc_chart_data_3,
                           cap_data=cap_chart_data_1, cap_data1=cap_chart_data_2, cap_data2=cap_chart_data_3,
                           fre_data=fre_chart_data_1, fre_data1=fre_chart_data_2, fre_data2=fre_chart_data_3,
                           ac_data=ac_chart_data_1, ac_data1=ac_chart_data_2, ac_data2=ac_chart_data_3,
                           uc_data=uc_chart_data_1, uc_data1=uc_chart_data_2, uc_data2=uc_chart_data_3)


@app.route("/upload_insert_data")
def upload_insert_data():
    return render_template('staff/RG/upload_insert_data.html')


@app.route("/upload_dataForm")
def upload_dataForm():
    return render_template('staff/RG/upload_dataForm.html')


@app.route("/manual_insertForm", methods=['GET', 'POST'])
def manual_insertForm():
    global old_value
    global field
    global cc
    manual_upload_form = ManualUploadForm(request.form)
    if request.method == 'POST' and manual_upload_form.validate():
        now = datetime.datetime.now()
        now_time = now.strftime("%X")
        now_date = now.strftime("%x")
        cost_dict = {}
        try:
            db = shelve.open('costs.db', 'w')
        except:
            return redirect(url_for("file_upload"))

        # Update Campaign Costs
        if manual_upload_form.data_field.data == "Campaign Costs: Online" or manual_upload_form.data_field.data == "Campaign Costs: Offline":
            cost_dict = db["Campaign Costs"]
            field = manual_upload_form.data_field.data
            for key in cost_dict:
                cc = cost_dict.get(key)
                if (str(cc.get_year()) + str(
                        cc.get_month())) == manual_upload_form.year.data + manual_upload_form.month.data:
                    if field == "Campaign Costs: Online":
                        old_value = cc.get_online_costs()
                        cc.set_online_costs(manual_upload_form.data_value.data)
                    else:
                        old_value = cc.get_offline_costs()
                        cc.set_offline_costs(manual_upload_form.data_value.data)
                    break
            db["Campaign Costs"] = cost_dict

        # Update Inventory Storage Costs
        elif manual_upload_form.data_field.data == "Inventory Storage Costs":
            cost_dict = db["ISC Costs"]
            field = manual_upload_form.data_field.data
            for key in cost_dict:
                cc = cost_dict.get(key)
                if str(cc.get_year()) + str(
                        cc.get_month()) == manual_upload_form.year.data + manual_upload_form.month.data:
                    if field == "Inventory Storage Costs":
                        old_value = cc.get_isc()
                        cc.set_isc(manual_upload_form.data_value.data)
                    break
            db["ISC Costs"] = cost_dict

        # Update Charitable Programme Costs
        elif manual_upload_form.data_field.data == "Charitable Programs: Supplies" or manual_upload_form.data_field.data == "Charitable Programs: Manpower" or manual_upload_form.data_field.data == "Charitable Programs: Venue Rental":
            cost_dict = db["CAP Costs"]
            field = manual_upload_form.data_field.data
            for key in cost_dict:
                cc = cost_dict.get(key)
                if str(cc.get_year()) + str(
                        cc.get_month()) == manual_upload_form.year.data + manual_upload_form.month.data:
                    if field == "Charitable Programs: Supplies":
                        old_value = cc.get_supplies()
                        cc.set_supplies(manual_upload_form.data_value.data)
                    elif field == "Charitable Programs: Manpower":
                        old_value = cc.get_manpower()
                        cc.set_manpower(manual_upload_form.data_value.data)
                    elif field == "Charitable Programs: Venue Rental":
                        old_value = cc.get_vr()
                        cc.set_vr(manual_upload_form.data_value.data)
                    break
            db["CAP Costs"] = cost_dict

        # Update Fund Raising Cost
        elif manual_upload_form.data_field.data == "Fund-raising Expenses: Catering" or manual_upload_form.data_field.data == "Fund Raising Expenses: Marketing" or manual_upload_form.data_field.data == "Fund-raising Expenses: Venue Rental":
            cost_dict = db["FRE Costs"]
            field = manual_upload_form.data_field.data
            for key in cost_dict:
                cc = cost_dict.get(key)
                if str(cc.get_year()) + str(
                        cc.get_month()) == manual_upload_form.year.data + manual_upload_form.month.data:
                    if field == "Fund-raising Expenses: Catering":
                        old_value = cc.get_catering()
                        cc.set_catering(manual_upload_form.data_value.data)
                    elif field == "Fund Raising Expenses: Marketing":
                        old_value = cc.get_vr()
                        cc.set_vr(manual_upload_form.data_value.data)
                    elif field == "Fund-raising Expenses: Venue Rental":
                        old_value = cc.get_marketing()
                        cc.set_marketing(manual_upload_form.data_value.data)
                    break
            db["FRE Costs"] = cost_dict

        # Update Admin Costs
        elif manual_upload_form.data_field.data == "Administration Costs: Employee Salaries" or manual_upload_form.data_field.data == "Administration Costs: Employee training" or manual_upload_form.data_field.data == "Administration Costs: Office Supplies" or manual_upload_form.data_field.data == "Administration Costs: Legal Fees":
            cost_dict = db["AC Costs"]
            field = manual_upload_form.data_field.data
            for key in cost_dict:
                cc = cost_dict.get(key)
                if str(cc.get_year()) + str(
                        cc.get_month()) == manual_upload_form.year.data + manual_upload_form.month.data:
                    if field == "Administration Costs: Employee Salaries":
                        old_value = cc.get_emp_salary()
                        cc.set_emp_salary(manual_upload_form.data_value.data)
                    elif field == "Administration Costs: Employee training":
                        old_value = cc.get_emp_training()
                        cc.set_emp_training(manual_upload_form.data_value.data)
                    elif field == "Administration Costs: Office Supplies":
                        old_value = cc.get_office_supplies()
                        cc.set_office_supplies(manual_upload_form.data_value.data)
                    elif field == "Administration Costs: Legal Fees":
                        old_value = cc.get_legal_fees()
                        cc.set_legal_fees(manual_upload_form.data_value.data)
                    break
            db["AC Costs"] = cost_dict

        # Update Utility Costs
        elif manual_upload_form.data_field.data == "Utilities Costs: Water" or manual_upload_form.data_field.data == "Utilities Costs: Electricity":
            cost_dict = db["UC Costs"]
            field = manual_upload_form.data_field.data
            for key in cost_dict:
                cc = cost_dict.get(key)
                if str(cc.get_year()) + str(
                        cc.get_month()) == manual_upload_form.year.data + manual_upload_form.month.data:
                    if field == "Utilities Costs: Water":
                        old_value = cc.get_water()
                        cc.set_water(manual_upload_form.data_value.data)
                    else:
                        old_value = cc.get_electricity()
                        cc.set_electricity(manual_upload_form.data_value.data)
                    break
            db["UC Costs"] = cost_dict
        changes = History(field, cc.get_month(), cc.get_year(), old_value, manual_upload_form.data_value.data,
                          now_date, now_time, session["username"])
        db.close()

        changes_dict = {}
        db1 = shelve.open('Staff_RG_update_history.db', 'c')
        try:
            changes_dict = db1['history']
        except:
            print("Error in retrieving update history from Staff_RG_update_history.db")

        changes.set_change_id("U" + str(len(changes_dict) + 1))
        changes_dict[changes.get_change_id()] = changes
        db1['history'] = changes_dict
        return redirect(url_for('cost_analysis'))

    else:
        print("hi")

    return render_template('staff/RG/manual_insertForm.html', form=manual_upload_form)


@app.route("/update_history")
def update_history():
    changes_dict = {}
    try:
        db2 = shelve.open("Staff_RG_update_history.db", "r")
    except:
        return redirect(url_for("file_upload"))

    try:
        changes_dict = db2['history']
    except:
        print("Error in retrieving data from shelve.")

    changes_list = []
    for key in changes_dict:
        change = changes_dict.get(key)
        changes_list.append(change)

    return render_template("staff/RG/update_history.html", update_history=changes_list)


# Allowed file type for file upload
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/file_uploadForm", methods=["GET", "POST"])
def file_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join("Staff_RG_costs.csv"))
            return redirect(url_for('cost_analysis'))
    return render_template("staff/RG/file_uploadForm.html")


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('staff/error404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
