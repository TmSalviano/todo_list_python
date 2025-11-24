from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#THe index is a list of the 5 latest to do items
def index(request):
    """
        This is 2 lists of the 5 latest not done and done todo items and you can create new 
        or delete the todo items and mark them as done which makes them disappear from the list
        when the todoitem is done or undone the pub_date is update to timezone.now().
    """
    return HttpResponse("Hello, world. This is a todo list")

def detail(request, todoitem_id):
    """
        Displays summary, todo_text and pub_date and also allows you to mark the todo item
        as done.
    """
    response = f"You are looking at details of {todoitem_id}"
    HttpResponse(response)
    
#This is a list with all of the todo items with a search bar at the top that matches
def all_items(request):
    """
        This is a long list with all of the todo items sorted by date with a search bar at the top 
        looking for matches with summary, todo_text, done and pub_dates. You can create or delete
        the todo items
    """
    HttpResponse("This is a list of all todo items with a search bar at the top")
    
def create(request):
    """
        This is the create view for todo items. It has a place to summarize, descrice the item and
        define the date and time of the item. 
    """

def delete(request, todoitem_id):
    """
        This is the delete view for the todo items. It shows a delete message containing the summary
        of the item
    """
    
#No need for a update view. Creating new correct todo items and deleting the previous bad ones is 
#simple enough
    
