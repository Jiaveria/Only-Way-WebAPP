from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE



class islamicarticle(models.Model):
      article_ID = models.AutoField(primary_key=True)
      title=models.CharField(max_length=100)
      article_slug=models.CharField(max_length=100)
      article_meta=models.TextField(max_length=500)
      bcontent = models.TextField(max_length=15000)
      created_at=models.DateTimeField(default=datetime.now,blank=True)

class Quiz(models.Model):
      questionID=models.AutoField(primary_key=True)
      question=models.CharField(max_length=250)
      op1=models.CharField(max_length=200)
      op2=models.CharField(max_length=200)
      op3=models.CharField(max_length=200)
      op4=models.CharField(max_length=200)
      correctop=models.CharField(max_length=200)

class Hadith(models.Model):
      Hadith_ID=models.AutoField(primary_key=True)
      ArabicText=models.CharField(max_length=2500)
      HAdith_Trans=models.CharField(max_length=1000)
      Hadith_Topic=models.CharField(max_length=300)
      Hadith_referenece=models.CharField(max_length=250)

class QuranicVerse(models.Model):
      QuranicVerse_ID=models.AutoField(primary_key=True)
      ArabicText=models.CharField(max_length=2500)
      Quranic_Trans=models.CharField(max_length=1000)
      Quranic_Topic=models.CharField(max_length=300)
      Quranic_reference=models.CharField(max_length=250)




    

