from django import forms

from .models import Cinema, Schedule


class CinemaAddForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ('title', 'adress')

    widgets = {
        'title': forms.CharField(max_length=40, ),
        'adress': forms.CharField(max_length=250, )
    }

    def __init__(self, *args, **kwargs):
        super(CinemaAddForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
            # self.fields[key].label = 'asdsdd'

    def clean_title(self):
        if self.cleaned_data['title'] == '':
            raise forms.ValidationError("Вы забыли про название кинотеатра")
        return self.cleaned_data['title']

    def clean_adress(self):
        if self.cleaned_data['adress'] == '':
            raise forms.ValidationError("Вы забыли указать адрес")
        return self.cleaned_data['adress']


class ScheduleAddForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = (
            'title',
            'date_time',
            'cinema'
        )

    def __init__(self, *args, **kwargs):
        super(ScheduleAddForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            pass
            self.fields[key].required = False
        self.fields['date_time'].label = ''
        self.fields['cinema'].widget.attrs = {'id': 'id_cinema_pick'}

    def clean_title(self):
        if self.cleaned_data['title'] == '':
            raise forms.ValidationError("Введите название фильма")
        return self.cleaned_data['title']

    def clean_date_time(self):
        if self.cleaned_data['date_time'] is None:
            raise forms.ValidationError('Пожалуйста, укажите дату сеанса')
        return self.cleaned_data['date_time']

    def clean_cinema(self):
        if self.cleaned_data['cinema'] is None:
            raise forms.ValidationError('Укажите место проведения фильма')
        return self.cleaned_data['cinema']

