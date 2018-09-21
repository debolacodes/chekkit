from django.shortcuts import render
from django.http import HttpResponse
from ussd.models import UssdData
from product.models import ProductLine,CodeCollection, Batch, ProductCode
from accounts.forms import ManufacturerForm, ProfileForm
from accounts.models import Location


from django.core import serializers
from rest_framework.decorators import api_view
from ussd.processor import USSDProcessor


import json

# Create your views here.

def index(request):
    return HttpResponse('Hello From Post')

def ussddata(request):
    ussdrecords = UssdData.objects.all()
    return HttpResponse(ussdrecords, content_type="application/json")

def locations(request):
    ussdrecords = UssdData.objects.all()
    return HttpResponse(ussdrecords, content_type="application/json")


def totalcodes(request):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    all_data = {};
    total = 0;
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        counter = 0
        for ud in ad:
            total = total + 1

    return HttpResponse(total)



def ussddatapl(request,pl):
    pd = ProductLine.objects.get(id = pl);
    ussdrecords = UssdData.objects.filter(product_line = pd)
    return HttpResponse(ussdrecords, content_type="application/json")


def ussddatarangepl(request,pl,start_date,end_date):
    pd = ProductLine.objects.get(id = pl)
    ussdrecords = UssdData.objects.filter(product_line = pd, created__range=(start_date, end_date))
    return HttpResponse(ussdrecords, content_type="application/json")


def ussddatadaypl(request,pl,date):
    date_list = date.split('-')
    pd = ProductLine.objects.get(id = pl)
    ussdrecords = UssdData.objects.filter(product_line = pd, created__year = date_list[0],
                                        created__month = date_list[1],
                                        created__day = date_list[1])
    return HttpResponse(ussdrecords, content_type="application/json")


def ussddatamonthpl(request,pl,date):
    date_list = date.split('-')
    pd = ProductLine.objects.get(id = pl)
    ussdrecords = UssdData.objects.filter(product_line = pd,created__year = date_list[0],
                                        created__month = date_list[1])
    return HttpResponse(ussdrecords, content_type="application/json")

def ussddatayearpl(request,pl,date):
    date_list = date.split('-')
    pd = ProductLine.objects.get(id = pl)
    ussdrecords = UssdData.objects.filter(product_line = pd,created__year = date_list[0])
    return HttpResponse(ussdrecords, content_type="application/json")

def ussddatarange(request,start_date,end_date):
    ussdrecords = UssdData.objects.filter(created__range=(start_date, end_date))
    return HttpResponse(ussdrecords, content_type="application/json")


def ussddataday(request,date):
    date_list = date.split('-')
    ussdrecords = UssdData.objects.filter(created__year = date_list[0],
                                        created__month = date_list[1],
                                        created__day = date_list[1])
    return HttpResponse(ussdrecords, content_type="application/json")


def ussddatamonth(request,date):
    date_list = date.split('-')
    ussdrecords = UssdData.objects.filter(created__year = date_list[0],
                                        created__month = date_list[1])
    return HttpResponse(ussdrecords, content_type="application/json")



def ussddatayear(request,date):
    date_list = date.split('-')
    ussdrecords = UssdData.objects.filter(created__year = date_list[0])
    return HttpResponse(ussdrecords, content_type="application/json")



























def analytics_complaints(request):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    all_data = {};
    COMPLAINT_CHOICES = {'1':'No complaint',
                        '2':'Product below quality',
                        '3':'Product too expensive'}
    complaints = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            if ussdd[6] in complaints:
                complaints[ussdd[6]] = int(complaints[ussdd[6]]) + 1
            else:
                complaints[ussdd[6]] = 1

    for lc in complaints:
        complain_key = lc.replace(']','');
        complain = COMPLAINT_CHOICES[complain_key].replace(']','')
        lc_str = lc_str + ("{'X':'"+complain+"','Y':"+str(complaints[lc])+"},")

    lc_str = lc_str[:-1].replace("'",'"');
    return HttpResponse('['+lc_str+']', content_type="application/json")


def analytics_locations(request):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    all_data = {};

    locations = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            if ussdd[1] in locations:
                locations[ussdd[1]] = int(locations[ussdd[1]]) + 1
            else:
                locations[ussdd[1]] = 1

    for lc in locations:
        lc_str = lc_str + ("{'X':'"+lc+"','Y':"+str(locations[lc])+"},")

    lc_str = lc_str[:-1].replace("'",'"')

    return HttpResponse('['+lc_str+']', content_type="application/json")



def analytics_codechecked(request):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    all_data = {};
    # pd = ProductLine.objects.get(id = pl)
    cc = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        counter = 0
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            counter = counter + 1;
        cc = cc + "{'X':'"+product_name[0]+"','Y':"+str(counter)+"},"

    cc = cc[:-1].replace("'",'"')
    return HttpResponse('['+cc+']', content_type="application/json")

def analytics(request):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user);
    all_data = {};
    # pd = ProductLine.objects.get(id = pl)

    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        counter = 0
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            print ("{name:'"+ussdd[1]+"',y:"+str(counter)+"},")

        all_data[product_name[0]] = ad_str
    # .replace('\\"', '"').replace('\\', '').replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')
    all_data_str = (json.dumps(all_data)).replace('\\', '').replace(',{', ',{"').replace('"{{', '{{"').replace('},}"', '},}')
    return HttpResponse(all_data_str, content_type="application/json")

















def analytics_complaints_product(request,product_id):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};
    COMPLAINT_CHOICES = {'1':'No complaint',
                        '2':'Product below quality',
                        '3':'Product too expensive'}
    complaints = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            if ussdd[6] in complaints:
                complaints[ussdd[6]] = int(complaints[ussdd[6]]) + 1
            else:
                complaints[ussdd[6]] = 1

    for lc in complaints:
        complain_key = lc.replace(']','');
        complain = COMPLAINT_CHOICES[complain_key].replace(']','')
        lc_str = lc_str + ("{name:'"+complain+"',y:"+str(complaints[lc])+"},")

    return HttpResponse('['+lc_str+']', content_type="application/json")


def analytics_locations_product(request,product_id):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};

    locations = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            if ussdd[1] in locations:
                locations[ussdd[1]] = int(locations[ussdd[1]]) + 1
            else:
                locations[ussdd[1]] = 1

    for lc in locations:
        lc_str = lc_str + ("{name:'"+lc+"',y:"+str(locations[lc])+"},")

    return HttpResponse('['+lc_str+']', content_type="application/json")



def analytics_codechecked_product(request,product_id):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};
    # pd = ProductLine.objects.get(id = pl)
    cc = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        counter = 0
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            counter = counter + 1;
        cc = cc + "{name:'"+product_name[0]+"',y:"+str(counter)+"},"
    return HttpResponse('['+cc+']', content_type="application/json")

def analytics_product(request,product_id):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};
    # pd = ProductLine.objects.get(id = pl)

    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl);
        counter = 0
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            print ("{name:'"+ussdd[1]+"',y:"+str(counter)+"},")

        all_data[product_name[0]] = ad_str
    # .replace('\\"', '"').replace('\\', '').replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')
    all_data_str = (json.dumps(all_data)).replace('\\', '').replace(',{', ',{"').replace('"{{', '{{"').replace('},}"', '},}')
    return HttpResponse(all_data_str, content_type="application/json")












def analytics_complaints_product_range(request,product_id,start_date,end_date):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};
    COMPLAINT_CHOICES = {'1':'No complaint',
                        '2':'Product below quality',
                        '3':'Product too expensive'}
    complaints = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl,created__range=(start_date,end_date));
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            if ussdd[6] in complaints:
                complaints[ussdd[6]] = int(complaints[ussdd[6]]) + 1
            else:
                complaints[ussdd[6]] = 1

    for lc in complaints:
        complain_key = lc.replace(']','');
        complain = COMPLAINT_CHOICES[complain_key].replace(']','')
        lc_str = lc_str + ("{name:'"+complain+"',y:"+str(complaints[lc])+"},")

    return HttpResponse('['+lc_str+']', content_type="application/json")


def analytics_locations_product_range(request,product_id,start_date,end_date):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};

    locations = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl,created__range=(start_date,end_date));
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            if ussdd[1] in locations:
                locations[ussdd[1]] = int(locations[ussdd[1]]) + 1
            else:
                locations[ussdd[1]] = 1

    for lc in locations:
        lc_str = lc_str + ("{name:'"+lc+"',y:"+str(locations[lc])+"},")

    return HttpResponse('['+lc_str+']', content_type="application/json")



def analytics_codechecked_product_range(request,product_id,start_date,end_date):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};
    # pd = ProductLine.objects.get(id = pl)
    cc = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl,created__range=(start_date,end_date));
        counter = 0
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            counter = counter + 1;
        cc = cc + "{name:'"+product_name[0]+"',y:"+str(counter)+"},"
    return HttpResponse('['+cc+']', content_type="application/json")

def analytics_codechecked_perday_product_range(request,product_id,start_date,end_date):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};

    result_array = {}
    lc_str = ""
    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl,created__range=(start_date,end_date));
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            date_created = (str(ussdd[4]))[:10]
            if date_created in result_array:
                result_array[date_created] = int(result_array[date_created]) + 1
            else:
                result_array[date_created] = 1

    for lc in result_array:
        lc_str = lc_str + ("{x:'"+lc+"',y:"+str(result_array[lc])+"},")


    lc_str = lc_str[:-1]
    return HttpResponse('['+lc_str+']', content_type="application/json")


def analytics_product_range(request,product_id,start_date,end_date):
    product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user,id=product_id);
    all_data = {};
    # pd = ProductLine.objects.get(id = pl)

    for pl in product_lines:
        product_name = str(pl).split(" (");
        ad_str = ""
        ad = UssdData.objects.filter(product_line = pl,created__range=(start_date,end_date));
        counter = 0
        for ud in ad:
            ad_str = ad_str + str(ud)
            ussdd = str(ud).split(",")
            print ("{name:'"+ussdd[1]+"',y:"+str(counter)+"},")

        all_data[product_name[0]] = ad_str
    # .replace('\\"', '"').replace('\\', '').replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')
    all_data_str = (json.dumps(all_data)).replace('\\', '').replace(',{', ',{"').replace('"{{', '{{"').replace('},}"', '},}')
    return HttpResponse(all_data_str, content_type="application/json")



@api_view(['GET', 'POST'])
def check_it(request):
    data = request.data
    processor = USSDProcessor(data=data)
    return processor.process_request()
