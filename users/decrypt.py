from cryptography.fernet import Fernet

def decrypt(passwd):
	f = open('key.key', 'rb')
	key = f.read()
	f.close()

	f2 = Fernet(key)
	decrypted = f2.decrypt(passwd)
	original = decrypted.decode()
	return original
