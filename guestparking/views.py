import base64

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from guestparking.models import Flat, Car


@login_required
def park(request, hash):
    flat = Flat.objects.filter(hash=hash).first()
    cars_error = False
    if request.method == 'POST':
        plate = request.POST['plate'].upper()
        cars = Car.objects.filter(parked=True).count()
        car = Car.objects.filter(plate=plate).first()
        if cars >= 2 or car:
            cars_error = True
        else:
            time = timezone.now()
            car = Car.objects.create(flat=flat, plate=plate, starttime=time)
            url = request.get_host() + reverse('leave', args=[hash, car.pk])
            email = EmailMessage()
            email.to = [flat.email]
            email.subject = 'Auto geparkt'
            email.from_email = settings.FROM_EMAIL
            body = 'Das Auto mit der Nummer {} wurde um {} parkiert' \
                   '\n hier kann es wieder ausgetragen werden' \
                   '\n {}'.format(plate, time, url)
            password=settings.SECRET_KEY.encode()
            password += b'='*(32-len(password))
            password = password[:32]
            key = Fernet(base64.b64encode(password))
            encrypted = key.encrypt(body.encode()).decode()
            email.body = '{}' \
                         '\n Signatur\n{}'.format(body, encrypted)
            email.send()
            return redirect(reverse('success', args=[car.pk]))
    return render(request, 'park.html', {'cars_error': cars_error})

@login_required
def success(request, carid):
    car = get_object_or_404(Car, pk=carid)
    return render(request, 'success.html', {'plate': car.plate})

@login_required
def leave(request, hash, carid):
    flat = Flat.objects.filter(hash=hash).first()
    car = flat.car_set.filter(id=carid, parked=True).first()
    if car:
        plate = car.plate
        time = timezone.now()
        car.parked = False
        car.blocked = True
        car.endtime = time
        car.save()
        email = EmailMessage()
        email.to = [flat.email]
        email.subject = 'Auto weggefahren'
        email.from_email = settings.FROM_EMAIL
        body = 'Das Auto mit der Nummer {} wurde um {} ausgetragen'.format(plate, time)
        password = settings.SECRET_KEY.encode()
        password += b'=' * (32 - len(password))
        password = password[:32]
        key = Fernet(base64.b64encode(password))
        encrypted = key.encrypt(body.encode()).decode()
        email.body = '{}' \
                     '\n Signatur\n{}'.format(body, encrypted)
        email.send()
        return render(request,'leave.html', {'plate': plate})
    return render(request, 'alreadyleft.html')


@login_required
def all(request):
    cars = Car.objects.filter(parked=True).all()
    return render(request, 'cars.html', {'cars': cars})


@login_required
def check(request):
    decoded = ''
    if request.method == 'POST':
        sign = request.POST['sign']
        password=settings.SECRET_KEY.encode()
        password += b'='*(32-len(password))
        password = password[:32]
        key = Fernet(base64.b64encode(password))
        decoded = key.decrypt(sign.encode()).decode()
    return render(request, 'check.html', {'decoded': decoded})
