from django.db import models
from jsonfield import JSONField

class File(models.Model):
    uuid = models.CharField(max_length=200, default = "none")
    filename = models.CharField(max_length=200)
    title = models.TextField()
    stats = JSONField()
    questions_pool = JSONField(default = {})
    params = JSONField(default = '{}')
    tickets = models.IntegerField(default = 5)
    output_format = models.CharField(max_length=200, default='PDF')

    def __str__(self):
        return str(self.filename)







