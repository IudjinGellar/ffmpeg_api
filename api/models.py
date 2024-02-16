from django.db import models
import uuid


class VideoFileModel(models.Model):
    class Processing(models.IntegerChoices):
        initial = 1
        processing = 2
        end = 3

    class ProcessingSucces(models.TextChoices):
        null = 'null'
        true = 'true'
        false = 'false'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    filename = models.CharField(default='no_name', max_length=50)
    process_status = models.IntegerField(choices=Processing.choices,
                                         default=Processing.initial)
    processing_success = models.CharField(max_length=10,
                                          choices=ProcessingSucces.choices,
                                          default=ProcessingSucces.null)
    file = models.FileField(upload_to='media/', editable=True)

    def __str__(self):
        return f'{self.id}: {self.filename}'
