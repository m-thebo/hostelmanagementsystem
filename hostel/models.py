from django.db import models

from django.contrib.auth.models import User

from user.models import Student, Admin


class Hostel(models.Model):
    HOSTEL_TYPE_CHOICES = [
        ('Boys', 'Boys'),
        ('Girls', 'Girls'),
    ]
    name = models.CharField(max_length=200)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    type = models.CharField(max_length=6, choices=HOSTEL_TYPE_CHOICES, default='Boys')

    def __str__(self):
        return self.name


class Wing(models.Model):
    name = models.CharField(max_length=200)
    hostel = models.ForeignKey(Hostel, related_name='wings', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Floor(models.Model):
    number = models.IntegerField()
    wing = models.ForeignKey(Wing, related_name='floors', on_delete=models.CASCADE)

    def __str__(self):
        return f'Floor {self.number}'


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    ]

    OCCUPANCY_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]

    number = models.CharField(max_length=200)
    room_type = models.CharField(max_length=6, choices=ROOM_TYPE_CHOICES, default='AC')
    occupancy = models.CharField(max_length=6, choices=OCCUPANCY_CHOICES, default='Single')
    floor = models.ForeignKey(Floor, related_name='rooms', on_delete=models.CASCADE)
    residents = models.ManyToManyField(Student, related_name='rooms', null=True)

    def __str__(self):
        return self.number


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='Pending')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.name}: {self.status}'


class Application(models.Model):
    ROOM_TYPE_CHOICES = [
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    ]

    OCCUPANCY_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=6, choices=ROOM_TYPE_CHOICES, default='AC')
    occupancy = models.CharField(max_length=6, choices=OCCUPANCY_CHOICES, default='Single')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.applicant.name}: {self.status}'
