import calendar
import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import AddCalendarItemForm
from .models import CalendarItem
from main.models import UserProfile


class Calendar(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/calendar.html', {'items': CalendarItem.objects.all()})


class CalendarApi(View):
    def get(self, request, *args, **kwargs):
        print(kwargs['month'], kwargs['year'])
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        prev_month = month - 1
        prev_year = year
        if prev_month == 0:
            prev_month = 12
            prev_year = year - 1
        next_month = month + 1
        if next_month > 12:
            next_month = 1
        items = CalendarItem.objects.filter(
            Q(start__year=year) & Q(start__month=month) | (
                        Q(start__year=prev_year) & Q(start__month=prev_month) & Q(end__month=month))
        )
        base = calendar.monthcalendar(year, month)
        print(base)
        new_base = []
        for i in base:
            for j in i:
                new_base.append(j)
        future_json = []
        for day in new_base:
            future_json.append(dict(
                {'active': day != 0 and day >= datetime.datetime.now().day and month == datetime.datetime.now().month,
                 'day': day, 'dow': calendar.weekday(year, month, day) if day != 0 else 0,
                 'items': list()}))
        for item in items:
            print("ITEM ", item)
            print("START DAY ", item.start.day)
            if item.start.month == month and item.end.month == month:
                for day in range(item.start.day, item.end.day + 1):
                    future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append({'title': item.title, 'id': item.id, 'icon': item.icon})
            elif item.end.month == month:
                for day in range(1, item.end.day + 1):
                    future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append({'title': item.title, 'id': item.id, 'icon': item.icon})
            elif item.end.month == next_month:
                for day in range(item.start.day, calendar.monthrange(year, month)[1] + 1):
                    future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append({'title': item.title, 'id': item.id, 'icon': item.icon})
            print("END DAY ", item.end.day)
        print(json.dumps(future_json, indent=4, sort_keys=True))
        return JsonResponse(future_json, safe=False)


class AddCalendarItem(View):
    def get(self, request):
        form = AddCalendarItemForm()
        return render(request, 'main/add_calendar_item.html', {'form': form})

    def post(self, request):
        form = AddCalendarItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.creator = UserProfile.objects.get(user=request.user)
            item.group = item.creator.family
            item.save()
            return redirect('calendar')
        else:
            return render(request, 'main/add_calendar_item.html', {'form': form})


class CalendarDetailApi(View):
    def get(self, request, *args, **kwargs):
        item = CalendarItem.objects.get(id=kwargs['id'])
        data = dict()
        data['id'] = item.id
        data['title'] = item.title
        data['group'] = item.group.id
        data['creator'] = item.creator.id
        data['start'] = item.start
        data['end'] = item.end
        data['description'] = item.description
        data['notification'] = item.notification
        data['icon'] = item.icon
        return JsonResponse(data, safe=False)


class DeleteCalendarItem(View):
    def get(self, request, *args, **kwargs):
        CalendarItem.objects.get(id=kwargs['id']).delete()
        return redirect('calendar')
