from django.urls import path
from .views import BubbleDataRequestView

urlpatterns = [
    path('data/', BubbleDataRequestView.as_view()),

]
