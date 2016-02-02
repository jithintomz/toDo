from django.shortcuts import render
import json
from helper import *
from taskmanager.models import *
from django.http import HttpResponse
import ast
from django.db.models import Q
# Create your views here.


def home(request):
    #poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'taskmanager/home.html')
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
		tagObjects = Tag.objects.filter(id__in=json.loads(request.body)["temptags"])
		newTask.tags.add(*(json.loads(request.body)["temptags"]))
	return JsonResponse({"added":tagstobeAdded,"deleted":tagstobeDeleted},status=200);
def get_tasks(request):
	requestObj = dict(request.GET)
	tasks = list(Task.objects.filter(Q(name__icontains = requestObj["q"][0])|Q(tags__name=requestObj["q"][0])).distinct().values())
	return JsonResponse({"tasks":tasks},status=200);

def remove_task(request):
	requestObj = json.loads(request.body)
	Task.objects.filter(id=requestObj["id"]).delete();
	return JsonResponse({"status":"success"},status=200);

def get_task(request,id):
	task = dict(Task.objects.values().get(id=id))
	tags=list(Task.tags.through.objects.filter(task_id=id).values_list("tag_id",flat=True))
	return JsonResponse({"task":task,"tags":tags},status=200);
def get_tag(request,id):
	tag = dict(Tag.objects.values("name","id").get(id=id))
	return JsonResponse({"tag":tag},status=200);

def get_tags(request):
	requestObj = dict(request.GET)
	tags = list(Tag.objects.all().values("name","id"))
	return JsonResponse({"tags":tags},status=200);

def create_tags(request):
 	requestObj = json.loads(request.body)
 	tags = list(requestObj['tags'].split(','))
 	tagObjects = [Tag(name=tag) for tag in tags]
 	Tag.objects.bulk_create(tagObjects)
 	tags = list(Tag.objects.all().values("name","id"))
	return JsonResponse({"tags":tags},status=200);

def update_or_delete_tag(request):
 	requestObj = json.loads(request.body)
 	if requestObj["action"] == "delete":
 		Tag.objects.filter(id=requestObj["tagdetails"]["id"]).delete();
 	if requestObj["action"] == "update":
 		Tag.objects.filter(id=requestObj["tagdetails"]["id"]).update(name=requestObj["tagdetails"]["name"])
	return JsonResponse({"status":"success"},status=200);

	
	  	


		

			
			



			


			








