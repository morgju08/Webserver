import sqlite3

def main():
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tweets ORDER BY Likes DESC")
    results = cursor.fetchall()
    print(results[0])
    for x in results:
        print("TWEET: %s  LIKES: %d" % (x[0], x[2]))

main()