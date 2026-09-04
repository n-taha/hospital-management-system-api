from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users import views
from departments.views import DepartmentViewSets
from appointments.views import AppointmentViewSets
from payments.views import InvoiceItemViewSets, InvoiceViewSets, ManualPaymentviewSets

router = DefaultRouter()

router.register('users', views.UserViewSets, basename='users')
router.register('doctors', views.DoctorViewSets, basename='doctors')
router.register('patients', views.PatientViewSets, basename='patient')
router.register('departments', DepartmentViewSets, basename='departments')
router.register('appointments', AppointmentViewSets, basename='appointments')
router.register('invoices', InvoiceViewSets, basename='invoices')
router.register('invoice-items', InvoiceItemViewSets, basename='items')
router.register('manual-payment', ManualPaymentviewSets, basename='manual-payments')

urlpatterns = [
    path("", include(router.urls))
]
