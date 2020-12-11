from django.db import models


class Cinema(models.Model):
    """Кинотеатры"""
    title = models.CharField('Название', max_length=40)
    adress = models.CharField('Адрес', max_length=250)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Кинотеатр'
        verbose_name_plural = 'Кинотеатры'



class Schedule(models.Model):
    """Расписания"""
    title = models.CharField('Название фильма', max_length=50)
    date_time = models.DateTimeField('Дата и время')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кинотеатр')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

