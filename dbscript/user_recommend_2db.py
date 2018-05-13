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
f = open('user_recommend_result.txt')
error = open('user_recommend_error.txt', 'a')
duplicate = {}
def main():
    from myapp.models import User
    from myapp.models import RcmdUser
    i = 0
    all = []
    user_dic = {}
    users = User.objects.all()
    for x in users:
        user_dic[x.id] = x
    for line in f:
        i += 1
        # print i
        line = line.strip('\n')
        line = line.split(' ')
        uid = int(line[0])
        # user = User.objects.get(id=uid)
        user = user_dic[uid]
        for j in range(1, len(line)):
            x = line[j]
            x = x.split(',')
            # rcmd = User.objects.get(id=int(x[0]))
            rcmd = user_dic[int(x[0])]
            similarity = float(x[1])
            all.append(RcmdUser(
                user=user,
                rcmd=rcmd,
                similarity=similarity
            ))
        if i % 100 == 0:
            print i
            RcmdUser.objects.bulk_create(all)
            all = []

    RcmdUser.objects.bulk_create(all)
    f.close()
    error.close()

if __name__ == "__main__":
    main()
    print('Done!')
