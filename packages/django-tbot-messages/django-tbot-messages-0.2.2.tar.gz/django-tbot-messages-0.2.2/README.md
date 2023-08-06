# django-tbot-messages

------------

#### Структура модуля
 - [Команда сreate_messages](#create_messages)
 - [utils.py](#utilspy)
 - [messages.py](#messagespy)
 - [views.py](#viewspy)

[Быстрый старт с модулем](#quickstart)  
[Локализация сообщений](#использование-локализации)  
[Система диалогов](#диалоги)

------------------------------------------------------------

### Описание  
Модуль служит для удобной интеграции функции отключаемых сообщений с возможностью переводов.  
Также в модуле предусмотрена простая машина состояний и система диалогов.

------------

### create_messages

Команда `manage.py create_messages` добавляет в базу данных сообщения описанные 
в переменной `BOT_MESSAGES` в файле `settings.py` проекта.

> Формат переменной BOT_MESSAGES:
> ```python
> BOT_MESSAGES = {
>   'ChooseLanguage': {
>        'text': 'Выберите язык',
>        'buttons': [
>            {'reply': True, 'row': 0, 'text': 'Русский'},
>            {'reply': True, 'row': 0, 'text': 'Українська'}
>        ]
>    },
>    'Promo': {
>        'text': 'Вам доступен бесплатный тестовый 2ух недельный период на максимальных возможностях!\n',
>        'text_ua': 'Промо українською',
>    },
>    'Menu': {
>        'text': 'Вам доступно главное меню.\n\n'
>                'В разделе "📝 Создать подписку" вы сможете создать запрос для поиска объявлений по заданным вами параметрам\n'
>                'В разделе "🗂 Мои подписки" вы сможете просмотреть/удалить созданные ранее вами запросы поиска авто.\n'
>                'В разделе "👨‍🔧 Техподдержка" вы сможете отправить сообщение нашему Администратору и получить ответ или консультацию\n'
>                'С помощью функции "🙅 Не беспокоить" вы сможете приостановить поиск объявлений и позднее его "🙋‍♂Восстановить".\n'
>                'В разделе "👤 Мой профиль" вы сможете просмотреть статус вашего текущего тарифа и продлить тариф.\n',
>        'text_ua': 'Меню українською',
>        'buttons': [
>            {'reply': True, 'row': 0, 'text': '🗂 Мои подписки', 'text_ua': '🗂 Мої підписки'},
>            {'reply': True, 'row': 0, 'text': '📝 Создать подписку', 'text_ua': '📝 Створити підписку'},
>            {'reply': True, 'row': 1, 'text': '👨‍🔧 Техподдержка', 'text_ua': '👨‍🔧 Техпідтримка'},
>            {'reply': True, 'row': 1, 'text': '🙅 Не беспокоить', 'text_ua': '🙅 Не турбувати'},
>            {'reply': True, 'row': 2, 'text': '👤 Мой профиль и тарифы', 'text_ua': '👤 Мій профіль та тарифи'},
>        ]
>    }
> }
>```

Конечно, помещать весь словарь в settings.py вас никто не просит...  
Всегда можно импортировать его из другого файла дабы не засорять настройки:

> settings.py
> ```python 
>  ...
>  from tbot.translations import messages
>  BOT_MESSAGES = messages
>  ...
> ```

Словарь `BOT_MESSAGES` состоит из пар имени сообщения в БД и его параметров.  
Среди параметров указываются ключи `text_{locale}` или просто `text` если мы хотим 
использовать это значение по умолчанию.

Также, среди параметров сообщения есть ключ `buttons`, значением которого является массив кнопок. `buttons` можно не указывать если сообщение не содержит кнопок. 
Каждая кнопка это словарь с параметрами:

> ```
>   text         : str   текст кнопки используемый по умолчанию
>   text_{locale}: str   текст кнопки используемый если в user_data есть ключ locale (не обязательно)
>   callback_data: str   callback_data кнопки
>   reply        : bool  при значении True кнопка становится ReplyButton (если параметр не указан или равен False - по умолчанию кнопка InlineKeyboardButton и требует параметр callback_data)
>   inline_mode  : bool  при значении True кнопка обретает параметр switch_inline_query_chat и становится "точкой входа" в инлайн режим бота
>   row          : int   номер ряда (начиная с нулевого), в котором будет отображена кнопка
>   * url        : str   пока что такого параметра нет, но всему своё время!
> ```

После того как вы создали словарь `BOT_MESSAGES`, запускайте команду `manage.py create_messages`,
если вы добавляли локализацию текста (ключи `text_{locale}`), вы увидите перечень добавленных 
локализаций и вопрос:

`ARE YOU SURE YOU WANT TO ADD FOUND LOCALES? (Y/n)::`

После нажатия Enter команда сгенерирует новые модели `BotMessage` и `Button` которые будут содержать 
поля с локализованным текстом. 

### Дисклеймер
Крайне рекомендую (на момент версии 0.2) выполнять команду `manage.py makemigrations <app>` с указанием параметра `app`!  
Это избавит вас от случайного удаления модели `BotMessage` и перезаписи этой самой модели сгенерированной моделью с локализованным текстом.


### utils.py

В этом файле вы найдете разные фильтры и функции облегчающие разработку

### messages.py

В `messages.py` присутствуют классы `BaseMessages` и `BaseDialogs`, работа с ними показывается [тут](#quickstart) и [тут](#диалоги) соответственно. 

## Quickstart

Прежде всего, установите данный модуль
```
pip install django-tbot-messages
```
Если модули [tbot-base](https://pypi.org/project/django-tbot-base/) и [bot-storage](https://pypi.org/project/bot-storage/) не были установлены в вашем проекте, 
не проблема - они указаны в зависимостях к данному модулю.


Далее, будет описан пример создания проекта с использованием `tbot_messages`

Инициализируйте приложение `tbot` с помощью `manage.py startapp tbot`  
Добавьте их в `INSTALLED_APPS` в `settings.py` проекта  

```python
INSTALLED_APPS = [
    ...
    'tbot',
    'tbot_messages',
]
```  

Не забудьте добавить BOT_STORAGE в `settings.py`, указав обьект хранилища

```python 
storage.py

from os import getenv
from bot_storage.storage import RedisStorage

storage = RedisStorage(
    host=getenv('REDIS_HOST', 'localhost'),
    username=getenv('REDIS_USER', None),
    password=getenv('REDIS_PASSWORD', None)
)
```

```python
settings.py

from .storage import storage
BOT_STORAGE = storage
```

Также, создадим сообщения нашего бота в файле `translations.py`

```python
messages = {
    'SupportText': {
        'text_ru': 'Отправьте текст вашего сообщения. 🙂',
        'text_ua': 'Надішліть ваш запит',
        'buttons': [
            {'reply': True, 'row': 0, 'text_ru': 'Главное меню', 'text_ua': 'Головне меню'},
        ]
    },
    'SupportSent': {
        'text_ru': 'Я отправил ваш вопрос Администратору!🙂 Он ответит вам в ближайшее время!',
        'text_ua': 'Я надіслав ваше питання адміну. Очікуйте',
    },
    'SupportAnswer': {
        'text_ru': 'Ответ от Администратора:\n'
                ' - <code>{text}</code>',
        'text_ua': 'Відповідь адміна: <code>{text}</code>',
    }
}
```

Укажите значение `BOT_MESSAGES` в `settings.py`

```python
 # tbot_base configuration
 BOT_HANDLERS = [
    'tbot.dispatcher',
    'tbot.handlers',
 ]

 from tbot.storage import storage
 from tbot.translations import messages

 # instance of storage (such as redis, db or another)
 BOT_STORAGE = storage
 BOT_MESSAGES = messages
```

> Настройка `BOT_HANDLERS` используется при запуске проекта, она служит для 
> последовательной загрузки всех модулей с хендлерами вашего бота. Данная настройка подразумевается
> при использовании базового модуля [tbot_base](https://pypi.org/project/django-tbot-base/)

Окей, теперь можем выполнять миграции
```
manage.py makemigrations && manage.py migrate
```

Выполняем команду `manage.py create_messages` и подтверждаем генерацию моделей с локализациями нажатием клавиши Enter (всегда можно отказаться написав `n`)  

Бинго! Сообщения и кнопки создались, теперь переходим к классу `BaseMessages`  
Создадим файл `messages.py` и в нем опишем класс `Messages` унаследованный от `BaseMessages`

```python
from tbot_messages.messages import BaseMessages

class Messages(BaseMessages):
    SupportText = 'SupportText'
    SupportSent = 'SupportSent'
    SupportAnswer = 'SupportAnswer'
```

Мы должны присвоить обьектам сообщений их названия в БД (однажды я автоматизирую этот процесс, но пока наслаждайтесь)

А теперь можем смело использовать обьект сообщения и отправлять его, если оно активно

`dispatcher.py`
```python
from telebot import types
from tbot.messages import Messages
from tbot_base.bot import tbot

@tbot.message_handler(commands=['start'])
def support_text(message: types.Message):
    user_id = message.from_user.id
    Messages.SupportText.send_if_active(user_id)
```

### Использование локализации
 
Язык который будет использован при отправке сообщения во время
вызова метода `send_if_active()` зависит от значения `locale` в user_data.  

Чтобы предложить пользователю выбрать язык, сделаем простой хендлер нажатия
реплай кнопок `Русский` и `Українська`

dispatcher.py
```python
from telebot import types
from tbot_base.bot import tbot
from .storage import storage

@tbot.message_handler(func=lambda message: message.text in ('Русский', 'Українська'))
def language_handler(message: types.Message):
    user_id = message.from_user.id
    if message.text == 'Русский':
        locale = None
    elif message.text == 'Українська':
        locale = 'ua'
    storage.update_user_data(user_id, 'locale', locale)
```

В данном случае, мы используем локализацию по умолчанию если был выбран русский язык.  
Т.е поле `text` будет использовано при `locale = None`, но как только `locale`
приобретает какое либо значение, текст сообщений берётся из `text_{locale}`


### Диалоги

Диалоги идеально подходят создания форм.  
Например, сделаем простую регистрацию используя класс `Dialogs` и `Messages` 

`messages.py`
```python
from tbot_messages.messages import BaseMessages, BaseDialogs

class Messages(BaseMessages):
    AskName = 'AskName'
    AskPhone = 'AskPhone'
    AskEmail = 'AskEmail'

class Dialogs(BaseDialogs):
    REG = (Messages.AskName, Messages.AskPhone, Messages.AskEmail)
```

И теперь напишем логику регистрации

`dispatcher.py`
```python
from telebot import types
from tbot_base.bot import tbot
from .storage import storage as st
from .messages import Dialogs
from .models import User

@tbot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    user_id = message.from_user.id
    user = User.object.filter(id=user_id).first()
    if not user:
        # флаг start в данном случае обязателен
        Dialogs.REG.next_message(user_id, start=True)
    else:
        ...

# state пользователя генерируется автоматически
@tbot.message_handler(func=lambda msg: st.get_user_state(msg.from_user.id) == 'REG:AskName')
def ask_name_handler(message: types.Message):
    name = message.text
    user_id = message.from_user.id
    
    # сохраняем значение в хранилище
    st.update_user_data(user_id, 'name', name)
    
    Dialogs.REG.next_message(user_id)
```

При использовании `.next_message()` перезаписывается `state` пользователя
на `dialog:message`. В данном примере диалог называется `REG`, и при вызове 
`.next_message(start=True)` отправленным сообщением будет первое в кортеже - `AskName`.

Вызвав метод `.next_message()` во второй раз, бот отправит пользователю сообщение 
`AskPhone` и установит его состояние на `REG:AskPhone`
