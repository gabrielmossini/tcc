from django.db import models

class DetectionEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    class_name = models.CharField(max_length=64)
    confidence = models.FloatField()
    track_id = models.IntegerField(null=True, blank=True)
    camera_id = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']


class ViolationEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    class_name = models.CharField(max_length=64)
    camera_id = models.CharField(max_length=64, null=True, blank=True)
    frame_count = models.IntegerField(default=1)

    class Meta:
        ordering = ['-timestamp']
