import sqlite3
import secrets
import hashlib

def main():
    # 1.) Prompt user for input
    username = input("Enter Username:  ")
    password = input("Enter Password:  ")
    print("User: %s, Password: %s" % (username, password))

    # 2.) Generate Salt
    salt = secrets.token_hex(6)

    # 3.) Put together the salt and password
    salted_password = password+salt

    # 4.) Hash the password
    hashed_password = hashlib.md5(salted_password.encode('ascii')).hexdigest()

    # 5.) Putting user info in database
    conn = sqlite3.connect("tweet_db.db")
    conn.execute("INSERT INTO Users (username, password, salt) VALUES (?,?,?)",
                 (username, hashed_password, salt))
    conn.commit()
    conn.close()

main()