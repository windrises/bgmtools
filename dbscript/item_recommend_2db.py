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
f = open('item_recommend_result.txt')
error = open('item_recommend_error.txt', 'a')
duplicate = {}
def main():
    from myapp.models import Subject
    from myapp.models import RcmdItem
    i = 0
    all = []
    for line in f:
        i += 1
        line = line.strip('\n')
        line = line.split(' ')
        sid = int(line[0])
        subject = Subject.objects.get(id=sid)
        for j in range(1, len(line)):
            x = line[j]
            x = x.split(',')
            rcmd = Subject.objects.get(id=int(x[0]))
            weight = float(x[1])
            all.append(RcmdItem(
                subject=subject,
                rcmd=rcmd,
                weight=weight
            ))
        if i % 100 == 0:
            print i
            RcmdItem.objects.bulk_create(all)
            all = []

    RcmdItem.objects.bulk_create(all)
    f.close()
    error.close()

if __name__ == "__main__":
    main()
    print('Done!')
