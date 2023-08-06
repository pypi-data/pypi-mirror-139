from loguru import logger
from django.db import models
from django.utils import timezone
from django.conf import settings


class Mailing(models.Model):
    status_choices = [
        ('planned', 'Запланирована'),
        ('send', 'Отправлена')
    ]
    user_model = settings.MAILING_USERMODEL

    text = models.TextField(max_length=1024, verbose_name='Текст')
    date = models.DateTimeField(verbose_name='Дата рассылки', default=timezone.now)
    count = models.IntegerField(verbose_name='Получили', default=0)
    status = models.CharField(max_length=50, choices=status_choices, default='planned')
    users = models.ManyToManyField(user_model, related_name='mailings')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            from .tasks import send_mailing
            send_mailing.apply_async(eta=self.date, args=[self.id])
        except Exception as e:
            logger.error(e)

    def save_change(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Рассылка #{}'.format(self.id)


class Photo(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='photo')
    image = models.ImageField(upload_to='mailing', verbose_name='Фото', blank=True)

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'


class Buttons(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='buttons')
    text = models.CharField(max_length=100, verbose_name='Название Кнопки')
    url = models.URLField(verbose_name='Ссылка Кнопки')

    class Meta:
        verbose_name = 'кнопка'
        verbose_name_plural = 'кнопки'
