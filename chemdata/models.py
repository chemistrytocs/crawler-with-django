from django.db import models

# Create your models here.
class Compound(models.Model):
    code = models.CharField(max_length =50)
    maker = models.CharField(max_length =50)
    name = models.CharField(max_length =50)
    pury = models.CharField(max_length =50)
    cas = models.CharField(max_length =50)
    pack = models.CharField(max_length =50)
    price = models.IntegerField()
    stock =  models.CharField(max_length =50)

    def __str__(self):
        return "{0}:{1}@{2}".format(self.cas,self.code,self.maker)
    
    def entry(self,elem):
        for i in elem.keys():
            setattr(self,i,elem[i])