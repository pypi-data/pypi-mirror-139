import inspect
import os
import pathlib
from io import StringIO

import loguru
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection, models, transaction

import tbot_messages
from tbot_messages.models import BotMessage, Button


class Command(BaseCommand):
    help = 'Inflate database with messages enumerated in messages_list in messages.py'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete all messages from DB before pushing them again')
        parser.add_argument('--strict', action='store_true', help='Raise exeption if there is some errors')
        parser.add_argument('--only-new', action='store_true', help='Do not update old messages, just add new')

    def handle(self, *args, **options):
        table_names = connection.introspection.table_names()
        if 'tbot_messages_botmessage' in table_names and 'tbot_messages_button' in table_names:
            if options.get('reset'):
                Button.objects.all().delete()
                BotMessage.objects.all().delete()
                os.system('rm -rf tbot_messages/generated/*')

            messages_dict = settings.BOT_MESSAGES
            # scanning for locales and updating model with them
            all_locales = self.get_all_locales(messages_dict)
            if all_locales:
                errors = self.check_messages_locales(messages_dict, all_locales)
                if errors and options.get('strict'):
                    raise ValueError("\n".join(errors))
                else:
                    for err in errors:
                        loguru.logger.debug(err)
                self.update_models(all_locales, options.get('reset'))

            only_new = options.get('only_new')
            self.create_messages(all_locales, messages_dict, only_new)
        else:
            self.stdout.write(self.style.ERROR("ERROR -- tbot_messages is not migrated"))

    @transaction.atomic
    def create_messages(self, all_locales, messages_dict, only_new):
        # creating messages

        for mess_index, mess_name in enumerate(messages_dict):
            message_dict = settings.BOT_MESSAGES[mess_name]
            message_object, is_new_mess = BotMessage.objects.get_or_create(
                id=mess_index,
                name=mess_name,
            )
            if not is_new_mess and only_new:
                continue

            message_locales = self.get_locales(messages_dict[mess_name])
            if all_locales and message_locales:
                for locale in message_locales:
                    key = f'text_{locale}'
                    text = message_dict.get(key)
                    setattr(message_object, key, text)

            message_object.text = message_dict.get('text', ' - ')

            message_object.is_active = True
            message_object.name = mess_name
            message_object.save()

            stdout_mess = 'CREATED' if is_new_mess else 'UPDATED'
            self.stdout.write(f"Message \"{mess_index:02d}.{mess_name}\" with buttons was", ending=' ')
            self.stdout.write(self.style.SUCCESS(stdout_mess))

            Button.objects.filter(message=message_object).delete()

            if message_dict.get('buttons'):
                for btn_index, btn in enumerate(message_dict['buttons']):
                    self.add_button(message_object, btn_index, btn, all_locales)

    @transaction.atomic
    def add_button(self, message_object, btn_index, btn, all_locales):
        # creating buttons
        button, is_new_btn = Button.objects.get_or_create(
            message=message_object,
            num=btn_index,
        )
        button_locales = self.get_locales(btn)
        if all_locales and button_locales:
            if all_locales != set(button_locales):
                loguru.logger.debug(f'Button {btn_index} is not localised correctly')
            for locale in button_locales:
                key = f'text_{locale}'
                text = btn.get(key)
                setattr(button, key, text)
        button.text = btn.get('text', ' - ')
        if btn.get('reply'):
            button.is_reply = True
        elif btn.get('inline_mode'):
            button.is_inline_mode = True
        else:
            button.callback_data = btn['callback_data']
            button.is_reply = False
            button.is_inline_mode = False
        button.row = btn['row']
        button.is_active = True
        button.save()
        self.stdout.write(f"\tButton \"{btn_index}\" was", ending=' ')
        stdout_mess = 'CREATED' if is_new_btn else 'UPDATED'
        self.stdout.write(self.style.SUCCESS(stdout_mess))

    @staticmethod
    def update_models(locales, reset):
        migrate = False
        for locale in locales:
            loguru.logger.debug(f'Found locale {locale}')
            field = models.TextField(
                verbose_name=f'Текст {locale.upper()}',
                max_length=4096,
                null=True,
                blank=True,
                default=''
            )
            for model in (BotMessage, Button):
                if f'text_{locale}' not in model.__dict__:
                    migrate = True
                    setattr(
                        model,
                        f'text_{locale}',
                        field
                    )
                    model.add_to_class(f'text_{locale}', field)
        if migrate:
            module_dir = pathlib.Path(inspect.getfile(tbot_messages)).parent
            generated_dir = module_dir / '_generated/'
            if reset:
                BotMessage.objects.all().delete()

            a = input('ARE YOU SURE YOU WANT TO ADD FOUND LOCALES? (Y/n):: ')
            if a == 'n':
                exit(0)

            try:
                os.remove(generated_dir / 'botmessage.py')
                os.remove(generated_dir / 'button.py')
            except FileNotFoundError:
                pass

            call_command('makemigrations')
            call_command('migrate')

            message_model = StringIO()
            button_model = StringIO()
            call_command('inspectdb', 'tbot_messages_botmessage', stdout=message_model)
            call_command('inspectdb', 'tbot_messages_button', stdout=button_model)

            with open(generated_dir / 'botmessage.py', 'x') as message_file:
                message_file.write(message_model.getvalue())
            with open(generated_dir / 'button.py', 'x') as button_file:
                for line in button_model.getvalue().splitlines():
                    if line.endswith('DO_NOTHING)'):
                        line = line.replace('DO_NOTHING)', 'CASCADE, related_name="buttons")')
                    button_file.write(line + '\n')

    @staticmethod
    def check_messages_locales(messages, locales):
        errors = []
        for message_name in messages:
            message = messages[message_name]
            for locale in locales:
                key = f'text_{locale}'
                if key not in message.keys():
                    errors.append(f'Message {message_name} does not have {key}!')
                else:
                    if message[key] == '':
                        errors.append(f'Value of {key} in {message_name} is empty!')
        return errors

    @staticmethod
    def get_locales(message):
        message_locales = []
        for message_key in message.keys():
            if message_key.startswith('text_'):
                _, locale = message_key.split('_')
                if locale not in message_locales:
                    message_locales.append(locale)
        return message_locales

    def get_all_locales(self, messages_dict):
        all_locales = set()
        for message_name in messages_dict:
            message_locales = self.get_locales(messages_dict[message_name])
            all_locales.update(message_locales)
        return all_locales
