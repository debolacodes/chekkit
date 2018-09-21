from django.template import loader
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers

from accounts.forms import ManufacturerForm, ProfileForm
from accounts.models import Location

from product.models import ProductLine, CodeCollection, Batch, ProductCode

# from ussdapp.models import UssdRecord
import json

import jsonpickle

# Create your views here.
def overview(request):
    if request.user.is_authenticated:
        if not request.user.profile.activated:
            if request.method == 'POST':
                create_manufacturer_form = ManufacturerForm(request.POST)
                profile_form = ProfileForm(request.POST)
                if create_manufacturer_form.is_valid() and profile_form.is_valid():
                    manufacturer = create_manufacturer_form.save()
                    position = profile_form.cleaned_data['position']
                    profile = request.user.profile
                    profile.manufacturer = manufacturer
                    profile.activated = True
                    profile.position = position
                    Location.objects.create(name=manufacturer.address, manufacturer=manufacturer)
                    profile.save()
                return redirect(reverse('frontend:overview'))
            else:
                create_manufacturer_form = ManufacturerForm()
                profile_form = ProfileForm(initial={})
            return render(request, 'frontend/overview.html',
                          {'create_manufacturer_form': create_manufacturer_form, 'profile_form': profile_form})
        else:
            product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user)
            context = {
                'product_lines': product_lines,
                'overview': True
            }
            return render(request, 'frontend/overview.html', context)
    else:
        return render(request, 'frontend/landing.html', {})


def activity(request):

    context = {
        'activity': True
    }
    return render(request, 'frontend/activity.html', context)



def analytics(request):

    context = {

        'analytics': True
    }
    return render(request, 'frontend/analytics.html', context)

# def ussdrecords(request):
#
#     ussdrecords = UssdRecord.objects.all()
#     return render(request, 'frontend/ussdrecords.html', {'ussdrecords': ussdrecords})


def collections(request):
    collection_object = CodeCollection.objects.filter(manufacturer=request.user.profile.manufacturer)
    context = {
        'collection_object': collection_object,
        'collections': True
    }
    return render(request, 'frontend/collections.html', context)


def charts(request):
    # collection_object = CodeCollection.objects.filter(manufacturer=request.user.profile.manufacturer)
    context = {
        'analytics': True
    }
    return render(request, 'frontend/charts.html', context)



def graphs(request):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    context = {
        'product_lines':product_lines,
        'analytics': True
    }
    return render(request, 'frontend/SimpleChart.html', context)





# productcodes

def productcode(request):

    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    # product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    pd = {};
    productcode_output = serializers.serialize('json',product_lines)

    return HttpResponse(productcode_output, content_type="application/json")

def collectionsJSON(request):
    collection_object = CodeCollection.objects.filter(manufacturer=request.user.profile.manufacturer)
    collection_output = serializers.serialize('json',collection_object)
    if(collection_object):
        return HttpResponse(collection_output, content_type="application/json")
    else:
        return HttpResponse("No Data", content_type="application/json")

def totalcodes(request):
    collection_object = CodeCollection.objects.filter(manufacturer=request.user.profile.manufacturer)
    collection_output = serializers.serialize('json',collection_object)
    if(collection_object):
        total = 0;
        for cco in collection_object:
            total = total + int(cco.quantity)
        return HttpResponse(total)
    else:
        return HttpResponse("0")



def all_batches(request):
    product_batches = Batch.objects.all()
    product_output = serializers.serialize('json',product_batches)
    return HttpResponse(product_output, content_type="application/json")





    # ussdrecords_output = serializers.serialize('json',ussdrecords)
    # return HttpResponse(ussdrecords_output, content_type="application/json")

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial

    return obj.__dict__




def productsLines(request):
    if request.user.is_authenticated:
        product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user)
        product_lines_codes = serializers.serialize('json',product_lines)
        pd = {}
        codesgenerated = {}
        for product_line in product_lines:
            pb = CodeCollection.objects.filter(product_line_id = product_line.id)
            # pj = serializers.serialize('json',pb)
            pj = serializers.serialize('json',pb)
            pd[product_line.id] = pj
            pmi = 0
            pdk = "`"+str(product_line.id)+"`"
            if pdk in codesgenerated:
                finalJsonStr = json.loads(jsonpickle.encode(pd[product_line.id]).replace('\\"', "'"));
                codesgenerated[pdk] = codesgenerated[pdk] + finalJsonStr;
                pmi = 1

            else:
                codesgenerated[pdk] = {};
                finalJsonStr = json.loads(jsonpickle.encode(pd[product_line.id]).replace('\\"', "'"));
                codesgenerated[pdk] = finalJsonStr;

        context = {
            'product_lines_with_batches': pd
        }
        contextjson = json.dumps(codesgenerated).replace('\"', '').replace("\\\\","").replace("'",'"').replace("`",'"');
        json_objects = json.loads(contextjson)
        return HttpResponse(contextjson, content_type="application/json")
    else:
        return HttpResponse("Unauthenticated", content_type="application/json")




def getjson(request):

    context = {
        'activity': True
    }
    return render(request, 'frontend/getjson.html', context)



def productname(request,pk):
    product_line = ProductLine.objects.filter(id = pk)
    return render(request, 'frontend/productname.html',{'product_line_object': product_line})


# def ussdrecords(request):
#     ussdrecord = UssdRecord.objects.all()
#     # return render(request, 'frontend/ussdrecords.html',{'ussdrecord': ussdrecord})
#     ussdrecords_json = serializers.serialize('json',ussdrecord)
#     return HttpResponse(ussdrecords_json, content_type="application/json")
#
#     product_output = serializers.serialize('json',product_batches)
#     context = {
#         'product_batches': product_batches,
#         'activity': True
#     }
#     return HttpResponse(product_output, content_type="application/json")
