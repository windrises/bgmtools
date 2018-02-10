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
f = open('user.json')
error = open('user_error.txt', 'a')
def main():
    from myapp.models import User
    i = 0
    all = []
    for line in f:
        i += 1
        data = ''
        try:
            data = json.loads(line)
        except:
            print i
            error.write(str(i) + '\n')
            error.flush()
            break
        all.append(User(
            user_name=data['user_name'],
            id=data['id'],
            nick_name=data['nick_name'],
            signup_time=data['signup_time'],
            ban=data['ban'],
            avater=data['avater']
        ))
        if i % 5000 == 0:
            print i
            User.objects.bulk_create(all)
            all = []

    User.objects.bulk_create(all)
    f.close()
    error.close()

if __name__ == "__main__":
    main()
    print('Done!')
