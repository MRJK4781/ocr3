import requests

from telegram import Update
from telegram.ext import CallbackContext

from ocrbot.config import API_KEY
from ocrbot.helpers.decorators import send_typing_action


@send_typing_action
def extract_image(update: Update, context: CallbackContext):
    '''
    This function is called when the user sends a photo.
    '''
    chat_id = update.effective_chat.id
    file_id = update.message.photo[-1].file_id
    file_path = context.bot.get_file(file_id).file_path
    m = update.message.reply_text('...', quote=True)
    if file_path is not None:
        data = requests.get(f"https://api.ocr.space/parse/imageurl?apikey={API_KEY}&url={file_path}&language=chs&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True").json()
        if data['IsErroredOnProcessing'] == False:
            message = data['ParsedResults'][0]['ParsedText']
            m.edit_text(text=message)
        else:
            m.edit_text(text="⚠️Something went wrong, please try again later ⚠️")
    else:
        m.edit_text("Something went wrong, Send this image again")
