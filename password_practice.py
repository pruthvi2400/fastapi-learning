from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

password = "mypassword123"
hashed_password = password_hash.hash(password)

print("Original password:", password)
print("Hashed password:", hashed_password)

print(
    "Correct password:",
    password_hash.verify("mypassword123", hashed_password)
)

print(
    "Wrong password:",
    password_hash.verify("wrongpassword", hashed_password)
)