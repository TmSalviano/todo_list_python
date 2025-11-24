from django.db import models

# Create your models here.
class TodoItem(models.Model):
    summary = models.CharField(100)
    todo_text = models.TextField(verbose_name="todo text")
    pub_date = models.DateTimeField(verbose_name="date published")