from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Application
from telegram.ext import filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler

import database
import config
import util


async def start_command_handler(update, context):
	cid = update.message.chat.id
	uid = update.message.from_user.id
	await update.message.reply_text(config.START_TEXT)
	return


async def list_command_handler(update, context):
	cid = update.message.chat.id
	uid = update.message.from_user.id

	q = database.Users.select().where(
		database.Users.tg_user_id == str(uid)
	)
	text = 'Список отслеживания:\n\n'
	for user in q:
		text += '{} /delete_{}\n'.format(user.channel_name, user.id)
	text += '\nЧто бы добавить канал в свой список отслеживания, перешли в бота любой его пост'
	await update.message.reply_text(text)
	return


async def forwarded_content_handler(update, context):
	cid = update.message.chat.id
	uid = update.message.from_user.id

	# Проверка что сообщение пересылается из канала
	if update.message.forward_from_chat and str(update.message.forward_from_chat.type) == 'channel':
		channel_id = update.message.forward_from_chat.id

		q = database.Users.select().where(
			(database.Users.tg_user_id == str(uid))
			& (database.Users.channel_id == str(channel_id))
		)

		if q.exists():
			text = 'Вы уже добавили ранее этот канал'
			await update.message.reply_text(text)
			return

		database.Users(
			tg_user_id=str(uid),
			channel_id=str(channel_id),
			channel_name=util.remove_emoji(update.message.forward_from_chat.title),
		).save()

		text = 'Канал {} добавлен в список отслеживания'.format(
			update.message.forward_from_chat.title,
		)
		text += '\n\n/list - управление списком отслеживания'
		await update.message.reply_text(text)
		return


async def text_content_handler(update, context):
	cid = update.message.chat.id
	uid = update.message.from_user.id

	if update.message.text.startswith('/delete_'):
		db_row_id = int(update.message.text.split('_')[1])

		q = database.Users.select().where(
			database.Users.id == db_row_id
		)
		if not q.exists():
			text = 'Канал был удален ранее'
			await update.message.reply_text(text)
			return
		db_row = q.get()

		if not db_row.tg_user_id == str(uid):
			text = 'Канал был удален ранее'
			await update.message.reply_text(text)
			return

		database.Users.delete().where(
			database.Users.id == db_row_id
		).execute()

		text = 'Канал {} удален из списка отслеживания'.format(
			db_row.channel_name,
		)
		text += '\n\n/list - управление списком отслеживания'
		await update.message.reply_text(text)
		return


def main():
	application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

	application.add_handler(CommandHandler('start', start_command_handler))
	application.add_handler(CommandHandler('list', list_command_handler))
	application.add_handler(MessageHandler(filters.FORWARDED, forwarded_content_handler))
	application.add_handler(MessageHandler(filters.TEXT, text_content_handler))

	application.run_polling()


if __name__ == '__main__':
	main()
