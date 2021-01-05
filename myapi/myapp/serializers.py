from rest_framework import serializers
from .models import Survivor, Inventory, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'points', 'quantity']

class InventorySerializer(serializers.ModelSerializer):
  
    items = ItemSerializer(many=True)

    class Meta:
        model = Inventory
        fields = ['id', 'items']

class SurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = '__all__'

    def validate_items(self, item, survivor, inventory):
        if item.name == "Water":
            item.points = 4
        elif item.name == "Food":
            item.points = 3
        elif item.name == "Medication":
            item.points = 2
        elif item.name == "Ammunition":
            item.points = 1
        else:
            survivor.delete()
            inventory.delete()
            item.delete()
            raise Exception("Wrong item!")

    def create(self, validated_data):
        items_data = validated_data.pop('inventory')
        survivor = Survivor.objects.create(**validated_data)
        inventory = Inventory.objects.create()
        for item_data in items_data['items']:
            item = Item.objects.create(**item_data)
            self.validate_items(item, survivor,inventory)
            item.save()
            inventory.items.add(item)
        survivor.inventory_id = inventory.id
        survivor.save()
        return survivor
        

class Survivor_LocationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Survivor
        fields = ('longitude', 'latitude')
    
