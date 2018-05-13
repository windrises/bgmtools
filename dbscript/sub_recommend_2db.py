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
f = open('sub_recommend_result.txt')
error = open('sub_recommend_error.txt', 'a')
duplicate = {}
def main():
    from myapp.models import Subject
    from myapp.models import RcmdSub
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
            similarity = float(x[1])
            all.append(RcmdSub(
                subject=subject,
                rcmd=rcmd,
                similarity=similarity
            ))
        if i % 100 == 0:
            print i
            RcmdSub.objects.bulk_create(all)
            all = []

    RcmdSub.objects.bulk_create(all)
    f.close()
    error.close()

if __name__ == "__main__":
    main()
    print('Done!')
