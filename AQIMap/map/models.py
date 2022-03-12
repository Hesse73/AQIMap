from django.db import models
import jsonfield

# Create your models here.
class AqiData(models.Model):
    record_time = models.FloatField()
    aqi_data = jsonfield.JSONField()
    
    @classmethod
    def init_data(cls, data, time):
        aqi_data_object = cls(aqi_data=data, record_time=time)
        aqi_data_object.save()
        return aqi_data_object

    def update(self,data,time):
        self.aqi_data = data
        self.record_time = time
        self.save()

