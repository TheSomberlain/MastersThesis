from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import apis

urlpatterns = [
    path('', views.home_page, name='home'),
    path('upload/', views.upload_images, name='upload'),
    path('signup/', views.register, name="signup"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('result/', views.result_view, name='result'),
    path('result/<int:image_id>/', views.result_view, name='result'),
    path('history/', views.history_view, name='history_view'),
    path('api/upload/', apis.upload_files_api, name='upload_api'),
    path('api/analyze/', apis.start_analysis_api, name='analyze_api'),
    path('api/exportexcel/', apis.export_rois_excel, name = 'export_excel'),
    path('api/exportcsv/', apis.export_rois_csv, name = 'export_csv'),
    path('api/createreport/', apis.create_report, name = "create_csv"),
    path('api/reportimages/<int:report_id>/', apis.report_images_api, name='report_images_api'),
]