from django.db import models

# Create your models here.
class mmodel(models.Model):
    name=models.CharField(max_length=100)
    used=models.CharField(max_length=100)
    mg=models.CharField(max_length=100)
    dosage=models.CharField(max_length=100)
    cmp=models.CharField(max_length=100)
    effects=models.CharField(max_length=100)
    pres=models.CharField(max_length=100)
    pack=models.CharField(max_length=100)
    image=models.FileField(upload_to="media")

    class Meta:
        db_table="med_details"

from django.db import models

class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    feedback = models.CharField(max_length=100)
    fdate = models.DateField()

    class Meta:
        db_table = "feedback"
