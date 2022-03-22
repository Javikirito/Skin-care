from django.db import models

# Create your models here.
class login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=8)
    type = models.CharField(max_length=15)

    class Meta:
        db_table = "login"

class department(models.Model):
    department = models.CharField(max_length=50)

    class Meta:
        db_table = "department"

class disease(models.Model):
    disease = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = "disease"

class doctor(models.Model):
    name = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=15)
    qual = models.CharField(max_length=50)
    photo = models.CharField(max_length=150)
    place = models.CharField(max_length=30)
    pin = models.CharField(max_length=10)
    post = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    DEPARTMENT = models.ForeignKey(department,on_delete=models.CASCADE,default=1)
    contact = models.CharField(max_length=15)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE,default=1)

    class Meta:
        db_table = "doctor"

class schedule(models.Model):
    DEPARTMENT = models.ForeignKey(department, on_delete=models.CASCADE, default=1)
    DOCTOR = models.ForeignKey(doctor,on_delete=models.CASCADE,default=1)
    date = models.CharField(max_length=15)
    time = models.CharField(max_length=15)
    timeto = models.CharField(max_length=15)

    class Meta:
        db_table = "schedule"

class symptoms(models.Model):
    sympt = models.CharField(max_length=80)

    class Meta:
        db_table = "symptoms"

class user(models.Model):
    name = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=10)
    place = models.CharField(max_length=20)
    pin = models.CharField(max_length=10)
    post = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    email = models.CharField(max_length=20)
    photo = models.CharField(max_length=150)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE,default=1)

    class Meta:
        db_table = "user"


class feedback(models.Model):
    date = models.CharField(max_length=15)
    DOCTOR = models.ForeignKey(doctor, on_delete=models.CASCADE, default=1)
    USER = models.ForeignKey(user,on_delete=models.CASCADE,default=1)
    feedback = models.CharField(max_length=150)
    rating = models.CharField(max_length=10)

    class Meta:
        db_table = "feedback"


class booking(models.Model):

    USER = models.ForeignKey(user,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    SCHEDULE = models.ForeignKey(schedule,on_delete=models.CASCADE)

    class Meta:
        db_table = "booking"


class payment(models.Model):
    date = models.DateField(max_length=15)
    amount = models.CharField(max_length=30)
    BOOKING = models.ForeignKey(booking,on_delete=models.CASCADE,default=1)

    class Meta:
        db_table = "payment"


class chat(models.Model):
    date = models.CharField(max_length=15)
    message = models.CharField(max_length=150)
    LOGINFROM=models.ForeignKey(login,on_delete=models.CASCADE,default=1,related_name="loginfrom")
    LOGINTO=models.ForeignKey(login,on_delete=models.CASCADE,default=1,related_name="loginto")
    class Meta:
        db_table = "chat"







