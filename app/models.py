from django.db import models

class Master (models.Model):
    STATUS = [
        (0,"deleted"),
        (1,"active")
    ]

    IS_COMPLETED = [
        (0,"No"),
        (1,"Yes")
    ]
    unique_id  = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, null=True, blank = True)
    description  = models.TextField(null=True, blank = True)
    status = models.IntegerField(choices=STATUS, default=1)
    is_completed = models.IntegerField(choices=IS_COMPLETED, default=0) 

    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    updated_timestamp = models.DateTimeField(blank=True, null=True)
    removed_timestamp = models.DateTimeField(blank=True, null=True)
    removed_by = models.CharField(max_length=50, null=True)

    class Meta:
        managed = True
        db_table = 'task_master'
