import sqlite3

conn = sqlite3.connect('verify_usr_req.db')
c = conn.cursor()

c.execute("""CREATE TABLE init_verif_req (
		username blob,
		password blob,
		userID blob,
		pubkey blob
		)""")


conn.commit()

c.execute("""CREATE TABLE verif_ident (
		username blob,
		userID blob,
		targetID blob,
		pubkey blob,
		signature blob
		)""")

conn.commit()

c.execute("""CREATE TABLE resp (
		username blob,
		userID blob,
		targetID blob,
		pubkey blob,
		signature blob
		)""")

conn.commit()
conn.close()
