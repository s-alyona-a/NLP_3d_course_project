from django.db import models

class Words(models.Model):
    word = models.TextField(max_length=15)
    lemma = models.TextField(max_length=15)
    pos = models.TextField(max_length=15)
    nmb_text = models.IntegerField()
    nmb_sent = models.IntegerField()
    nmb_word = models.IntegerField()

    def __str__(self):
        return self.content
    
    class Meta:
        app_label = 'myapp2'

class Sentences(models.Model):
    sentence = models.TextField()
    nmb_sent = models.IntegerField()
    author = models.TextField()
    title = models.TextField()
    nmb_text = models.IntegerField()

    def __str__(self):
        return self.content
    
    class Meta:
        app_label = 'myapp2'
