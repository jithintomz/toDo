from django.shortcuts import render
import json
from helper import *
from taskmanager.models import *
from django.http import HttpResponse
import ast
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from guardian.models import UserObjectPermission
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from guardian.decorators import *
from guardian.shortcuts import *

# Create your views here.

@login_required
def home(request):
    #poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'taskmanager/home.html')


@login_required
def create_or_update_task(request):
	taskDetails = json.loads(request.body)["taskdetails"]
	tagstobeAdded = []
	tagstobeDeleted  = []
	if "id" in taskDetails:
		task=Task.objects.get(pk=taskDetails["id"])
		task.name = taskDetails["name"]
		task.description = taskDetails.get("description","")
		task.isCompleted = taskDetails.get("isCompleted",False)
		task.dueDate = taskDetails.get("dueDate")
		task.save()
		tagstobeAdded = list(set(json.loads(request.body)["temptags"])-set(json.loads(request.body)["currenttags"]))
		tagstobeDeleted = list(set(json.loads(request.body)["currenttags"])-set(json.loads(request.body)["temptags"]))
		task.tags.add(*(tagstobeAdded))
		task.tags.remove(*(tagstobeDeleted))
	else:
		newTask = Task.objects.create(name = taskDetails["name"],description = taskDetails.get("description",""),isCompleted = taskDetails.get("iscompleted",False))
		assign_perm("change_task",request.user,newTask)
		print "permissions"
		print get_perms(request.user,newTask)
		tagObjects = Tag.objects.filter(id__in=json.loads(request.body)["temptags"])
		newTask.tags.add(*(json.loads(request.body)["temptags"]))
	return JsonResponse({"added":tagstobeAdded,"deleted":tagstobeDeleted},status=200);

@login_required
def get_tasks(request):
	requestObj = dict(request.GET)
	tasks = get_objects_for_user(request.user,"change_task",klass = Task)
	tasks = list(tasks.filter(Q(name__icontains = requestObj["q"][0])|Q(tags__name=requestObj["q"][0])).distinct().values())
	return JsonResponse({"tasks":tasks},status=200);

@require_POST
@permission_required_or_403("change_task",("taskmanager.Task","id","id"))
def remove_task(request,id):
	requestObj = json.loads(request.body)
	Task.objects.filter(id=requestObj["id"]).delete();
	return JsonResponse({"status":"success"},status=200);

@permission_required_or_403("change_task",("taskmanager.Task","id","id"))
def get_task(request,id):
	task = dict(Task.objects.values().get(id=id))
	tags=list(Task.tags.through.objects.filter(task_id=id).values_list("tag_id",flat=True))
	return JsonResponse({"task":task,"tags":tags},status=200);

@login_required
def get_tag(request,id):
	tag = dict(Tag.objects.values("name","id").get(id=id))
	return JsonResponse({"tag":tag},status=200);

@login_required
def get_tags(request):
	requestObj = dict(request.GET)
	tags = list(Tag.objects.all().values("name","id"))
	return JsonResponse({"tags":tags},status=200);

@login_required
def create_tags(request):
 	requestObj = json.loads(request.body)
 	tags = list(requestObj['tags'].split(','))
 	tagObjects = [Tag(name=tag) for tag in tags]
 	Tag.objects.bulk_create(tagObjects)
 	tags = list(Tag.objects.all().values("name","id"))
	return JsonResponse({"tags":tags},status=200);

@login_required
def update_or_delete_tag(request):
 	requestObj = json.loads(request.body)
 	if requestObj["action"] == "delete":
 		Tag.objects.filter(id=requestObj["tagdetails"]["id"]).delete();
 	if requestObj["action"] == "update":
 		Tag.objects.filter(id=requestObj["tagdetails"]["id"]).update(name=requestObj["tagdetails"]["name"])
	return JsonResponse({"status":"success"},status=200);


	
	  	


		

			
			



			


			








