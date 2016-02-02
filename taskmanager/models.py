from django.db import models

# Create your models here


class Tag(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True);


class Task(models.Model):
    name = models.CharField(blank=True, null=True,max_length=250);
    description = models.TextField(blank=True, null=True);
    isCompleted = models.NullBooleanField(blank=True,null=True,default=False)
    dueDate = models.DateTimeField(null=True,blank=True)
    tags = models.ManyToManyField(Tag)

    