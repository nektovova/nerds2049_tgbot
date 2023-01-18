from peewee import *
from playhouse.shortcuts import ReconnectMixin

import config


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
	pass


db = ReconnectMySQLDatabase(
	config.DATABASE_NAME, 
	user=config.DATABASE_USER, 
	password=config.DATABASE_PASSWORD,
	host=config.DATABASE_HOST, 
	port=config.DATABASE_PORT,
	charset=config.DATABASE_CHARSET,
)


class BaseModel(Model):

	class Meta:
		database = db


class Users(BaseModel):
	tg_user_id = TextField()
	channel_id = TextField()
	channel_name = TextField()


db.connect()
db.create_tables([Users,])
