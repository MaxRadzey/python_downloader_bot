from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import ManyToOneRel

from bot.models import TelegramUser

admin.site.unregister(User)
admin.site.unregister(Group)


def get_fields_from_moddel(db_model):
    fields = []
    for field in db_model._meta.get_fields():
        if isinstance(field, ManyToOneRel):
            continue
        fields.append(field.name)
    return fields


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):

    list_display = get_fields_from_moddel(TelegramUser)
