import bcrypt

password_to_salt = "super secret password"
salted = bcrypt.hashpw( bytes(password_to_salt,  'utf-8' ) , bcrypt.gensalt(10))

print(salted)

