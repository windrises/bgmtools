# coding=utf-8
import sys
import os
import django
import datetime
import calendar

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
if django.VERSION >= (1, 7):
    django.setup()
from myapp.models import Subject
from myapp.models import User
from myapp.models import Comment
from myapp.models import AverageScore
from myapp.models import AllAverageScore

error = open('calculate_error.txt', 'a')
subjects = Subject.objects.filter(sub_cat='real')
average_score_dic = {}
dt1 = datetime.datetime(1900, 1, 1)
now_dt = datetime.datetime(2018, 1, 15)
now_timeid = (now_dt - dt1).days
repeat = {}
log_cnt = 0

def change_timeid(timeid):
    timeid = (timeid + 20) / 21 * 21
    return timeid

for subject in subjects:
    log_cnt += 1
    if log_cnt % 1000 == 0:
        print log_cnt
    comments = subject.comment_set.all().order_by('timeid')
    sum = 0
    num = len(comments)
    if num == 0:
        continue
    last_timeid = change_timeid(comments[0].timeid)
    cnt = 0
    tot = 0
    comments_len = len(comments)
    for i in range(comments_len + 1):
        comment = ''
        cur_timeid = -1
        if i != comments_len:
            comment = comments[i]
            cur_timeid = change_timeid(comment.timeid)
        else:
            cur_timeid = now_timeid + 1
        while last_timeid < cur_timeid:
            dt2 = dt1 + datetime.timedelta(days=last_timeid)
            timestr = str(dt2.year) + '-' + str(dt2.month) + '-' + str(dt2.day)
            score = 0.0
            if cnt != 0:
                score = sum * 1.0 / cnt
            if last_timeid not in average_score_dic:
                average_score_dic[last_timeid] = []
            average_score_dic[last_timeid].append([subject, timestr, score, tot, cnt])
            last_timeid += 21
        last_timeid = cur_timeid
        if i != comments_len:
            sum += comment.star
            tot += 1
            if comment.star != 0:
                cnt += 1

print '--------------'
log_cnt = 0
m_array = [51, 21, 21, 21, 21]
sub_cat_dic = {'anime': 0, 'book': 1, 'music': 2, 'game': 3, 'real': 4}
sub_cat_array = ['anime', 'book', 'music', 'game', 'real']
sum = [0.0] * 5
cnt = [0] * 5
average_score_array = []
all_average_score_array = []
timeids = sorted(average_score_dic.keys())
for timeid in timeids:
    average_scores = average_score_dic[timeid]
    for average_score in average_scores:
        sub_cat_index = sub_cat_dic[average_score[0].sub_cat]
        sum[sub_cat_index] += average_score[2] * average_score[4]
        cnt[sub_cat_index] += average_score[4]
    C_array = [0.0] * 5
    for i in range(0, 5):
        if cnt[i] != 0:
            C_array[i] = sum[i] * 1.0 / cnt[i]
            error.write(str(timeid) + '    ' + sub_cat_array[i] + '\n')
            all_average_score_array.append(AllAverageScore(timeid=timeid, sub_cat=sub_cat_array[i], score=C_array[i]))
    average_score_sort_array = {0: [], 1: [], 2: [], 3: [], 4: []}
    for i, average_score in enumerate(average_scores):
        sub_cat_index = sub_cat_dic[average_score[0].sub_cat]
        R = average_score[2]
        v = average_score[4]
        m = m_array[sub_cat_index]
        C = C_array[sub_cat_index]
        if v < m:
            average_score_array.append(AverageScore(timeid=timeid, timestr=average_score[1], subject=average_score[0],
                                                    score=average_score[2], people=average_score[3],
                                                    votes=average_score[4]))
            if len(average_score_array) >= 10000:
                log_cnt += len(average_score_array)
                print log_cnt
                AverageScore.objects.bulk_create(average_score_array)
                average_score_array = []
            continue
        imdb_score = (R * v + m * C) / (v + m)
        average_score_sort_array[sub_cat_index].append([imdb_score, i])
    for i in range(0, 5):
        average_score_sort_array[i] = sorted(average_score_sort_array[i], key=lambda x: x[0], reverse=True)
        tlen = len(average_score_sort_array[i])
        for j in range(tlen):
            index = average_score_sort_array[i][j][1]
            average_score = average_scores[index]
            average_score_array.append(AverageScore(timeid=timeid, timestr=average_score[1], subject=average_score[0],
                                                    score=average_score[2], imdb_score=average_score_sort_array[i][j][0],
                                                    rank=j + 1, people=average_score[3], votes=average_score[4]))
            if len(average_score_array) >= 10000:
                log_cnt += len(average_score_array)
                print log_cnt
                AverageScore.objects.bulk_create(average_score_array)
                average_score_array = []
    sum = [0.0] * 5
    cnt = [0] * 5

AverageScore.objects.bulk_create(average_score_array)
AllAverageScore.objects.bulk_create(all_average_score_array)
print('Done!')
