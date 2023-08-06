from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from .models import *


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, **kwargs):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u'<a href="%s" target="_blank"><img src="%s"'
                          u' alt="%s" width="300" style="object-fit: cover;"/>'
                          u'</a>' % (image_url, image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class BtnInline(admin.TabularInline):
    model = Buttons
    extra = 1
    max_num = 30


class PhotoInline(admin.StackedInline):
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    model = Photo
    extra = 1
    max_num = 9


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_status', 'date', 'get_users', 'get_count')
    readonly_fields = ('get_count',)
    inlines = [BtnInline, PhotoInline]
    exclude = ('status', 'count')
    filter_horizontal = ('users',)

    @admin.display(description='пользователи')
    def get_users(self, obj):
        return obj.users.all().count()

    @admin.display(ordering='status', description='статус')
    def get_status(self, obj):
        return obj.get_status_display()

    @admin.display(ordering='count', description='получили')
    def get_count(self, obj):
        return '{} из {}'.format(obj.count, obj.users.count())
