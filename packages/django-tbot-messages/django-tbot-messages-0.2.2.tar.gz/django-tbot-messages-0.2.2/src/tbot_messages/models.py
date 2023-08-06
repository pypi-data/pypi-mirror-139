import importlib

from django.db import models

try:
    m = importlib.import_module('tbot_messages._generated.botmessage')
    BotMessage = m.__getattribute__('TbotMessagesBotmessage')
    BotMessage._meta.verbose_name = 'текст сообщения'
    BotMessage._meta.verbose_name_plural = 'текста сообщений'
except (ModuleNotFoundError, AttributeError) as e:
    class BotMessage(models.Model):
        name = models.CharField(verbose_name='ID',
                                max_length=200, unique=True)
        text = models.TextField(verbose_name='Текст', max_length=4096,
                                null=True, default='', blank=True)
        is_active = models.BooleanField(verbose_name='Активно?',
                                        null=True, default=True)

        def __str__(self):
            return f'{self.id:2d}.{self.name}'

        class Meta:
            verbose_name = 'текст сообщения'
            verbose_name_plural = 'текста сообщений'

try:
    m = importlib.import_module('tbot_messages._generated.button')
    Button = m.__getattribute__('TbotMessagesButton')
    Button._meta.ordering = ('num',)
except (ModuleNotFoundError, AttributeError):
    class Button(models.Model):
        message = models.ForeignKey(BotMessage, on_delete=models.CASCADE, related_name='buttons')
        text = models.CharField(verbose_name='Текст кнопки', max_length=200, default='', null=True)
        num = models.SmallIntegerField(verbose_name='Номер кнопки', default=0)
        is_active = models.BooleanField(verbose_name='Активна?', default=True, null=True)

        # for inline-mode
        is_inline_mode = models.BooleanField(default=False, null=True)

        # for default(inline) buttons
        callback_data = models.CharField(max_length=40, null=True)

        # for reply buttons
        is_reply = models.BooleanField(default=False, null=True)
        row = models.SmallIntegerField(default=0, null=True)

        def __str__(self):
            return self.text

        class Meta:
            ordering = ('num',)
            verbose_name = 'Кнопка'
            verbose_name_plural = 'Кнопки'
