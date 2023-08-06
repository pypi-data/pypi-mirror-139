import re
import time
from loguru import logger
from django.conf import settings
from tbot_base.bot import tbot as bot
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InputMediaPhoto)

from .models import Mailing

app = settings.CELERY_APP


@app.task(name='send_mailing')
def send_mailing(mail_id):
    count = 0
    time.sleep(2)
    try:
        mailing = Mailing.objects.prefetch_related('buttons').prefetch_related('photo').get(pk=mail_id)
        try:
            markup = InlineKeyboardMarkup(row_width=1)
            for btn in mailing.buttons.all():
                markup.add(InlineKeyboardButton(btn.text, url=btn.url))
        except Exception:
            markup = None
        try:
            photo = []
            for ph in mailing.photo.all():
                if ph:
                    with open(settings.MEDIA_ROOT + f'/{ph.image}', "rb") as f:
                        photo.append(InputMediaPhoto(f.read()))
        except Exception:
            photo = None

        for user in mailing.users.all():
            try:
                if photo is not None and len(photo) > 0:
                    bot.send_media_group(user.user_id, photo)
                if mailing.text:
                    text = re.sub(
                        r'(?=[_|*|\[|\]\(|\)|~|`|>|#|\+|\-|=|\||\{|\}|\.|\!])',
                        r'\\',
                        mailing.text
                    )
                    bot.send_message(user.user_id, text, reply_markup=markup, parse_mode='MarkdownV2')
                time.sleep(0.1)
                count += 1
            except Exception as e:
                logger.error(e)
                logger.info(f'Error: send to {user.user_id}')

        mailing.status = 'send'
        mailing.count = count
        mailing.save_change()
        logger.info(f'----------Конец рассылки--------\nОтправил: {count} раз')
    except Exception as e:
        logger.debug(e)
        logger.info(f'Рассылка с #{mail_id} не найдена')
