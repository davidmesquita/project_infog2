from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from .models import Survivor
from .survivors import SURVIVOR_1_POST, SURVIVOR_2_POST, SURVIVOR_3_POST, SURVIVOR_4_POST, SURVIVOR_ERROR_POST, ZOMBIE_POST
import json


TRADE_ITEMS_POST = [
{
    "id": 1,
    "survivor_1": {
        "trade_item": {
            "Water": 1,
            "Ammunition": 4
        }
    }
},
{
    "id": 2,
    "survivor_2": {
        "trade_item": {
            "Water": 1,
            "Ammunition": 4
        }
    }
}
]

# Create your tests here.
class Test(TestCase):

    def create_survivor(self, SURVIVOR_POST):
        response = self.client.post(
            reverse('survivor_create'),
            data=json.dumps(SURVIVOR_POST),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        survivor = Survivor.objects.get(name=SURVIVOR_POST["name"])
class SurvivorTest(Test):

    def test_create_survivors(self):
        self.create_survivor(SURVIVOR_1_POST)
        self.create_survivor(SURVIVOR_2_POST)
        self.create_survivor(SURVIVOR_3_POST)
        survivors = Survivor.objects.all()
        self.assertEqual(3, survivors.count())
        survivor = survivors.first()
        self.assertEqual("Joaquina", survivor.name)
        self.assertEqual(23, survivor.age)
        self.assertEqual("F", survivor.gender)
        self.assertEqual(Decimal('51.261236710000000000000000'), survivor.last_location.latitude)
        self.assertEqual(Decimal('11.123412300000000000000000'), survivor.last_location.longitude)
        self.assertEqual(4, survivor.inventory.items.get(name="Water").points)
        self.assertEqual(10, survivor.inventory.items.get(name="Water").quantity)
        self.assertEqual(3, survivor.inventory.items.get(name="Food").points)
        self.assertEqual(5, survivor.inventory.items.get(name="Food").quantity)
        self.assertEqual(2, survivor.inventory.items.get(name="Medication").points)
        self.assertEqual(8, survivor.inventory.items.get(name="Medication").quantity)
        self.assertEqual(1, survivor.inventory.items.get(name="Ammunition").points)
        self.assertEqual(15, survivor.inventory.items.get(name="Ammunition").quantity)
        self.assertEqual(False, survivor.infected)
        self.assertEqual(0, survivor.reported_infected)

    def test_error_create_survivors(self):
        response = self.client.post(
            reverse('survivor_create'),
            data=json.dumps(SURVIVOR_ERROR_POST),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_error_create_zombie(self):
        with self.assertRaises(Exception):
            self.client.post(
                reverse('survivor_create'),
                data=json.dumps(ZOMBIE_POST),
                content_type='application/json'
            )

    def test_get_all_survivors(self):
        self.create_survivor(SURVIVOR_1_POST)
        self.create_survivor(SURVIVOR_2_POST)
        self.create_survivor(SURVIVOR_3_POST)
        response = self.client.get(reverse('survivor_create'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Joaquina", response.content.decode())
        self.assertIn("David", response.content.decode())
        self.assertIn("Jhenifer", response.content.decode())

    def test_get_survivor(self):
        survivor = self.create_survivor(SURVIVOR_1_POST)
        response = self.client.get(reverse('survivor_detail', kwargs={"pk": survivor.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("Joaquina", survivor.name)
        self.assertIn("Joaquina", response.content.decode())

    def test_error_get_survivor_inexistent(self):
        response = self.client.get(reverse('survivor_detail', kwargs={"pk": 1}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        return survivor

class TradeItemsTest(Test):

    def test_trade_items(self):
        survivor_1 = self.create_survivor(SURVIVOR_1_POST)
        survivor_2 = self.create_survivor(SURVIVOR_2_POST)
        self.assertEqual(20, survivor_1.inventory.items.get(name="Water").quantity)
        self.assertEqual(9, survivor_1.inventory.items.get(name="Food").quantity)
        self.assertEqual(6, survivor_1.inventory.items.get(name="Medication").quantity)
        self.assertEqual(19, survivor_1.inventory.items.get(name="Ammunition").quantity)
        self.assertEqual(5, survivor_2.inventory.items.get(name="Water").quantity)
        self.assertEqual(20, survivor_2.inventory.items.get(name="Food").quantity)
        self.assertEqual(6, survivor_2.inventory.items.get(name="Medication").quantity)
        response = self.client.patch(
        self.assertEqual(20, survivor_2.inventory.items.get(name="Ammunition").quantity),
            reverse ('trade_items', kwargs={"pk_sur_1": surviro_1.id, "pk_sur_2": survivor_2.id}),
            data=json.dumps(TRADE_ITEMS_POST),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        survivor_1.refresh_from_db()
        survivor_2.refresh_from_db()
        self.assertEqual(9, survivor_1.inventory.items.get(name="Water").quantity)
        self.assertEqual(6, survivor_1.inventory.items.get(name="Food").quantity)
        self.assertEqual(7, survivor_1.inventory.items.get(name="Medication").quantity)
        self.assertEqual(18, survivor_1.inventory.items.get(name="Ammunition").quantity)
        self.assertEqual(6, survivor_2.inventory.items.get(name="Water").quantity)
        self.assertEqual(9, survivor_2.inventory.items.get(name="Food").quantity)
        self.assertEqual(7, survivor_2.inventory.items.get(name="Medication").quantity)
        self.assertEqual(17, survivor_2.inventory.items.get(name="Ammunition").quantity)

    def test_error_zombie_trade_items(self):
        survivor_1 = self.create_survivor(SURVIVOR_1_POST)
        survivor_1.infected = True
        survivor_1.reported_infected = 3
        survivor_1.save()
        survivor_2 = self.create_survivor(SURVIVOR_2_POST)
        with self.assertRaises(Exception):
            self.client.patch(
                reverse('trade_items', kwargs={"pk_sur_1": survivor_1.id, "pk_sur_2": survivor_2.id}),
                data=json.dumps(TRADE_ITEMS_POST),
                content_type='application/json'
            )

    def test_error_miss_item_trade_items(self):
        survivor_1 = self.create_survivor(SURVIVOR_1_POST)
        survivor_2 = self.create_survivor(SURVIVOR_4_POST)
        with self.assertRaises(Exception):
            self.client.patch(
                reverse('trade_items', kwargs={"pk_sur_1": survivor_1.id, "pk_sur_2": survivor_2.id}),
                data=json.dumps(TRADE_ITEMS_POST),
                content_type='application/json'
            )

    def test_error_diff_points_trade_items(self):
        survivor_1 = self.create_survivor(SURVIVOR_1_POST)
        survivor_2 = self.create_survivor(SURVIVOR_2_POST)
        with self.assertRaises(Exception):
            self.client.patch(
                reverse('trade_items', kwargs={"pk_sur_1": survivor_1.id, "pk_sur_2": survivor_2.id}),
                data=json.dumps(ERROR_TRADE_ITEMS_POST),
                content_type='application/json'
            )

