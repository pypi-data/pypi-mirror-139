from django.contrib import admin
from .models import BotMessage, Button


class ButtonInline(admin.TabularInline):
    model = Button
    extra = 0
    max_num = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

    def get_fields(self, request, obj=None):
        fields = ['is_active']
        for text_key in filter(lambda key: key.startswith('text'), Button.__dict__):
            fields.append(text_key)
        fields.append('is_inline_mode')
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['is_inline_mode']
        for text_key in filter(lambda key: key.startswith('text'), Button.__dict__):
            fields.append(text_key)
        return fields


@admin.register(BotMessage)
class MessageAdmin(admin.ModelAdmin):
    ordering = ('id',)
    inlines = [ButtonInline]

    def get_list_display(self, request):
        list_display = ['name', ]
        for text_key in filter(lambda key: key.startswith('text'),
                               BotMessage.__dict__):
            list_display.append(text_key)
        list_display.extend(['buttons', 'status'])
        return list_display

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    @admin.display(description='Кнопки')
    def buttons(self, obj):
        texts = []
        for btn in obj.buttons.all():
            if hasattr(btn, 'text_ru') and btn.text_ru:
                texts.append(btn.text_ru)
            else:
                texts.append(btn.text)

        return texts

    @admin.display(description='Статус')
    def status(self, obj):
        return '🟢' if obj.is_active else '🔴'
