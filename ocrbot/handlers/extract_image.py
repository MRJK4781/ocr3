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
    m = update.message.reply_text('Extracting...', quote=True)
    if file_path is not None:
        data = requests.get(f"https://api.ocr.space/parse/imageurl?apikey={API_KEY}&url={file_path}&language=chs&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True").json()
        if data['IsErroredOnProcessing'] == False:
            message = data['ParsedResults'][0]['ParsedText']
            query.edit_message_text(text=message)
        else:
            query.edit_message_text(text="⚠️Something went wrong, please try again later ⚠️")
    else:
        query.edit_message_text("Something went wrong, Send this image again")
