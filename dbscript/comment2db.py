#coding=utf-8
#!/usr/bin/env python
import os
import json
import datetime
import calendar
import django
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
if django.VERSION >= (1, 7):
    django.setup()
f = open('comment.json')
error = open('comment_error.txt', 'a')
dt1 = datetime.datetime(1900, 1, 1)
duplicate = {}
def main():
    from myapp.models import Subject
    from myapp.models import User
    from myapp.models import Comment
    i = 0
    all = []
    for line in f:
        i += 1
        data = ''
        try:
            data = json.loads(line)
        except:
            error.write(line + '\n')
            line = line.replace('\\', '\\\\').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
            data = json.loads(line)
            error.write('----' + line + '\n')
            error.flush()
        user_name = data['user_name']
        sid = data['sid']
        user = ''
        subject = ''
        try:
            user = User.objects.get(user_name=user_name)
            subject = Subject.objects.get(id=sid)
        except:
            error.write('not exists ------ ' + line + '\n')
            error.flush()
            continue
        key = user_name + '|' + str(sid)
        if key in duplicate:
            error.write('duplicate ------' + line + '\n')
            error.flush()
            continue
        else:
            duplicate[key] = 1
        time = data['time']
        time = time.split(' ')[0].split('-')
        dt2 = datetime.datetime(int(time[0]), int(time[1]), int(time[2]))
        timeid = (dt2 - dt1).days
        timeid = (timeid + 6) / 7 * 7
        all.append(Comment(
            user=user,
            subject=subject,
            star=data['star'],
            time=data['time'],
            timeid=timeid,
            content=data['comment']
        ))
        if i % 10000 == 0:
            print i
            Comment.objects.bulk_create(all)
            all = []

    Comment.objects.bulk_create(all)
    f.close()
    error.close()

if __name__ == "__main__":
    main()
    print('Done!')
