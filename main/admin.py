from django import forms
from django.contrib import admin
from .models import Cinema, Schedule


# Register your models here.

class CinemaAdmin(admin.ModelAdmin):
    class CinemaForm(forms.ModelForm):
        class Meta:
            model = Cinema
            fields = 'title', 'adress'

    def save_model(self, request, obj, form, change):
        pass

    list_display = ('title', 'adress')


class ScheduleAdmin(admin.ModelAdmin):
    class ScheduleForm(forms.Form):
        class Meta:
            #model = Schedule
            fields = 'title', 'date_time', 'cinema'
    def save_model(self, request, obj, form, change):
        pass


admin.AdminSite.site_header = 'Быстрый набросок сайта про кинотеатры за 2 часа'

admin.site.register(Cinema, CinemaAdmin)
admin.site.register(Schedule, ScheduleAdmin)
