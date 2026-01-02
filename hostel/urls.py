from django.urls import path

from . import views

urlpatterns = [
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lodge_complaint/', views.lodge_complaint, name='lodge_complaint'),
    path('download_voucher/', views.download_voucher, name='download_voucher'),
    path('apply_room/', views.submit_application, name='apply_room'),

    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('complaints/', views.fetch_complaints, name='fetch_complaints'),
    path('applications/', views.fetch_applications, name='fetch_applications'),
]