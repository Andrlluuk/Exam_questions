from django.db import models
from jsonfield import JSONField

class File(models.Model):
    filename = models.CharField(max_length=200)
    title = models.TextField()
    stats = JSONField()
    questions_pool = JSONField()

    def __str__(self):
        return str(self.filename)







