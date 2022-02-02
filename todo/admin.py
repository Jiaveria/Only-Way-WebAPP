from django.contrib import admin
# Register your models here.
from .models import islamicarticle,Quiz,Hadith,QuranicVerse


admin.site.register(islamicarticle)
admin.site.register(Quiz)
admin.site.register(QuranicVerse)
admin.site.register(Hadith)