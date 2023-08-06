# django-tbot-mailing

### Установка

`pip install django-tbot-mailing`

### Настройка

В `settings.py`

```python
...
INSTALLED_APPS = [
    ...,
    'tbot_base'
    'tbot_delay_messages'
]

BOT_HANDLERS = [        # для tbot_base
    'tbot.dispatcher',
]

MAILING_USERMODEL = 'tbot.User' # укажите модель пользователя 

from .celery import app
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_APP = app # приложение celery созданное в celery.py проекта

MEDIA_ROOT = 'media/'
```

Необходимые для работы модуля опции - `MAILING_USERMODEL` и `CELERY_APP`.  
В модели пользователя, указанной в `MAILING_USERMODEL` должно присутствовать поле
`user_id`  
Также, для корректного сохранения изображений рассылки укажите `MEDIA_ROOT`

Далее, выполняем миграции

`./manage.py makemigrations && ./manage.py migrate`

Не забудьте запустить celery  

`celery -A proj worker -E`

### Использование

Создать и запланировать рассылку вы можете в админ-панели 
