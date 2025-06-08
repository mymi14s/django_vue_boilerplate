from datetime import datetime
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db.models.fields.files import ImageFieldFile

# Create your models here.

class Setting(models.Model):
    """ User profile model."""
    id = models.CharField(max_length=50, primary_key=True)
    site_name = models.CharField(max_length=50)
    site_title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        count= Setting.objects.all().count()
        if count>1:
            raise ValidationError("This is a single data model, you cannot add more than 1 record.")
        super(Setting, self).save(*args, **kwargs)
    

    def as_dict(self, fields=None):
            
        obj_dict = model_to_dict(self, fields=fields)

        for k, v in obj_dict.items():
            if isinstance(v, datetime):
                obj_dict[k] = str(v)
            if isinstance(v, ImageFieldFile):
                if v:
                    obj_dict[k] = v.url
                else:
                    obj_dict[k] = ''
        
        return obj_dict
