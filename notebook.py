#_________WORKING WITH IMPORTS____________________________________________________________

from datetime import datetime
import json 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

#_________________________________________________________________________________________
#_________STARTING THE BOT________________________________________________________________


TOKEN = '5338479753:AAFzPCrocDj05i_nAAnU5JVMpmVj61LiUjc'
print("Bot started")
updater = Updater(TOKEN)


def start(update, context):
    """creates buttons and type an information"""
    chat = update.effective_chat
    buttons = [
        [KeyboardButton('/make_a_note')],
        [KeyboardButton('/check_my_notes')],
        [KeyboardButton('/delete_the_note')],
        [KeyboardButton('/menu')]
        ]
    context.bot.send_message(chat_id=chat.id, text="""Hi there! 
    \ni'm your friend, so you may entrust me the most secret things π
    \nI would be glad to listen to you π""",
    reply_markup=ReplyKeyboardMarkup(buttons))
    menu(update, context)

def menu(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="""
     - for creating a note tap on the button ππ "/make_a_note",
     \n - for viewing notes tap on the button πΈπ "/check_my_notes",
     \n - for deleting a note tap on the button ππ "/delete_the_note",
     \n - for viewing this menu tap on the button ππ "/menu"
     """)
#_________________________________________________________________________________________
#_________WORKING WITH MEMORY_____________________________________________________________


def saver(new_note):
    """saves notes with current date 
    into the file "notes.json" """

    now = datetime.now()
    save_to_json={
        'note' : f'{str(new_note)}',
        'date' : f'{now.strftime("%d.%m.%Y")}'
    }

    try:
        with open("notes.json") as f:
            data = list(json.load(f))
            data.append(save_to_json)
        with open("notes.json", 'w') as f:
            json.dump(data, f, indent=3)
    except FileNotFoundError:
        data = []
        data.append(save_to_json)
        with open('notes.json', 'w') as f:
            json.dump(data, f, indent=3)


#_________________________________________________________________________________________
#_________WORKING WITH NOTES______________________________________________________________


def first_addnote(update, context):
    """prints the text and triggers the next step"""

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="""
    okay, write down a note!ποΈπ""")
    return 1

    
def second_addnote(update, context):
    """is triggered by the previous func. 
    it gives the note to the saver func"""

    chat = update.effective_chat    
    new_note = str(update.message.text)
    saver(new_note) 
    context.bot.send_message(chat_id=chat.id, text="""
    well done!π""")
    return ConversationHandler.END


def cancel(update):
    """cancels the command if something went wrong"""

    update.message.reply_text(
        'Cancelled by user. Send /make_a_note to start again')
    return ConversationHandler.END


def checking_the_notes(update, context):
    """prints all notes to the user"""

    chat = update.effective_chat
    try:
        with open("notes.json") as f:
            data = json.load(f)
            if data == [] or data == '':
                context.bot.send_message(chat_id=chat.id, text="""
            you have added nothing yetπ""")
            else:
                context.bot.send_message(chat_id=chat.id, text="""
                __________________""")
                for i in data:
                    all_notes = i["note"]
                    context.bot.send_message(chat_id=chat.id, text="- " + f"{all_notes}")
                context.bot.send_message(chat_id=chat.id, text="""
                __________________""")
    except FileNotFoundError:
        context.bot.send_message(chat_id=chat.id, text="""
        you have added nothing yetπ""")


def first_deleter(update, context):
    """prints the text and triggers the next step"""

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="""
    please write the number of the note,\nor text it allπ""")
    return 2


def second_deleter(update, context):
    """is triggered by the previous func. 
    it deletes the note, chosen by user"""

    chat = update.effective_chat
    note = str(update.message.text)
    verifying = note.replace(" ", "")
    if verifying.isalpha() == True:
        try:
            with open("notes.json") as f:
                data = list(json.load(f))
                for i in data:
                    if i['note'] == note:
                        data.remove(i)
            with open("notes.json", "w") as f:            
                json.dump(data, f, indent=3)
            context.bot.send_message(chat_id=chat.id, text="""
    well done!π""")
        except FileNotFoundError:
            context.bot.send_message(chat_id=chat.id, text="""
            you have added nothing yetπ""")
    elif verifying.isdigit() == True:
        try:
            with open("notes.json") as f:
                data = list(json.load(f))
                ind = int(note) - 1
                data.pop(ind)
            with open("notes.json", "w") as f:            
                json.dump(data, f, indent=3)
            context.bot.send_message(chat_id=chat.id, text="""
    well done!π""")
        except FileNotFoundError:
            context.bot.send_message(chat_id=chat.id, text="""
            you have added nothing yetπ""")
        except IndexError:
            context.bot.send_message(chat_id=chat.id, text="""
            there is not such number of noteπ""")
    return ConversationHandler.END

    
#_________________________________________________________________________________________
#_________ADDING COMMANDS AND FUNCTIONS___________________________________________________


"""special construction for adding a note"""

adding_handler = ConversationHandler(
    entry_points=[CommandHandler('make_a_note', first_addnote)],
    states={
            1: [MessageHandler(Filters.text, second_addnote)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


"""special construction for deleting a note"""

deleting_handler = ConversationHandler(
    entry_points=[CommandHandler('delete_the_note', first_deleter)],
    states={
            2: [MessageHandler(Filters.text, second_deleter)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


disp = updater.dispatcher
disp.add_handler(adding_handler)
disp.add_handler(deleting_handler)
disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("check_my_notes", checking_the_notes))
disp.add_handler(CommandHandler("menu", menu))
disp.add_handler(CommandHandler("start", menu))
updater.start_polling()
updater.idle()
#_________________________________________________________________________________________
