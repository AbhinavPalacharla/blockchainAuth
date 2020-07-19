import sqlite3

conn = sqlite3.connect('verified_users.db')

c = conn.cursor()

c.execute("""CREATE TABLE users (
		username blob,
		password blob,
		userID blob,
		pubkey blob,
		privkey blob,
		rank blob
		)""")

conn.commit()

c.execute("""CREATE TABLE project_managers (
		username blob,
		password blob,
		userID blob,
		pubkey blob,
		privkey blob,
		rank blob
		)""")

conn.commit()

c.execute("""CREATE TABLE admins (
		username blob,
		password blob,
		userID blob,
		pubkey blob,
		privkey blob,
		rank blob
		)""")

conn.commit()
conn.close()
