# lab_section_management/urls.py
from django.urls import path
from .views import LabSectionListView, LabSectionCreateView, LabSectionDetailView, LabSectionUpdateView, LabSectionDeleteView

urlpatterns = [
    path('', LabSectionListView.as_view(), name='lab_section_list'),
    path('create/', LabSectionCreateView.as_view(), name='lab_section_create'),
    path('<int:pk>/', LabSectionDetailView.as_view(), name='lab_section_detail'),
    path('update/<int:pk>/', LabSectionUpdateView.as_view(), name='lab_section_update'),
    path('delete/<int:pk>/', LabSectionDeleteView.as_view(), name='lab_section_delete'),
]
