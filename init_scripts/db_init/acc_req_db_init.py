import sqlite3

conn = sqlite3.connect('requests.db')
c = conn.cursor()

c.execute("""CREATE TABLE acc_req (
		username blob,
		userID blob,
		targetID blob,
		pubkey blob,
		msg blob,
		signature blob
		)""")

conn.commit()
conn.close()
