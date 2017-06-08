from django.conf.urls import url, include
from allauth.account import views
from manager import views as manager_views

urlpatterns = [
    url(r"^$", manager_views.MainView.as_view(), name="main_page"),

]
