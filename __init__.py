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
from Forum import ForumPost, ForumPinnedPostsCounter, ForumAnnoucementsPostCounter, ForumUHCPostCounter

# Account Management Imports
from Forms import CreateUserForm, CreateStaffForm
from User import User
from Staff import Staff
from datetime import timedelta, datetime

# Report Generation Imports
from Staff_RG_manual_upload import ManualUploadForm
import csv
import datetime
from Staff_RG_costs import Data, CampaignCosts, ISC, CapCosts, FreCosts, AdminCosts, UtilitiesCosts
from Staff_RG_update_history import History
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
            return redirect(url_for('donate_Money'))

    return render_template('customer/AM/login.html')


@app.route('/donate/item/login', methods=['GET', 'POST'])
def donate_item_login():
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
            return redirect(url_for('donate_Item'))

    return render_template('customer/AM/login.html')


@app.route('/donate/history/login', methods=['GET', 'POST'])
def donate_history_login():
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

            # If only Money donations are created and Items are empty
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
                        # print(donorsMID_list)

                return render_template('customer/TP/donationHistory.html', donorsIID_list='',
                                       donorsMID_list=donorsMID_list)

            # If only Item donations are created and Money is empty
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

            # Once both item and money donations has been made
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
                        # print(donorsMID_list)

                # Item History
                donorsIID_dict = db["Items"]
                useridsI = [*donorsIID_dict]
                donorsIID_list = []

                if SID in useridsI:
                    donorsList = donorsIID_dict[SID]
                    for i in range(len(donorsList)):
                        donorIID = donorsList[i]
                        donorsIID_list.append(donorIID)
                        # print(donorsIID_list)

                # print(donorI_dID)
                # print("hi")
                return render_template('customer/TP/donationHistory.html', donorsIID_list=donorsIID_list,
                                       donorsMID_list=donorsMID_list)

            db.close()

        except:
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
            now_time = now.strftime("%X")
            now_date = now.strftime("%x")

            donor = DonateMoney(donate_money.donateToWho.data, donate_money.moneyAmount.data,
                                donate_money.cardInfo_Name.data,
                                donate_money.cardInfo_Number.data, donate_money.cardInfo_CVV.data,
                                donate_money.cardInfo_DateExpiry.data, donate_money.cardInfo_YearExpiry.data, now_date,
                                now_time)
            # donor.set_moneyID()
            # set the money ID counter
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

            # setting the donation status "pending" or "confirmed"
            if request.form.get('Cancel') == 'Cancel':
                donor.set_status("Pending")
            if request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")
                donate_amount = donor.get_money_amount()
                dbMC['TotalMAmount'] = donate_amount
            # print(donor.get_status())

            # {donor ID: [donation info1, donation info2]}
            donationinfoMNest.append(donor)
            donor_moneychoices[SID] = donationinfoMNest

            dbMC["Money"] = donor_moneychoices

            dbMC.close()

            return redirect(url_for('donateHistory'))

        return render_template('customer/TP/donateMoney.html', form=donate_money)


app.config["Item_Donations"] = "static/customer/img/Idonation"
app.config["Allowed_Images_Type"] = ["PNG", "JPG", "JPEG"]


def allowed_images(filename):
    if not "." in filename:
        return False

    file = filename.rsplit(".", 1)[1]

    if file.upper() in app.config["Allowed_Images_Type"]:
        return True
    else:
        return False


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
                    # list(donanationinfoI)
                    # donor_itemchoices.pop(donor_itemchoices[SID])

                # print(donationinfoI)
                for x in donationinfoI:
                    for y in x:
                        donationinfoINest.append(y)
                # print(donationinfoINest)

            except:
                print("Error in retrieving Donors IM from donorChoices")

            now = datetime.datetime.now()
            now_time = now.strftime("%X")
            now_date = now.strftime("%x")

            donor = DonateItem(donate_item.donateToWho.data, donate_item.itemType.data, donate_item.itemName.data,
                               donate_item.itemWeight.data, donate_item.itemHeight.data, donate_item.itemLength.data,
                               donate_item.itemWidth.data, donate_item.collectionType.data,
                               donate_item.collectionDate.data,
                               donate_item.collectionMonth.data, donate_item.collectionTime.data,
                               donate_item.pickupAddress1.data, donate_item.pickupAddress2.data,
                               donate_item.pickupAddress3.data, donate_item.pickupPostalCode.data, now_date, now_time)

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

                # if image.filename == " ":
                #     print("Image must have filename")
                #     return redirect(request.url)
                #
                # if not allowed_images(image.filename):
                #     print("That image type is not allowed")
                #     return redirect(request.url)

                donor.set_item_image(image.filename)
                image.save(os.path.join(app.config["Item_Donations"], image.filename))
                # return redirect(request.url)

            # Setting the collection status (for staff side)
            donor.set_collection_status("Pending")

            # setting the donation status "pending" or "confirmed"
            if request.form.get('Cancel') == 'Cancel':
                donor.set_status("Pending")
            if request.form.get('Confirm') == 'Confirm':
                donor.set_status("Confirmed")
            # print(donor.get_status())

            # {donor ID: [donation info1, donation info2]}
            # change donorIDnInfo to donor_itemchoices
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

        # donor = donors_dict.get(id)
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

        # donor = donors_dict.get(id)
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
    # TypeError: The view function did not return a valid response. The function either returned None or ended
    # without a return statement.

    # Displaying Donation History
    donorsIID_dict = {}
    try:
        db = shelve.open("donorChoices", "r")

        # If only Item donations are created and Money is empty
        if "Items" in db:
            # Item History
            donorsIID_dict = db["Items"]
            # useridsI = [*donorsIID_dict]
            donorsIID_list = []
            unnested_donorsIID_list = []

            for key in donorsIID_dict:
                donorinfo_list = donorsIID_dict[key]
                donorsIID_list.append(donorinfo_list)

            for x in donorsIID_list:
                for y in x:
                    unnested_donorsIID_list.append(y)

            return render_template('customer/TP/donationGallery.html', donorsIID_list=unnested_donorsIID_list)

        db.close()
    except:
        return render_template('customer/TP/donationGalleryEmpty.html')

    return render_template('customer/TP/donationGalleryEmpty.html')


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


ROWS_PER_PAGE = 10


@app.route("/forum/pinned_posts")
def forum_pinned_posts():
    # page = request.args.get('page', 1, type=int)
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
    global last_id
    pinned_posts_dict = {}
    user_dict = {}
    db = shelve.open('forumdb', 'c')
    pinned_posts_dict = db['PinnedPosts']
    userdb = shelve.open('account.db', 'r')
    user_dict = userdb['Users']
    pinned_posts_list = []
    user_list = []

    print(pinned_posts_dict)

    post = pinned_posts_dict.get(forum_pinned_posts_id)
    session['forum_pinned_post_id'] = forum_pinned_posts_id
    pinned_posts_list.append(post)
    for key in user_dict:
        user = user_dict.get(key)
        user_list.append(user)
    userdb.close()

    # Create forum post reply
    reply_post_form = ForumPostReply(request.form)
    if request.method == 'POST':
        post_reply_dict = {}

        try:
            post_reply_dict = db['PostReply']
        except:
            print("Error in retrieving data from forumdb.")



        replies_dict = {}
        post_reply_dict[forum_pinned_posts_id] = replies_dict
        if forum_pinned_posts_id in post_reply_dict:
            replies_dict = post_reply_dict[forum_pinned_posts_id] #{post_id:id_dict}
            reply_details = ForumPost()
            reply_datetime = reply_details.set_date_time(datetime.datetime.now().strftime("%d %b %Y, %H:%M"))
            reply_username = reply_details.set_username(session['username'])
            reply_message = reply_details.set_reply_message(reply_post_form.reply_message.data)


        print(post_reply_dict)
        replies_dict = post_reply_dict[forum_pinned_posts_id]
        for reply_id in replies_dict:
            last_id = reply_id
        reply_id = last_id + 1
        print(reply_id)
        replies_dict[reply_id] = [datetime.datetime.now().strftime("%d %b %Y, %H:%M"),session['username'],reply_post_form.reply_message.data]
        # post_reply_dict[forum_pinned_posts_id] = replies_dict

    db.close()

    return render_template('customer/CS/forum-post.html', post_list=pinned_posts_list,
                           user_list=user_list, form=reply_post_form)


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
        pinned_posts_list = []
        db = shelve.open('forumdb', 'r')
        pinned_posts_dict = db['PinnedPosts']
        db.close()

        post = pinned_posts_dict.get(forum_pinned_posts_id)
        pinned_posts_list.append(post)
        forum_pinned_posts_form_update.post_message.data = post.get_post_message()
        return render_template('customer/CS/forum-post_update.html', form=forum_pinned_posts_form_update,
                               list=pinned_posts_list)


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
    user_dict = {}
    db = shelve.open('forumdb', 'c')
    announcements_dict = db['Announcements']
    userdb = shelve.open('account.db', 'r')
    user_dict = userdb['Users']
    announcements_list = []
    user_list = []

    post = announcements_dict.get(forum_announcements_post_id)
    session['forum_announcements_post_id'] = forum_announcements_post_id
    announcements_list.append(post)
    for key in user_dict:
        user = user_dict.get(key)
        user_list.append(user)
    userdb.close()
    db.close()
    return render_template('customer/CS/forum-post.html', post_list=announcements_list, user_list=user_list)


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
        announcements_list = []
        db = shelve.open('forumdb', 'r')
        announcements_dict = db['Announcements']
        db.close()

        post = announcements_dict.get(forum_announcements_post_id)
        announcements_list.append(post)
        forum_announcements_form_update.post_message.data = post.get_post_message()
        return render_template('customer/CS/forum-post_update.html', form=forum_announcements_form_update,
                               list=announcements_list)


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
    userdb = shelve.open('account.db', 'r')
    user_dict = userdb['Users']
    uhc_list = []
    user_list = []

    post = uhc_dict.get(forum_uhc_post_id)
    session['forum_uhc_post_id'] = forum_uhc_post_id
    uhc_list.append(post)
    for key in user_dict:
        user = user_dict.get(key)
        user_list.append(user)
    userdb.close()

    db.close()

    return render_template('customer/CS/forum-post.html', post_list=uhc_list, user_list=user_list)


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
        uhc_list = []
        db = shelve.open('forumdb', 'r')
        uhc_dict = db['UHC']
        db.close()

        post = uhc_dict.get(forum_uhc_post_id)
        uhc_list.append(post)
        forum_uhc_form_update.post_message.data = post.get_post_message()
        return render_template('customer/CS/forum-post_update.html', form=forum_uhc_form_update,
                               list=uhc_list)


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
    if "username" in session:
        return redirect(url_for('home'))
    create_user_form = CreateUserForm(request.form)
    if request.method == "POST" and create_user_form.validate():
        users_dict = {}
        db = shelve.open('account.db', 'c')
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from account.db.")

        user = User(create_user_form.username.data, create_user_form.email.data, create_user_form.gender.data,
                    create_user_form.password.data, create_user_form.confirm_password.data)
        user.set_date_time(user.get_date_time())

        userCounter = []
        if "UserCounter" not in db:
            db["UserCounter"] = userCounter

        userCounter = db["UserCounter"]
        if len(userCounter) == 0:
            userID = 1
        else:
            userid_counter = userCounter[-1]
            userid_counter += 1
        userCounter.append(userid_counter)
        db["UserCounter"] = userCounter
        user.set_user_id(userid_counter)

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        session['user_created'] = user.get_username()

        return redirect(url_for('profile'))
    return render_template('customer/AM/CreateAccount.html', form=create_user_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for('home'))
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
            print(b.get_date_time())
            return redirect(url_for('profile'))

    return render_template('customer/AM/login.html')


@app.route('/profile')
def profile():
    if "username" in session:
        username = session["username"]
        email = session["email"]
        gender = session["gender"]
        return render_template('customer/AM/profile.html', username=username, email=email, gender=gender)
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

@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    if "username" in session:
        return redirect(url_for('staff_home'))
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db['Staff']
        except:
            print("Error in retrieving Staff from staff.db.")

        staff = Staff(create_staff_form.staff_username.data, create_staff_form.staff_email.data,
                      create_staff_form.staff_gender.data,
                      create_staff_form.staff_password.data, create_staff_form.staff_confirm_password.data)
        staff.set_date_time(staff.get_date_time())
        staff_dict[staff.get_staff_id()] = staff
        db['Staff'] = staff_dict

        db.close()

        session['staff_created'] = staff.get_username()

        return redirect(url_for('staff_profile'))
    return render_template('staff/AM/CreateStaffAccount.html', form=create_staff_form)


@app.route("/staff_profile")
def staff_profile():
    if "username" in session:
        username1 = session["username"]
        return render_template('staff/AM/staff_profile.html', username1=username1)
    update_staff_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'c')
        staff_dict = db['Staff']

        staff = staff_dict.get(id)
        staff.set_username(update_staff_form.staff_username.data)
        staff.set_email(update_staff_form.staff_email.data)
        staff.set_gender(update_staff_form.staff_gender.data)
        staff.set_password(update_staff_form.staff_password.data)

        db['Staff'] = staff_dict
        db.close()

        session['staff_updated'] = staff.get_username()

        # return redirect(url_for('retrieve'))
    else:
        return redirect(url_for('staff_login'))


@app.route("/staff_login", methods=['GET', 'POST'])
def staff_login():
    if "username" in session:
        return redirect(url_for('staff_home'))
    create_stafflogin_form = CreateStaffForm(request.form)
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    staff_list = []
    for key in staff_dict:
        a = staff_dict[key]
        if a.get_username() == create_stafflogin_form.staff_username.data and a.get_password() == create_stafflogin_form.staff_password.data:
            session["username"] = a.get_username()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=1)
            print(a.get_date_time())
            return redirect(url_for('staff_profile'))

    return render_template('staff/AM/stafflogin.html')


@app.route('/logout')
def staff_logout():
    session.pop('username', None)
    return render_template('staff/home.html')


@app.route("/account_management")
def account_management():
    return render_template('staff/AM/unlock_delete_acc.html')


@app.route("/retrievestaff")
def retrieve_staff():
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    staffs_list = []
    for key1 in staff_dict:
        staff = staff_dict.get(key1)
        staffs_list.append(staff)

    return render_template('staff/AM/unlock_delete_acc.html', count1=len(staffs_list), staffs_list=staffs_list)


@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    update_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'c')
        staff_dict = db['Staff']

        staff = staff_dict.get(id)
        staff.set_username(update_staff_form.staff_username.data)
        staff.set_email(update_staff_form.staff_email.data)
        staff.set_gender(update_staff_form.staff_gender.data)
        staff.set_password(update_staff_form.staff_password.data)

        db['Staff'] = staff_dict
        db.close()

        session['staff_updated'] = staff.get_username()

        return redirect(url_for('retrieve'))
    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        staff = staff_dict.get(id)
        update_staff_form.staff_username.data = staff.get_username()
        update_staff_form.staff_email.data = staff.get_email()
        update_staff_form.staff_gender.data = staff.get_gender()
        update_staff_form.staff_password.data = staff.get_password()
        update_staff_form.staff_confirm_password.data = staff.get_confirm_password()

        return render_template('staff/AM/updateAccount.html', form=update_staff_form)


@app.route('/delete_staff/<int:id>', methods=['POST'])
def delete_staff(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']

    staff = staff_dict.pop(id)

    db['Staff'] = staff_dict
    db.close()

    session['staff_deleted'] = staff.get_username()

    return redirect(url_for('retrieve_staff'))


# ------------ Transaction Processing ------------ #

@app.route("/incoming_items")
def incoming_item():
    # SID = session["username"]
    donorsI_dict = {}
    try:
        db = shelve.open("donorChoices", "r")
        donorsIID_dict = db["Items"]
        # useridsI = [*donorsIID_dict]
        donorsIID_list = []
        unnested_donorsIID_list = []

        for key in donorsIID_dict:
            donorinfo_list = donorsIID_dict[key]
            donorsIID_list.append(donorinfo_list)

        for x in donorsIID_list:
            for y in x:
                unnested_donorsIID_list.append(y)

        # if SID in useridsI:
        #     donorsList = donorsIID_dict[SID]
        #     for i in range(len(donorsList)):
        #         donorIID = donorsList[i]
        #         donorsIID_list.append(donorIID)
        return render_template('staff/TP/incoming_item.html', donorsIID_list=unnested_donorsIID_list)
    except:
        return render_template('staff/TP/incoming_item.html')


@app.route("/incoming_items/confirmation/<string:id>", methods=['GET', 'POST'])
def incoming_item_confirmation(id):
    SID = session["username"]
    if request.method == 'POST':
        donorsI_dict = {}
        db = shelve.open('donorChoices', 'w')

        donorsI_dict = db['Items']
        donoinfoList = donorsI_dict[SID]
        updatedonoinfo = ""

        for i in range(len(donoinfoList)):
            if donoinfoList[i].get_itemID() == id:
                updatedonoinfo = donoinfoList[i]

        donor = updatedonoinfo

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
        donoinfoList = donorsI_dict[SID]
        updatedonoinfo = ""

        for i in range(len(donoinfoList)):
            if donoinfoList[i].get_itemID() == id:
                updatedonoinfo = donoinfoList[i]

        donor = updatedonoinfo

        if request.form.get('Archive') == 'Archive':
            donor.set_collection_status("Archive")

        print(donor.get_collection_status())

        db['Items'] = donorsI_dict

        db.close()

        return redirect(url_for('incoming_item'))


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
    # Analytics Overview
    now = datetime.datetime.now()
    dbMC = shelve.open("donorChoices", "r")
    try:
        donor_moneychoices = dbMC["Money"]
    except:
        print("Error in retrieving Donors MC from donorMoneyChoices")

    donorsIID_dict = dbMC["Money"]
    donorsIID_list = []
    unnested_donorsIID_list = []

    for key in donorsIID_dict:
        donorinfo_list = donorsIID_dict[key]
        donorsIID_list.append(donorinfo_list)

    for x in donorsIID_list:
        for y in x:
            unnested_donorsIID_list.append(y)

    total_month = 0
    for i in unnested_donorsIID_list:
        if now.month == unnested_donorsIID_list[i].get_date().month():
            total_month += unnested_donorsIID_list[i].get_money_amount()

    dbMC.close()

    IDA_dict = {}
    On_vs_Off_dict = {}
    expenses_dict = {}
    db = shelve.open("dashboard.db", "c")

    try:
        IDA_dict = db['IDA']
        On_vs_off_dict = db['on_vs_off']

    except:
        print("Error retrieving values from shelve")

    costs_db = shelve.open('costs.db', 'r')
    cc_dict = costs_db['Campaign Costs']
    cap_dict = costs_db['CAP Costs']
    fre_dict = costs_db['FRE Costs']
    isc_dict = costs_db['ISC Costs']
    ac_dict = costs_db['AC Costs']
    uc_dict = costs_db['UC Costs']
    costs_db.close()

    now = datetime.datetime.now()

    return render_template('staff/RG/dashboard.html')


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
                                        row['Charitable Programs: Manpower'], row['Charitable Programs: Venue Rental'])
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
    costs_db.close()

    # Retrieve Costs from shelve and store in dictionary
    costs_db = shelve.open('costs.db', 'r')
    cc_dict = costs_db['Campaign Costs']
    cap_dict = costs_db['CAP Costs']
    fre_dict = costs_db['FRE Costs']
    isc_dict = costs_db['ISC Costs']
    ac_dict = costs_db['AC Costs']
    uc_dict = costs_db['UC Costs']
    costs_db.close()

    now = datetime.datetime.now()
    # For dashboard
    IDA_data = {}

    cc_chart_data_1 = []
    cc_chart_data_2 = []
    cc_chart_data_3 = []
    cc_chart_data_4 = []
    cc_chart_data_5 = []
    for key in cc_dict:
        cc = cc_dict.get(key)
        if now.year == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_1.append(data)
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_2.append(data)
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_3.append(data)
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_4.append(data)
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_online_costs()), int(cc.get_offline_costs()), int(cc.get_total())]
            cc_chart_data_5.append(data)

    isc_chart_data_1 = []
    isc_chart_data_2 = []
    isc_chart_data_3 = []
    isc_chart_data_4 = []
    isc_chart_data_5 = []
    for key in isc_dict:
        cc = isc_dict.get(key)
        if now.year == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_1.append(data)
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_2.append(data)
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_3.append(data)
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_4.append(data)
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_isc())]
            isc_chart_data_5.append(data)

    cap_chart_data_1 = []
    cap_chart_data_2 = []
    cap_chart_data_3 = []
    cap_chart_data_4 = []
    cap_chart_data_5 = []
    for key in cap_dict:
        cc = cap_dict.get(key)
        if now.year == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_1.append(data)
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_2.append(data)
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_3.append(data)
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_4.append(data)
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_supplies()), int(cc.get_manpower()), int(cc.get_vr()),
                    int(cc.get_total())]
            cap_chart_data_5.append(data)

    fre_chart_data_1 = []
    fre_chart_data_2 = []
    fre_chart_data_3 = []
    fre_chart_data_4 = []
    fre_chart_data_5 = []
    for key in fre_dict:
        cc = fre_dict.get(key)
        if now.year == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_1.append(data)
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_2.append(data)
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_3.append(data)
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_4.append(data)
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_catering()), int(cc.get_vr()), int(cc.get_marketing()),
                    int(cc.get_total())]
            fre_chart_data_5.append(data)

    ac_chart_data_1 = []
    ac_chart_data_2 = []
    ac_chart_data_3 = []
    ac_chart_data_4 = []
    ac_chart_data_5 = []
    for key in ac_dict:
        cc = ac_dict.get(key)
        if now.year == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_1.append(data)
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_2.append(data)
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_3.append(data)
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_4.append(data)
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_emp_salary()), int(cc.get_emp_training()), int(cc.get_office_supplies()),
                    int(cc.get_legal_fees()), int(cc.get_total())]
            ac_chart_data_5.append(data)

    uc_chart_data_1 = []
    uc_chart_data_2 = []
    uc_chart_data_3 = []
    uc_chart_data_4 = []
    uc_chart_data_5 = []
    for key in uc_dict:
        cc = uc_dict.get(key)
        if now.year == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_1.append(data)
        elif now.year - 1 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_2.append(data)
        elif now.year - 2 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_3.append(data)
        elif now.year - 3 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_4.append(data)
        elif now.year - 4 == int(cc.get_year()):
            data = [cc.get_month(), int(cc.get_water()), int(cc.get_electricity()), int(cc.get_total())]
            uc_chart_data_5.append(data)

    return render_template('staff/RG/cost_analysis.html', cc_data=cc_chart_data_1, cc_data1=cc_chart_data_2,
                           cc_data2=cc_chart_data_3,
                           isc_data=isc_chart_data_1, isc_data1=isc_chart_data_2, isc_data2=isc_chart_data_3,
                           cap_data=cap_chart_data_1, cap_data1=cap_chart_data_2, cap_data2=cap_chart_data_3,
                           fre_data=fre_chart_data_1, fre_data1=fre_chart_data_2, fre_data2=fre_chart_data_3,
                           ac_data=ac_chart_data_1, ac_data1=ac_chart_data_2, ac_data2=ac_chart_data_3,
                           uc_data=uc_chart_data_1, uc_data1=uc_chart_data_2, uc_data2=uc_chart_data_3, )


@app.route("/upload_insert_data")
def upload_insert_data():
    return render_template('staff/RG/upload_insert_data.html')


@app.route("/detailed_analysis")
def detailed_analysis():
    return render_template('staff/RG/detailed_analysis.html')


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
        db = shelve.open('costs.db', 'w')

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
                          now_date, now_time, "Kenobi")
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
    except FileNotFoundError:
        print("Database not found")

    try:
        changes_dict = db2['history']
    except:
        print("Error in retrieving data from shelve.")

    changes_list = []
    for key in changes_dict:
        change = changes_dict.get(key)
        changes_list.append(change)

    return render_template("staff/RG/update_history.html", update_history=changes_list)


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
        # if file.filename != '':
        #     file_ext = os.path.splitext(file.filename)[1]
        #     if file_ext not in app.config['ALLOWED_EXTENSIONS']:
        #         abort(400)
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
