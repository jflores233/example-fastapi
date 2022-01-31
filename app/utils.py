from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hash a password
def hash(password: str):
    return pwd_context.hash(password)

#check if the password match
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)