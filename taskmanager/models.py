from django.db import models
from django.contrib.auth.models import User as auth_user,Group
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here

@receiver(post_save,sender = auth_user)
def add_to_group(sender,**kwargs):
	print "recieved signal"
	if kwargs["created"] == True:
			kwargs["instance"].groups.add(Group.objects.get_or_create(name = "managers")[0].id)

class Employee(models.Model):
	user  = models.OneToOneField(auth_user,primary_key=True)
	designation = models.CharField(max_length=40)


class Tag(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True);


class Task(models.Model):
    name = models.CharField(blank=True, null=True,max_length=250);
    description = models.TextField(blank=True, null=True);
    isCompleted = models.NullBooleanField(blank=True,null=True,default=False)
    dueDate = models.DateTimeField(null=True,blank=True)
    tags = models.ManyToManyField(Tag)

    