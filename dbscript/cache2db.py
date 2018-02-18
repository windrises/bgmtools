#coding=utf-8
#!/usr/bin/env python
import os
import django
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
if django.VERSION >= (1, 7):
    django.setup()

def main():
    from myapp.models import Tag
    from myapp.models import Subject
    from myapp.models import Cache
    all = []
    for sub_cat in ['anime', 'book', 'music', 'game', 'real']:
        tags = Tag.objects.filter(sub_cat=sub_cat, cnt__gte=500)
        for tag in tags:
            tag = tag.name
            result = Subject.objects.filter(sub_cat=sub_cat, tag__name=tag)
            alltag = []
            for x in result:
                for y in x.tag.all():
                    alltag.append(y.name)
            cnt = {}
            for x in alltag:
                if cnt.has_key(x):
                    cnt[x] += 1
                else:
                    cnt[x] = 1
            hottag = cnt.items()
            hottag.sort(key=lambda d: d[1], reverse=True)
            hottag = hottag[: 100]
            key = 'multitag ' + sub_cat + ' ' + tag
            value = ''
            for x in hottag:
                value += x[0] + ' ' + str(x[1]) + ','
            value = value[: -1]
            all.append(Cache(key=key, value=value))
        tags = Tag.objects.filter(sub_cat=sub_cat)
        tags = tags.order_by('-cnt')
        key = 'multitag ' + sub_cat + '  '
        value = ''
        for i in range(0, 100):
            value += tags[i].name + ' ' + str(tags[i].cnt) + ','
        value = value[: -1]
        all.append(Cache(key=key, value=value))
    Cache.objects.bulk_create(all)

if __name__ == "__main__":
    main()
    print('Done!')
