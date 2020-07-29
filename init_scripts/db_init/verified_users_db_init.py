import sqlite3

conn = sqlite3.connect('verified_users.db')

c = conn.cursor()

c.execute("""CREATE TABLE users (
		username blob,
		userID blob,
		pubkey blob
		)""")

conn.commit()
conn.close()
