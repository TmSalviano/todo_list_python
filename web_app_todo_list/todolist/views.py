from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from todolist.models import TodoItem

# Create your views here.

#THe index is a list of the 5 latest to do items
def index(request):
    """
        This is 2 lists of the 5 latest not done and done todo items and you can create new 
        or delete the todo items and mark them as done which makes them disappear from the list
        when the todoitem is done or undone the pub_date is update to timezone.now().
    """
    latest5_done = TodoItem.objects.filter(done=True).order_by("-pub_date")[:5]
    latest5_not_done = TodoItem.objects.filter(done=False).order_by("-pub_date")[:5]
    context = { "latest5_done" : latest5_done, "latest5_not_done" : latest5_not_done}
    return render(request, "todolist/index.html", context)

def detail(request, todoitem_id):
    """
        Displays summary, todo_text and pub_date and also allows you to mark the todo item
        as done.
    """
    try:
        todoitem = TodoItem.objects.get(pk=todoitem_id)
    except TodoItem.DoesNotExist:
        raise Http404("Todo Item does not exist")
    return render(request, "todolist/detail.html", { "todoitem" : todoitem})
    
#This is a list with all of the todo items with a search bar at the top that matches
def all_items(request):
    """
        This is a long list with all of the todo items sorted by date with a search bar at the top 
        looking for matches with summary, todo_text, done and pub_dates. You can create or delete
        the todo items
    """
    return HttpResponse("This is a list of all todo items with a search bar at the top")
    
def create(request):
    """
        This is the create view for todo items. It has a place to summarize, descrice the item and
        define the date and time of the item. 
    """
    return HttpResponse("Here I create todo items")

def delete(request, todoitem_id):
    """
        This is the delete view for the todo items. It shows a delete message containing the summary
        of the item
    """
    return HttpResponse("Here I delete todo items")
    
#No need for a update view. Creating new correct todo items and deleting the previous bad ones is 
#simple enough
    
