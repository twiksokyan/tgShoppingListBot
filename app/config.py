from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
admins = env.list("ADMINS", subcast=int)
IP = env.str("IP")

# for DB
DB_USER = env.str("DB_USER") # имя пользователя (twiksokyan)
DB_PASS = env.str("DB_PASS") # пароль для юзера
DB_NAME = env.str("DB_NAME") # имя БД
DB_HOST = env.str("DB_HOST") # обычно localhost, если на компе запускаю
