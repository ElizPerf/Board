from django.urls import path

from boardapp import views
from .views import NoticesList, NoticeDetail, NoticesListProfile, response_create, response_status

urlpatterns = [
   path('', NoticesList.as_view(), name='notices_list'),
   path('notices/', NoticesList.as_view(), name='notices'),
   path('notices_profile/', NoticesListProfile.as_view(), name='notices_profile'),
   path('notices/<int:notice_id>/', NoticeDetail.as_view(), name='notice'),
   path('notices/create/', views.notice_create, name='notice_create'),
   path('notices/edit/<int:notice_id>/', views.notice_edit, name='notice_edit'),
   path('notices/delete/<int:notice_id>/', views.notice_delete, name='notice_delete'),
   path('notices/response/<int:notice_id>/', response_create, name='response_create'),
   path('responses/<int:response_id>/response_status/<str:action>/', response_status, name='response_status'),
]