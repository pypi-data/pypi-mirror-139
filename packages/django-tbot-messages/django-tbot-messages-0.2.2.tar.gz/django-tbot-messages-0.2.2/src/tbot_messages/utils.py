from django.forms.models import model_to_dict
from telebot import types
from telebot.custom_filters import AdvancedCustomFilter


class IsReplyButtonClick(AdvancedCustomFilter):
    """
        Filter to check whether the call.data is equals to callback_data of given button
        Example:
        @bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[1])
    """
    key = 'is_reply_btn_click'

    def check(self, message, button):
        if button.is_active:
            btn_txt = model_to_dict(
                button
            )[f'text_{message.from_user.lang}'] if model_to_dict(
                button
            ).get(f'text_{message.from_user.lang}') else model_to_dict(
                button
            )['text']
            return True if btn_txt == message.text else False
        else:
            return False

# todo: is_state filter


def is_text(text_to_check):
    return lambda message: message.text == text_to_check


def is_data(data_to_check):
    return lambda call: call.data == data_to_check


def generate_inline_result_from_queryset(
        query_set,
        offset,
        title,
        description,
        text,
        title_attr=False,
        description_attr=False,
        text_attr=False
):
    # todo: описание
    """
    Функция генерирующая список из InlineQueryResultArticle

    :param query_set:
    :param offset:
    :param title:
    :param description:
    :param text:
    :param title_attr:
    :param description_attr:
    :param text_attr:
    :return:
    """
    start_index = offset * 15
    end_index = start_index + 15
    query_set = query_set[start_index: end_index]

    results = []
    for index, model in enumerate(query_set, start=start_index):
        results.append(
            types.InlineQueryResultArticle(
                id=index, title=getattr(model, title) if title_attr else title,
                description=getattr(model,
                                    description) if description_attr else description,
                input_message_content=types.InputTextMessageContent(
                    message_text=getattr(model, text) if text_attr else text
                )
            )
        )
    return results
