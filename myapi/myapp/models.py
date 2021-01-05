from __future__ import unicode_literals

from django.db import models
from django.db.models import signals

class Item(models.Model):
    name = models.CharField("Name", max_length=20)
    points = models.PositiveIntegerField("Points", null = True)
    quantity = models.PositiveIntegerField("Quantity", default=0)
    
    class Meta:
        verbose_name = u'Item'
        verbose_name_plural = u'Items'
        
    def __str__(self):
        return self.name

class Inventory(models.Model):

    '''survivor = models.OneToOneField(Survivor, verbose_name='Survivor', on_delete=models.CASCADE)'''
    items = models.ManyToManyField(Item)

    class Meta:
        verbose_name = u'Inventory'
        verbose_name_plural = u'Inventories'

    def __str__ (self):
        return self.inventory 

class Survivor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    is_infected = models.BooleanField()
    count_reports = models.IntegerField(default=0)
    inventory = models.ForeignKey(Inventory, null=True, on_delete=models.CASCADE)


        
    def __str__(self):
        return self.name
  
def survivor_pre_save(signal, instance, sender, **kwargs):
    if instance.inventory_id is not None:
        items = []
        for item in instance.inventory.items.all():
            items.append(item.name)
        if not "Water" in items:
            water = Item.objects.create(name="Water", points=4, quantity=0)
            instance.inventory.items.add(water)
        if not "Food" in items:
            food = Item.objects.create(name="Food", points=3)
            instance.inventory.items.add(food)
        if not "Medication" in items:
            medication = Item.objects.create(name="Medication", points=2)
            instance.inventory.items.add(medication)
        if not "Ammunition" in items:
            ammunition = Item.objects.create(name="Ammunition", points=1)
            instance.inventory.items.add(ammunition)
    else:
        if instance.infected == True or instance.reported_infected > 0:
            raise Exception("Impossible to register zombies!")

signals.pre_save.connect(survivor_pre_save, sender=Survivor)

