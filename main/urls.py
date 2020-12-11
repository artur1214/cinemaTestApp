from django.urls import path
from .views import CinemaAddView, AddCinemaApiView, \
    CinemaView, ScheduleAddView, AddScheduleApiView, \
    MainView, ScheduleView, ScheduleDeleteView, CinemaUpdateView

urlpatterns = [
    path('add/cinema/', CinemaAddView.as_view(), name='cinema_add'),
    path('add/schedule/', ScheduleAddView.as_view(), name='schedule_add'),
    path('view/cinema/', CinemaView.as_view()),
    path('api/cinema/add/', AddCinemaApiView.as_view()),
    path('api/schedule/add/', AddScheduleApiView.as_view()),
    path('', MainView.as_view()),
    path('view/schedule/', ScheduleView.as_view()),
    path('api/remove/', ScheduleDeleteView.as_view()),
    path('api/cinema/update/', CinemaUpdateView.as_view()),
]
