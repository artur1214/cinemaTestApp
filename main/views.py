import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import Cinema, Schedule
from .forms import CinemaAddForm, ScheduleAddForm
import json


class AddCinemaApiView(View):
    def post(self, request: WSGIRequest):
        title = request.POST.get('title')
        adress = request.POST.get('adress')
        print(title)
        form = CinemaAddForm(request.POST)
        print(request.POST['title'])
        if form.is_valid():
            if Cinema.objects.filter(Q(title=title)).count():
                return JsonResponse({'ok': False, 'error': 'Кинотеатр с таким названием уже существует'})
            elif Cinema.objects.filter(Q(title=title)).count():
                return JsonResponse({'ok': False, 'error': 'Кинотеатр с таким адресом уже существует'})
            else:
                Cinema(title=title, adress=adress).save()
                if Cinema.objects.filter(title=form.cleaned_data['title'], adress=form.cleaned_data['adress']).count():
                    return JsonResponse({'ok': True})
                else:
                    return JsonResponse({'ok': False, 'error': 'Непредвиденная ошибка сервера.'})
        else:
            print(form.errors)
            return JsonResponse({'ok': False, 'error': form.errors})


class CinemaAddView(View):
    def get(self, request):
        return render(request, 'main/cinemaAdd.html', {'form': CinemaAddForm()})


class CinemaView(View):
    def get(self, request):
        cinemas = Cinema.objects.all()[:15]
        return render(request, 'main/cinemaView.html', {'show': cinemas})


class ScheduleAddView(View):
    def get(self, request):
        return render(request, 'main/scheduleAdd.html', {'form': ScheduleAddForm()})


class AddScheduleApiView(View):
    def post(self, request: WSGIRequest):
        form = ScheduleAddForm(request.POST)
        if form.is_valid():
            Schedule(title=form.cleaned_data['title'],
                     date_time=form.cleaned_data['date_time'],
                     cinema=form.cleaned_data['cinema']).save()
            if Schedule.objects.filter(title=form.cleaned_data['title'],
                                       date_time=form.cleaned_data['date_time'],
                                       cinema=form.cleaned_data['cinema']).count():
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'error': 'Непредвиденная ошибка сервера.'})
        else:
            return JsonResponse({'ok': False, 'error': form.errors})


class MainView(View):
    def get(self, request: WSGIRequest):
        return render(request, 'main/index.html', )


class ScheduleView(View):
    def get(self, request: WSGIRequest):
        cinema_list = Cinema.objects.all()
        if 'date' in request.GET.keys():
            date = request.GET['date']
        else:
            date = str(datetime.date.today())
        if 'cinema' in request.GET.keys():
            cinema_id = int(request.GET['cinema'])
        else:
            cinema_id = ''
        if cinema_id in Cinema.objects.values_list('id', flat=True):
            films = Schedule.objects.filter(date_time__date=date, cinema_id=cinema_id).all()
        else:
            films = Schedule.objects.filter(date_time__date=date).all()
        return render(request, 'main/scheduleView.html', {'date': date, 'films': films,
                                                          'cinema_id': cinema_id, 'cinema_list': cinema_list})


class ScheduleDeleteView(View):
    def post(self, request: WSGIRequest):
        json_dict = json.loads(request.body)
        Schedule.objects.get(id=int(json_dict['id'])).delete()
        return JsonResponse({'ok': True})


class CinemaUpdateView(View):
    def post(self, request: WSGIRequest):
        json_dict = json.loads(request.body)
        if json_dict['del']:
            try:
                Cinema.objects.get(id=int(json_dict['id'])).delete()
                return JsonResponse({'ok': True})
            except Schedule.DoesNotExist as e:
                return JsonResponse({'ok': False})
        else:
            form = CinemaAddForm({'title': json_dict['title'], 'adress': json_dict['adress']})
            if form.is_valid():
                cinema = Cinema.objects.get(id=int(json_dict['id']))
                cinema.title = json_dict['title']
                cinema.adress = json_dict['adress']
                cinema.save()
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'error': form.errors})
