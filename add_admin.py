import hashlib
from database import *

print('Введите через пробел имя пользователя админа и пароль:')

db = Database()


def check(db):
    admin = input().split()
    users = db.all()
    for i in users:
        if i[0] == admin[0]:
            print('Данный пользователь уже зарегестрирован, введите другие данные:')
            return check(db)
    return admin


admin, password = check(db)

hash = hashlib.sha256(password.encode()).hexdigest()
db.register(admin, hash, 'TRUE')
print('Пользователь успешно зарегистрирован')
