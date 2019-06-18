import json
import pandas as pd
from consumption.forms import Search
from datetime import date, datetime # json serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDate, TruncMonth
from .models import User_data, Consumption
from django.core.paginator import Paginator

SUMMARY_HTML = 'summary.html'
HOME_HTML = 'home.html'
DETAIL_HTML = 'details.html'

def front_page(request):
    return render(request, HOME_HTML)

def summary(request):
    
    tables = []
    queries = {
        # average and total consumption of all users
        'user_data_id': list(Consumption.objects.values('user_data_id')
                                .order_by('user_data_id')
                                .annotate(Average_consumption=Avg('consumption'),
                                        Total_consumption=Sum('consumption'))
                                ),
        # average and total consumption for each date
        'Date': list(Consumption.objects.annotate(Date=TruncDate('datetime'))
                        .values('Date').order_by('Date')
                        .annotate(Average_consumption=Avg('consumption'),
                                Total_consumption=Sum('consumption'))
                        ),
        # average and total consumption for each area
        'area': list(User_data.objects.select_related('user_data_id')
                        .values('area').order_by('area')
                        .annotate(
                            Average_consumption=Avg('consumption__consumption'),
                            Total_consumption=Sum('consumption__consumption'))
                        ),
        # average and total consumption for each tariff
        'tariff': list(User_data.objects.select_related('user_data_id')
                        .values('tariff').order_by('tariff')
                        .annotate(
                            Average_consumption=Avg('consumption__consumption'),
                            Total_consumption=Sum('consumption__consumption'))
                        )}

    for header, result in queries.items():
        df = pd.DataFrame(result)[[header, 'Average_consumption','Total_consumption']] 

        if header == 'user_data_id':
            df.loc[len(df) + 1] = [
            'All',
            Consumption.objects.values('consumption')
            .aggregate(Avg('consumption'))['consumption__avg'],
            Consumption.objects.values('consumption')
            .aggregate(Sum('consumption'))['consumption__sum']
            ]
        df['Average_consumption'] = round(df['Average_consumption'], 2)
        df['Total_consumption'] = round(df['Total_consumption'], 2)
        df = df.rename(columns={'user_data_id': 'User ID',
                                'Average_consumption': 'Average Consumption',
                                'Total_consumption': 'Total Consumption',
                                'area': 'Area', 'tariff': 'Tariff'})
        tables.append(df.to_html(index=False, justify='left'))
        del df

    # chart
    all_users = User_data.objects.all()
    user_data = []
    a = User_data.objects.select_related('user_data_id').values('area').order_by('area').annotate(Average_consumption=Avg('consumption__consumption'))
    b = User_data.objects.select_related('user_data_id').values('tariff').order_by('tariff').annotate(Average_consumption=Avg('consumption__consumption')) 
    c = Consumption.objects.annotate(Month=TruncMonth('datetime')).values('Month').order_by('Month').annotate(Average_consumption=Avg('consumption'))

    for user in all_users:
            user_data.append({
            'id': user.id,
            'area': user.area,
            'tariff': user.tariff,
            'total_consumption': Consumption.get_total(user),
            'average_consumption': int(Consumption.get_average(user)),
            })  

    areadata = list(a)
    tariffdata = list(b)
    monthdata = list(c)

    # for date-type of json
    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%m/%Y")
        raise TypeError ("Type %s not serializable" % type(obj))

    context = {
    'data': json.dumps(user_data),
    'areadata': json.dumps(areadata),
    'tariffdata': json.dumps(tariffdata),
    'tables': tables,
    'monthdata': json.dumps(monthdata,default=json_serial),
    }

    print(monthdata)
    return render(request, SUMMARY_HTML, context)

def details(request):
    form = Search(request.GET)

    if form.is_valid():
        id_search = form.cleaned_data['id_search']
        print(id_search)

    else: # set the initial parameter as 3000
        id_search = 3000
    
    tables = []
    for ppp in User_data.objects.select_related('user_data_id').values('id', 'area', 'tariff',
                            'consumption__datetime',
                            'consumption__consumption').filter(id=id_search).order_by('consumption__datetime'):
       
        tables.append(ppp)

    # print(tables)

    all_users = User_data.objects.all()
    user_data = []
    b = User_data.objects.select_related('user_data_id').values('tariff').order_by('tariff').annotate(Average_consumption=Avg('consumption__consumption'))     
    c = Consumption.objects.annotate(Month=TruncMonth('datetime')).values('Month').order_by('Month').annotate(Average_consumption=Avg('consumption')).filter(user_data_id=id_search)

    monthdata = list(c)

    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%m/%Y")
            # return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))

    for user in all_users:
                user_data.append({
                'id': user.id,
                'tariff': user.tariff,
                'total_consumption': Consumption.get_total(user),
                'average_consumption': int(Consumption.get_average(user)),
                })  

    # pagination
    paginator = Paginator(tables, 100) # Show 25 contacts per page
    page = request.GET.get('page')
    # table list turn for pagination 
    tables = paginator.get_page(page)
    
    context = {'tables':tables, 'form': form, 'monthdata': json.dumps(monthdata,default=json_serial)}

    return render(request, DETAIL_HTML, context)