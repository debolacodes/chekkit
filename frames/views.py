from django.shortcuts import render

# Create your views here.
from django.views.decorators.clickjacking import xframe_options_exempt



@xframe_options_exempt
def analytics(request, start_date, end_date):
    return render(request, 'analytics/codes_over_products.html', {'start_date': start_date, 'end_date': end_date})

@xframe_options_exempt
def locations(request, start_date, end_date):
    return render(request, 'analytics/codes_over_locations.html', {'start_date': start_date, 'end_date': end_date})

@xframe_options_exempt
def complaints(request, start_date, end_date):
    return render(request, 'analytics/codes_over_complaints.html', {'start_date': start_date, 'end_date': end_date})
