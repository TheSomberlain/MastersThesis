from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('upload/', views.upload_images, name='upload'),
    path('history/', views.view_history, name='history'),
    path('signup/', views.register, name="signup"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('result/', views.result_view, name='result'),
    path('result/<int:image_id>/', views.result_view, name='result'),
    path('api/upload/', views.upload_files_api, name='upload_api'),
    path('api/analyze/', views.start_analysis_api, name='analyze_api'),
]