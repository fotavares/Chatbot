# -*- coding: utf-8 -*-

import random
import json
import emoji
import re
import os
from dotenv import load_dotenv
from pytz import timezone
from datetime import datetime, time
from telegram import Update,Chat,MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

PATH = os.path.dirname(os.path.abspath(__file__))
JSON_CHATS = os.path.join(PATH,  "chats.json")
JSON_FALAS = os.path.join(PATH,  "jorjao.json")

load_dotenv()

CANAL_INTERNO = os.getenv('CANAL_INTERNO')
TOKEN = os.getenv('TOKEN')
BOTNAME = os.getenv('BOTNAME')
OWNER = os.getenv('OWNER')


mandou_dia = False
mandou_tarde = False
mandou_noite = False

class json_chats:
	js = None
	def __init__(self):
		with open(JSON_CHATS, "r", encoding = "utf-8") as jsfile:
			self.js = json.load(jsfile)

	def update(self,nome,id):
		found = False
		for j in self.js['chat_id']:
			if j['nome'] == nome:
				found = True
				j['chat_id'] = id
				#j['update'] = calendar.timegm(time.gmtime())

		if not found:
			newjs = {"nome":nome,"chat_id":id}#,"update":calendar.timegm(time.gmtime())
			self.js['chat_id'].append(newjs)
		self.save()

	def check(self,nome,id):
		for j in self.js['chat_id']:
			if j['nome'] == nome:
				return j['chat_id'] == id

	def save(self):
		with open(JSON_CHATS, 'w', encoding='utf-8') as f:
			json.dump(self.js, f, ensure_ascii=False, indent=4)

def get_json_falas():
	with open(JSON_FALAS, "r", encoding = "utf-8") as read_file:
		jsondata = json.load(read_file)
		return jsondata

def find(regex, string):
	x = re.search(regex,string)
	if x == None:
		return False
	else:
		return True

def send_log(context:CallbackContext,mensagem):
	context.bot.send_message(CANAL_INTERNO,"#Jorjaobot: "+ mensagem)

def get_dados_mensagem(chat):
	dados = "#fonte Id: {} - Tipo:{} - Titulo:{} - User:{} - Nome:{} - Sobrenome:{} - Bio:{} - Descrição:{} - Invite:{}".format(chat.id,chat.type,
		chat.title if chat.title is not None else '',
		chat.username if chat.username is not None else '',
		chat.first_name if chat.first_name is not None else '',
		chat.last_name if chat.last_name is not None else '',
		chat.bio if chat.bio is not None else '',
		chat.description if chat.description is not None else '',
		chat.invite_link if chat.invite_link is not None else '')

	return dados

def get_dados_curto(chat):
	dados = "#fonte Id: {} - Tipo:{} - Titulo:{} - User:{} - Nome:{} ".format(chat.id,chat.type,
		chat.title if chat.title is not None else '',
		chat.username if chat.username is not None else '',
		chat.full_name if chat.full_name is not None else '')

	return dados

def trata_mensagens(update: Update, context: CallbackContext) -> None:
	
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		message = update.effective_message
		
		falas = get_json_falas()
		for chave in falas['public']['actions']:
			if(find(r''+chave['word'],message.text.lower())):
				send_log(context,get_dados_curto(chat) + " TRIGGOU: " +chave['word'])
				if(chave['type'] == "text"):
					enviado = random.choice(chave['response'])
					message.reply_text(enviado,reply_to_message_id=message.message_id)
				elif(chave['type'] == "emoji"):
					qty = 1
					if(('qty' in chave) and (chave['qty'] != None)): 
						qty = int(chave['qty'])
					enviado = random.choice(chave['response'])
					message.reply_text(emoji.emojize(enviado * qty,use_aliases=True),reply_to_message_id=message.message_id)
				elif(chave['type'] == "image"):
					enviado = random.choice(chave['response'])
					message.reply_photo(enviado,reply_to_message_id=message.message_id)
				elif(chave['type'] == "doc"):
					enviado = random.choice(chave['response'])
					message.reply_document(enviado,reply_to_message_id=message.message_id)
				break

def trata_foto(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.photo[0].file_id)

def trata_video(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.video.file_id + ' - ' + mensagem.video.mime_type+ ' - ' + (mensagem.caption if mensagem.caption is not None else '') )

def trata_audio(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.audio.file_id)

def trata_animacao(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.animation.file_id)

def trata_documentos(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.document.file_id + ' - ' + mensagem.document.file_name )

def trata_video_nota(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.video_note.file_id)

def trata_sticker(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.sticker.file_id + ' - Set: t.me/addstickers/'+ str(mensagem.sticker.set_name))

def trata_voz(update: Update, context: CallbackContext) -> None:
	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP, chat.PRIVATE]:
		mensagem = update.effective_message
		chat.bot.send_message(CANAL_INTERNO,get_dados_curto(chat))
		chat.bot.forward_message(CANAL_INTERNO,chat.id,mensagem.message_id)
		chat.bot.send_message(CANAL_INTERNO,mensagem.voice.file_id)

def trata_usuarios_entrando(update: Update, context: CallbackContext) -> None:
	data = datetime.now(timezone('Brazil/East')).strftime('%d/%m/%Y %H:%M:%S')

	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
		falas = get_json_falas()
		message = update.effective_message
		if len(message.new_chat_members) > 0:
			for new_user in message.new_chat_members:
				if new_user.first_name != BOTNAME:
					if(falas["new_user"]["type"] == "text"):
						chat.bot.send_message(chat.id, random.choice(falas["new_user"]["response"]) % new_user.first_name)
					if(falas["new_user"]["type"] == "image"):
						chat.bot.sen_photo(chat.id, random.choice(falas["new_user"]["response"]))
					if(falas["new_user"]["type"] == "doc"):
						chat.bot.send_document(chat.id, random.choice(falas["new_user"]["response"]))
					send_log(context,'{} entrou em {} no {}'.format(new_user.first_name, data, chat.title))
				else:
					jschats = json_chats()
					jschats.update(chat.title,chat.id)
					send_log(context,'Fui colocado em {} no {}'.format(data, chat.title))
					send_log(context,get_dados_mensagem(chat))


def trata_usuarios_saindo(update: Update, context: CallbackContext) -> None:
	data = datetime.now(timezone('Brazil/East')).strftime('%d/%m/%Y %H:%M:%S')

	chat = update.effective_chat
	if chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
		falas = get_json_falas()
		message = update.effective_message
		#Usuario saiu
		if message.left_chat_member is not None:
			if message.left_chat_member.username == BOTNAME:
				send_log(context,'Fui Removido em {} de {}'.format(message.left_chat_member.first_name, data, chat.title))
			else:	
				if(falas["new_user"]["type"] == "text"):
					chat.bot.send_message(chat.id, random.choice(falas["left_user"]["response"]) % message.left_chat_member.first_name)
				if(falas["new_user"]["type"] == "image"):
					chat.bot.sen_photo(chat.id, random.choice(falas["left_user"]["response"]))
				if(falas["new_user"]["type"] == "doc"):
					chat.bot.send_document(chat.id, random.choice(falas["left_user"]["response"]))
				send_log(context,'{} saiu em {} de {}'.format(message.left_chat_member.first_name, data, chat.title))

def trata_comandos(update: Update, context: CallbackContext) -> None:
	pass

def dump_json(update: Update, context: CallbackContext) -> None:
	falas = get_json_falas()
	for chave in falas['public']['actions']:
		if chave['type'] == 'image':
			for img in chave['response']:
				update.message.bot.send_photo(update.effective_chat.id,img)
				update.message.bot.send_message(update.effective_chat.id,img)
	update.message.bot.send_message(update.effective_chat.id,"Cabou")

def limpa_automaticos(context: CallbackContext) -> None:
	global mandou_dia
	global mandou_tarde
	global mandou_noite

	mandou_dia = False
	mandou_tarde = False
	mandou_noite = False

def manda_bom_dia(context: CallbackContext) -> None:
	global mandou_dia
	if not mandou_dia:
		falas = get_json_falas()
		chats = [-1001274558355,-1001494834857]
		for chave in falas['public']['actions']:
			if(find(r''+chave['word'],"bom dia")):
				if(chave['type'] == "image"):
					mandou_dia = True
					for c in chats:
						enviado = random.choice(chave['response'])
						context.bot.send_photo(c,enviado)

		current_jobs = context.job_queue.get_jobs_by_name('dia')
		for job in current_jobs:
			job.schedule_removal()
		hora_execucao = time(random.randint(5,6),random.randint(0,59),0,tzinfo=timezone('Brazil/East'))
		context.job_queue.run_daily(manda_bom_dia,time=hora_execucao,job_kwargs={"misfire_grace_time":None},name='dia')

def manda_boa_tarde(context: CallbackContext) -> None:
	global mandou_tarde
	if not mandou_tarde:
		falas = get_json_falas()
		chats = [-1001274558355,-1001494834857]
		for chave in falas['public']['actions']:
			if(find(r''+chave['word'],"boa tarde")):
				if(chave['type'] == "image"):
					mandou_tarde = True
					for c in chats:
						enviado = random.choice(chave['response'])
						context.bot.send_photo(c,enviado)

		current_jobs = context.job_queue.get_jobs_by_name('tarde')
		for job in current_jobs:
			job.schedule_removal()
		hora_execucao = time(random.randint(12,13),random.randint(0,59),0,tzinfo=timezone('Brazil/East'))
		context.job_queue.run_daily(manda_boa_tarde,time=hora_execucao,job_kwargs={"misfire_grace_time":None},name='tarde')

def manda_boa_noite(context: CallbackContext) -> None:
	global mandou_noite
	if not mandou_noite:
		falas = get_json_falas()
		chats = [-1001274558355,-1001494834857]
		for chave in falas['public']['actions']:
			if(find(r''+chave['word'],"boa noite")):
				if(chave['type'] == "image"):
					mandou_noite = True
					for c in chats:
						enviado = random.choice(chave['response'])
						context.bot.send_photo(c,enviado)

		current_jobs = context.job_queue.get_jobs_by_name('noite')
		for job in current_jobs:
			job.schedule_removal()

		hora_execucao = time(random.randint(22,23),random.randint(0,59),0,tzinfo=timezone('Brazil/East'))
		context.job_queue.run_daily(manda_boa_noite,time=hora_execucao,job_kwargs={"misfire_grace_time":None},name='noite')

def main() -> None:
	# Create the Updater and pass it your bot's token.
	updater = Updater(TOKEN)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# Comandos do bot
	dispatcher.add_handler(CommandHandler('dumpimagens', dump_json))

	#Mensagens normais e restante das coisas
	dispatcher.add_handler(MessageHandler(Filters.command,trata_comandos))
	dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members,trata_usuarios_entrando))
	dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member,trata_usuarios_saindo))
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.entity(MessageEntity.SPOILER) & ~Filters.update.edited_message, trata_mensagens))
	dispatcher.add_handler(MessageHandler(Filters.video, trata_video))
	dispatcher.add_handler(MessageHandler(Filters.audio, trata_audio))
	dispatcher.add_handler(MessageHandler(Filters.animation, trata_animacao))
	dispatcher.add_handler(MessageHandler(Filters.document, trata_documentos))
	dispatcher.add_handler(MessageHandler(Filters.video_note, trata_video_nota))
	dispatcher.add_handler(MessageHandler(Filters.photo, trata_foto))
	dispatcher.add_handler(MessageHandler(Filters.sticker, trata_sticker))
	dispatcher.add_handler(MessageHandler(Filters.voice, trata_voz))
	

	#Jobs Automáticos
	hora_execucao = time(0,1,0,tzinfo=timezone('Brazil/East'))
	updater.job_queue.run_daily(limpa_automaticos,time=hora_execucao,job_kwargs={"misfire_grace_time":None})


	hora_execucao = time(random.randint(5,6),random.randint(0,59),0,tzinfo=timezone('Brazil/East'))
	updater.job_queue.run_daily(manda_bom_dia,time=hora_execucao,job_kwargs={"misfire_grace_time":None},name='dia')

	hora_execucao = time(random.randint(12,13),random.randint(0,59),0,tzinfo=timezone('Brazil/East'))
	updater.job_queue.run_daily(manda_boa_tarde,time=hora_execucao,job_kwargs={"misfire_grace_time":None},name='tarde')

	hora_execucao = time(random.randint(22,23),random.randint(0,59),0,tzinfo=timezone('Brazil/East'))
	updater.job_queue.run_daily(manda_boa_noite,time=hora_execucao,job_kwargs={"misfire_grace_time":None},name='noite')

	# Start the Bot
	updater.start_polling(allowed_updates=Update.ALL_TYPES,drop_pending_updates=True)
	updater.idle()

print ('Botando Jorjão pra fuder...')


if __name__ == '__main__':
	main()


