import bcrypt

passwordStudent1 = b"std1"
passwordStudent2 = b"std2"
passwordStudent3 = b"std3"
passwordInstructor1 = b"ist123"
passwordInstructor2 = b"ist2"
passwordAdmin = b"adm123"

hashed = bcrypt.hashpw(passwordStudent1, bcrypt.gensalt())
print(hashed.decode())