import shelve
# I hacked your system and got your password muahahahhahah
# username: DavidLim
# passowrd: abc123
with shelve.open('staff.db', 'r') as db:
    s = db['Staff']
    print(s[1].get_username())
    print(s[1].get_password())