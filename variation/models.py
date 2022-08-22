# from django.db import models

# # Create your models here.
# class VariationBase(models.Model):
#     label = models.CharField(max_length=255) 
  


# class Variation(models.Model):
#     base = models.ForeignKey('VariationBase', related_name='variations', on_delete=models.CASCADE)
#     value1 = models.CharField(max_length=255, null=True) 
#     value2 = models.CharField(max_length=255, null=True)
    
#     class Meta:
#         unique_together = ["value1", "value2"]
