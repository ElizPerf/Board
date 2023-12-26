from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField



class Notice(models.Model):
    TYPE = (
        ('Tanks', 'Tanks'),
        ('Healers', 'Healers'),
        ('DD', 'DD'),
        ('Traders', 'Traders'),
        ('Guidemasters', 'Guidemasters'),
        ('Smiths', 'Smiths'),
        ('Tanners', 'Tanners'),
        ('PotionMasters', 'PotionMasters'),
        ('Spellmasters', 'Spellmasters'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=18, choices=TYPE, default='Tanks')
    title = models.TextField()
    text = RichTextUploadingField(config_name='special', null=True)

    def get_absolute_url(self):
        return reverse('notice', args=[str(self.id)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = self.request.user
        super().save(*args, **kwargs)


class Response(models.Model):

    STATUS = (
        ('undefined', 'Неопределенный'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='undefined')




