from django.contrib.auth.models import User
from django.http import HttpResponse
from numpy import size
from rest_framework import viewsets, status, filters, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import pandas as pd
from .models import *
from .serializers import *
from .filters import *


# for searching in DB
class SearchViewSet(generics.ListCreateAPIView):
    search_fields = ['symbol','date']
    filter_backends = (filters.SearchFilter,)
    queryset = DailyPriceModel.objects.all().order_by('symbol')
    serializer_class = DailyPriceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    http_method_names = ['get']


# add data using csv file
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadCSV(request):
    try:
        price = pd.read_csv(request.data['csv'])
        stockslist = []
        for i in range(len(price['Date'])):
            try: 
                stockslist.append(
                    DailyPriceModel(
                    date=price['Date'][i],
                    symbol=price['Symbol'][i],
                    prevClose=price['Prev Close'][i],
                    open=price['Open'][i],
                    high=price['High'][i],
                    low=price['Low'][i],
                    last=price['Last'][i],
                    close=price['Close'][i],
                    vwap=price['VWAP'][i],
                    volume=price['Volume'][i],
                    # turnover=price['Turnover'][i],
                    )
                )
            except:
                pass
        DailyPriceModel.objects.bulk_create(stockslist)
        return HttpResponse([price], status=status.HTTP_200_OK)
    except:
        return HttpResponse("something went wrong", status=status.HTTP_400_BAD_REQUEST)


# add data using json data
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadJSON(request):
    try:
        price = request.data
        stockslist = []
        for i in range(len(price)):
            try: 
                date_time_obj = datetime.strptime(price[i]['Date'], '%Y-%m-%d')
                stockslist.append(
                    DailyPriceModel(
                    date=date_time_obj.date(),
                    symbol=price[i]['Symbol'],
                    prevClose=float(price[i]['Prev Close']),
                    open=float(price[i]['Open']),
                    high=float(price[i]['High']),
                    low=float(price[i]['Low']),
                    last=float(price[i]['Last']),
                    close=float(price[i]['Close']),
                    vwap=float(price[i]['VWAP']),
                    volume=int(price[i]['Volume']),
                    )
                )
            except:
                pass
        DailyPriceModel.objects.bulk_create(stockslist)
        return Response({"msg":"file upload successfully"}, status=status.HTTP_200_OK)
    except:
        return HttpResponse("something went wrong", status=status.HTTP_400_BAD_REQUEST)


# for creating new user
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])
        token = Token.objects.get(user=user)
        response = {str(token)}
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


# to get filtered data
class FilterViewSet(viewsets.ModelViewSet):
    queryset = DailyPriceModel.objects.all().order_by("symbol")
    serializer_class = DailyPriceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if len(request.GET):
            myFilter = DailyPriceFilter(request.GET,queryset=queryset)
            queryset=myFilter.qs
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# for deleting data
class DeleteViewSet(viewsets.ModelViewSet):
    queryset = DailyPriceModel.objects.all()
    serializer_class = DailyPriceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    http_method_names = ['delete','get']

    @action(detail=False, methods=['DELETE','GET'])
    def deletedata(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        myFilter = DailyPriceFilter(request.GET,queryset=queryset)
        queryset=myFilter.qs.delete()
        
        return Response({str(request.GET).split('{')[1].split('}')[0]})


# Show all data grouped by company
class ShowDataViewSet(viewsets.ModelViewSet):
    queryset = DailyPriceModel.objects.all()
    serializer_class = DailyPriceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        data={}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for i in range(size(serializer.data)):
            try:
                data[serializer.data[i]['symbol']].append(serializer.data[i])
            except:
                data[serializer.data[i]['symbol']]=[]
                data[serializer.data[i]['symbol']].append(serializer.data[i])

        return Response(data)

    @action(detail=False, methods=['GET'])
    def companylist(self, request, pk=None):
        data=set({})
        que = DailyPriceModel.objects.raw("""SELECT DISTINCT id,Symbol FROM api_dailypricemodel GROUP BY Symbol;""")
        for i in range(len(que)):
            data.add(que[i].symbol)
        return Response(data)
