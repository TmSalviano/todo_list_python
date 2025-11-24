from django.db import models
from django.utils.timezone import now

# Create your models here.
class TodoItem(models.Model):
    summary = models.CharField(max_length=100)
    todo_text = models.TextField()
    pub_date = models.DateTimeField(verbose_name="date published")
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.summary