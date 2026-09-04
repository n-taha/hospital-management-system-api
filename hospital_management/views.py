from rest_framework.decorators import api_view
from django.shortcuts import redirect

@api_view()
def my_view(request):
  return redirect('/api/v1/')