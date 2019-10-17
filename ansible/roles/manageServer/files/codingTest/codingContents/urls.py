from django.urls import path

from . import views

urlpatterns= [
	path('',views.index,name='index'),
	path('api/sns/',views.sns,name='sns'),
	path('api/sns_r/',views.sns_r,name='sns_r'),
]

