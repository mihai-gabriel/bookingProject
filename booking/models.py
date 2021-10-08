from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('booking:hotel', kwargs={'pk': self.pk})


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    description = models.TextField()
    number = models.PositiveIntegerField()
    available = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return "Hotel {} - Room: {}".format(self.hotel.name, self.number)

    def get_absolute_url(self):
        return reverse('booking:room', kwargs={'pk': self.pk})


class Order(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    number_of_people = models.IntegerField(default=0)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self):
        return "Order {} - {}".format(self.pk, self.room)

    def get_price(self):
        return self.number_of_people * self.room.price
