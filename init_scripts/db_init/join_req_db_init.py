import sqlite3

conn = sqlite3.connect('requests.db')
c = conn.cursor()

c.execute("""CREATE TABLE join_req (
		username blob,
		userID blob,
		pubkey blob,
		request_rank blob,
		endorser1 blob,
		endorser2 blob,
		endorser3 blob
		)""")

conn.commit()
conn.close()
