from enum import Enum
from typing import Union

from django.conf import settings
from loguru import logger
from tbot_base.bot import tbot as bot
from telebot import types

from .models import BotMessage


class MessageDescriptor:
    def __init__(self, name):
        self._model_name = name if name else self.name
        if not self.get_model():
            logger.debug(f'Message {self._model_name} is not exists in database!')

    def __str__(self):
        return self._model_name

    def get_model(self):
        try:
            return BotMessage.objects.get(name=self._model_name)
        except:
            return None

    @property
    def id(self):
        return self.get_model().id

    @property
    def text(self):
        return self.get_model().text

    @property
    def is_active(self):
        return self.get_model().is_active

    @property
    def buttons(self):
        # return self._buttons if self._buttons else self.get_model().buttons.filter(is_active=True)
        return self.get_model().buttons.filter(is_active=True)

    @property
    def mess_key(self):
        m = self.get_model()
        return f'{m.id:02d}.{m.name}'

    def get_keyboard_markup(self, locale):
        buttons = self.buttons
        if not buttons.exists():
            return None
        # определяем максимальное количество рядов клавы
        rows = buttons.order_by('-row').first().row + 1
        # определяем тип клавиатуры (берем первую кнопку и смотрим ее тип)
        if buttons.first().is_reply:
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=rows,
                one_time_keyboard=True
            )
        else:
            markup = types.InlineKeyboardMarkup(
                row_width=rows
            )

        # наполняем клавиатуру
        for current_row in range(rows):
            row_buttons_models = buttons.filter(row=current_row)
            row_buttons_objects = []

            for button_model in row_buttons_models:
                text = getattr(button_model, f'text_{locale}', None)
                if not text:
                    text = button_model.text
                if button_model.is_reply:
                    row_buttons_objects.append(
                        types.KeyboardButton(text=text)
                    )
                    continue

                # если кнопка должна отправлять в инлайн мод
                switch_current_pm = '' if button_model.is_inline_mode else None
                row_buttons_objects.append(
                    types.InlineKeyboardButton(
                        text=text,
                        callback_data=button_model.callback_data,
                        switch_inline_query_current_chat=switch_current_pm
                    )
                )
            markup.row(*row_buttons_objects)
        return markup

    def send_if_active(
            self, user_id: int, custom_text: str = None, custom_markup=None,
            set_state: str = None, format_map: dict = None, **kwargs
    ):
        if set_state:
            settings.BOT_STORAGE.set_user_state(user_id, set_state)

        if not self.is_active:
            return

        text = None
        locale = None
        if custom_text:
            text = custom_text
        else:
            if locale := settings.BOT_STORAGE.get_user_data(user_id).get('locale'):
                text = getattr(self.get_model(), f'text_{locale}')
            if not text:
                text = self.text
        if format_map:
            text = text.format_map(format_map)

        markup = custom_markup if custom_markup else self.get_keyboard_markup(locale)
        try:
            return bot.send_message(
                user_id, text, reply_markup=markup, parse_mode='html', **kwargs
            )
        except Exception as e:
            logger.debug(self._model_name)
            raise e


class DialogDescriptor:
    def __init__(self, *messages):
        self.messages = messages
        self.messages_name = [str(m) for m in messages]

    def next_message(self, user_id, start=False):
        if start:
            first_message = self.messages[0]
            return self._proceed(user_id, message=first_message)

        dialog_name, current_step = self._get_current_stage(user_id)
        if dialog_name != self.name:
            raise Exception(f'{user_id} is in {dialog_name}, but {self.name} was called')

        next_message = self._get_next_message(current_step)
        if not next_message:
            logger.debug('there is no next message')
            return None

        sent_message = self._proceed(user_id, next_message)
        if not sent_message:
            return self.next_message(user_id)

        return sent_message

    def previous_message(self, user_id):
        dialog_name, current_step = self._get_current_stage(user_id)
        if dialog_name != self.name:
            raise Exception(f'{user_id} is in {dialog_name}, but {self.name} was called')

        previous_message = self._get_previous_message(current_step)
        if not previous_message:
            logger.debug('there is no previous message')
            return None

        sent_message = self._proceed(user_id, previous_message)
        if not sent_message:
            return self.previous_message(user_id)

        return sent_message

    def _get_next_message(self, current_step):
        if current_step not in self.messages_name:
            raise Exception(f'"{current_step}" is not {self.name} stage')

        try:
            indx = self.messages_name.index(current_step)
            return self.messages[indx + 1]
        except IndexError:
            return None
        except ValueError:
            logger.debug(f'get_next_message ValueError: {current_step}')

    def _get_previous_message(self, current_step):
        if current_step not in self.messages_name:
            raise Exception(f'"{current_step}" is not {self.name} stage')

        try:
            indx = self.messages_name.index(current_step)
            if indx > 0:
                return self.messages[indx - 1]
        except IndexError:
            return None
        except ValueError as e:
            logger.debug(f'get_previous_message {e} ValueError: {current_step}')

    def _proceed(self, user_id, message: MessageDescriptor):
        next_state = self._generate_state(message)
        return message.send_if_active(user_id, set_state=next_state)

    def _generate_state(self, message):
        return f'{self.name}:{message.name}'

    @staticmethod
    def _get_current_stage(user_id):
        state = settings.BOT_STORAGE.get_user_state(user_id)
        if state:
            dialog_name, current_step = state.split(':')
            return dialog_name, current_step
        else:
            raise Exception(f'{user_id} doesn\'t have a state')


class BaseMessages(MessageDescriptor, Enum):
    pass


class BaseDialogs(DialogDescriptor, Enum):
    @classmethod
    def get_current_dialog(cls, user_state: str) -> Union[tuple[DialogDescriptor, str], tuple[None, None]]:
        """
        Returns current dialog of user and stage of this dialog
        Returns tuple(None, None) if user is not in dialog
        :param user_state: get_user_state(user_id)
        :return: Union[tuple[DialogDescriptor, str], tuple[None, None]]
        """

        if user_state and ':' in user_state:
            dialog_name, stage = user_state.split(':')
            if dialog_name in cls.__members__:
                return cls.__members__[dialog_name], stage
            else:
                raise ValueError(f'No such dialog {dialog_name}')
        return None, None
