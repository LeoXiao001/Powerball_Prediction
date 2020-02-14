from django.shortcuts import render
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import dateparse
from django.db import IntegrityError
import datetime

from sodapy import Socrata

from .models import History, WhiteBall, RedBall, Picture


class HistoryListView(ListView):
    model = History
    context_object_name = 'histories'
    template_name = 'powerball/history.html'
    paginate_by = 10

    def get_queryset(self):
        self.update_history()
        return History.objects.all()

    def update_history(self):
        # get the latest record draw date
        latest = History.objects.order_by('-draw_date')
        client = Socrata(settings.SODAPY_SOCRATA_DOMAIN, settings.SODAPY_APP_TOKEN)
        if not latest:  # no record in the database;
            # get history starts from 2015-10-04, when powerball numbers changed
            results = client.get(settings.SODAPY_SOCRATA_DATASET_ID,
                                where="draw_date > '2015-10-04'")
        else:  # only need to add latest ones
            latest_date = latest[0].draw_date.strftime('%Y-%m-%d')
            condition = "draw_date > \'{}\'".format(latest_date)
            results = client.get(settings.SODAPY_SOCRATA_DATASET_ID,
                                where=condition)

        for item in results:
            draw_date = item['draw_date']
            numbers = item['winning_numbers']
            draw_date_str = dateparse.parse_datetime(draw_date).date().strftime('%Y-%m-%d')
            white_ball = numbers[:-3]
            red_ball = numbers[-2:]
            try:
                his = History(draw_date=draw_date_str, white_ball=white_ball, red_ball=red_ball)
                his.save()
            except IntegrityError:
                pass


def statistic(request):
    oldest_date = History.objects.order_by('draw_date')[0].draw_date.strftime('%Y-%m-%d')
    white_ball_query = WhiteBall.objects.order_by('number')
    red_ball_query = RedBall.objects.order_by('number')
    white_ball_freq, red_ball_freq = [0] * 69, [0] * 26
    frequency_count(white_ball_query, white_ball_freq)
    frequency_count(red_ball_query, red_ball_freq)
    white_ball_num = [f'{i:02}' for i in range(1, 70)]
    red_ball_num = [f'{i:02}' for i in range(1, 27)]

    return render(request, 'powerball/statistic.html',
                        {'white_ball_num': white_ball_num,
                        'white_ball_freq': white_ball_freq,
                        'red_ball_num': red_ball_num,
                        'red_ball_freq': red_ball_freq,
                        'oldest_date': oldest_date})

def frequency_count(query_set, frequencies):
    for item in query_set:
        index = int(item.number) - 1
        frequencies[index] = item.frequency


def prediction(request):
    white_ball_query = WhiteBall.objects.order_by('frequency')
    red_ball_query = RedBall.objects.order_by('frequency')

    white_nums = get_nums(white_ball_query, 5)
    red_nums = get_nums(red_ball_query, 1)
    white_nums_combinations = combinations(white_nums, 5)
    red_nums_combinations = combinations(red_nums, 1)
    predicts = get_predicts(white_nums_combinations, red_nums_combinations)

    latest_date = History.objects.order_by('-draw_date')[0].draw_date
    valid_date = check_valid_date(latest_date)
    # print(type(latest_date))

    return render(request, 'powerball/prediction.html', {'predictions': predicts,
                                                        'valid_date': valid_date})

def check_valid_date(latest_date):
    latest_weekday = latest_date.weekday()
    if latest_weekday == 2:
        delta_day = datetime.timedelta(days=3)
    elif latest_weekday == 5:
        delta_day = datetime.timedelta(days=4)
    valid_date = latest_date + delta_day
    valid_time = datetime.time(22, 59, 0)
    valid_day = datetime.datetime.combine(valid_date, valid_time)

    return valid_day.strftime('%Y-%m-%d %H:%M:%S')

def get_predicts(white_nums, red_nums):
    result = []
    for white in white_nums:
        for red in red_nums:
            result.append((' '.join(white), red[0]))

    return result

def get_nums(query, target):
    result = []
    counts = 0
    visited = set()
    temp = []
    for item in query:
        freq = item.frequency
        if freq not in visited:
            if temp:
                result.append(temp)
                temp = []
            if counts >= target:
                break
            visited.add(freq)
        temp.append(item.number)
        counts += 1

    return result

def combinations(nums, target):
    result = []
    single_nums = []
    for item in nums:
        if len(item) <= target:
            single_nums.extend(item)
            target -= len(item)
            if not target:
                result.append(single_nums)
                break
        else:
            temp = pick_num(item, target)
            for row in temp:
                result.append(single_nums + row)
            break
    for item in result:
        item.sort()
    return result

def pick_num(nums, target):
    result = []
    path = []
    index = 0
    dfs(nums, index, path, result, target)
    return result

def dfs(nums, index, path, result, target):
    if len(path) == target:
        result.append(list(path))
        return
    for i in range(index, len(nums)):
        path.append(nums[i])
        dfs(nums, i + 1, path, result, target)
        path.pop()


def index(request):
    return render(request, 'powerball/index.html')


class PictureListView(ListView):
    model = Picture
    context_object_name = 'pictures'
    template_name = 'powerball/pictures.html'

    def get_queryset(self):
        return Picture.objects.all()


def powerball_model(request):
    return render(request, 'powerball/model.html')