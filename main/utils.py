from django.template.defaultfilters import slugify as django_slugify
from random import randint
from django.db import models

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

def create_code(length = 4):
    code = ''
    for i in range(4):
        code += str(randint(0,9))
    return code

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class ContactsChoices(models.TextChoices):
    WHATSAPP = 'whatsapp'
    INSTAGRAM = 'instagram'
    TELEGRAM = 'telegram'
    VK = 'vk'
    YOUTUBE = 'youtube'
    AVITO = 'avito'