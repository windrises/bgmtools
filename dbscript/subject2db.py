#coding=utf-8
#!/usr/bin/env python
import os
import json
import datetime
import calendar
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
if django.VERSION >= (1, 7):
    django.setup()

def getdate(date, data, error):
    if date.find('/') != -1:
        date = date.replace('/', '-')
    else:
        date = date.replace('年', '-')
        date = date.replace('月', '-')
        date = date.replace('日', '-')
    date = date.split('-')
    year = 1900
    month = 1
    day = 1
    dateid = 0
    try:
        if len(date) == 1:
            year = 1900
            month = 1
            day = 1
            date = ''
        elif len(date) == 2:
            year = int(date[0])
            month = 12
            day = 31
            date = date[0]
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = calendar.monthrange(year, month)[1]
            date = date[0] + '-' + str(month)
        else:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            date = date[0] + '-' + str(month) + '-' + str(day)
        if len(date) > 10:
            date = ''
            dateid = 0
            error.write('------------' + str(str(data).decode('unicode_escape')) + '\n')
            error.flush()
        else:
            dt1 = datetime.datetime(1900, 1, 1)
            dt2 = datetime.datetime(year, month, day)
            dateid = (dt2 - dt1).days
    except:
        date = ''
        dateid = 0
        error.write(str(str(data).decode('unicode_escape')) + '\n')
        error.flush()
    return [date, dateid]

def main():
    from myapp.models import Tag
    from myapp.models import Subject
    f = open('subject.json')
    i = 1
    error = open('subject_error.txt', 'a')
    for line in f:
        if i % 100 == 0:
            print i
        i += 1
        data = ''
        try:
            data = json.loads(line)
        except:
            line = line.replace('\\', '').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
            data = json.loads(line)
            error.write('--------' + line + '\n')
            error.flush()
        tag = data['tag']
        datestr = data['date']
        date = data['date']
        [date, dateid] = getdate(date, data, error)
        votes = data['votes']
        if votes == '':
            votes = 0
        else:
            votes = int(votes)
        rank = data['rank']
        if rank == '':
            rank = 123456789
        else:
            rank = int(rank)
        name = data['namejp']
        if name == '':
            name = data['namechs']
        subject = ''
        sub_cat = data['sub_cat']
        if sub_cat == 'anime':
            if len(Subject.objects.filter(id=data['id'])) != 0:
                continue
            eps = data['eps']
            author = data['author']
            director = data['director']
            personset = data['personset']
            tip = ''
            if eps != '':
                tip += eps + '话'
            if datestr != '':
                if tip != '':
                    tip += ' / '
                tip += datestr
            if author != '':
                if tip != '':
                    tip += ' / '
                tip += author
            if director != '':
                if tip != '':
                    tip += ' / '
                tip += director
            if personset != '':
                if tip != '':
                    tip += ' / '
                tip += personset
            tip = tip[: min(500, len(tip))]

            subject = Subject.objects.create(
                        id=data['id'],
                        sub_cat=sub_cat,
                        img=data['img'],
                        namechs=data['namechs'],
                        namejp=data['namejp'],
                        name=name,
                        cat=data['cat'],
                        dateid=dateid,
                        date=date,
                        star=data['star'],
                        votes=votes,
                        rank=rank,
                        tip=tip
                    )

        elif sub_cat == 'book':
            if len(Subject.objects.filter(id=data['id'])) != 0:
                continue
            eps = data['eps']
            painter = data['painter']
            author = data['author']
            pub = data['pub']
            pages = data['pages']
            tip = ''
            if eps != '':
                tip += eps + '话'
            if datestr != '':
                if tip != '':
                    tip += ' / '
                tip += datestr
            if painter != '':
                if tip != '':
                    tip += ' / '
                tip += painter
            if author != '':
                if tip != '':
                    tip += ' / '
                tip += author
            if pub != '':
                if tip != '':
                    tip += ' / '
                tip += pub
            if pages != '':
                if tip != '':
                    tip += ' / '
                tip += pages
            tip = tip[: min(500, len(tip))]

            subject = Subject.objects.create(
                id=data['id'],
                sub_cat=sub_cat,
                img=data['img'],
                namechs=data['namechs'],
                namejp=data['namejp'],
                name=name,
                cat=data['cat'],
                dateid=dateid,
                date=date,
                star=data['star'],
                votes=votes,
                rank=rank,
                tip=tip
            )

        elif sub_cat == 'music':
            if len(Subject.objects.filter(id=data['id'])) != 0:
                continue
            artist = data['artist']
            tip = ''
            if datestr != '':
                tip += datestr
            if artist != '':
                if tip != '':
                    tip += ' / '
                tip += artist
            tip = tip[: min(500, len(tip))]

            subject = Subject.objects.create(
                id=data['id'],
                sub_cat=sub_cat,
                img=data['img'],
                namechs=data['namechs'],
                namejp=data['namejp'],
                name=name,
                cat=data['cat'],
                dateid=dateid,
                date=date,
                star=data['star'],
                votes=votes,
                rank=rank,
                tip=tip
            )

        elif sub_cat == 'game':
            if len(Subject.objects.filter(id=data['id'])) != 0:
                continue
            platform = data['platform']
            type = data['type']
            develop = data['develop']
            tip = ''
            if datestr != '':
                tip += datestr
            if platform != '':
                if tip != '':
                    tip += ' / '
                tip += platform
            if type != '':
                if tip != '':
                    tip += ' / '
                tip += type
            if develop != '':
                if tip != '':
                    tip += ' / '
                tip += develop
            tip = tip[: min(500, len(tip))]

            subject = Subject.objects.create(
                id=data['id'],
                sub_cat=sub_cat,
                img=data['img'],
                namechs=data['namechs'],
                namejp=data['namejp'],
                name=name,
                cat=data['cat'],
                dateid=dateid,
                date=date,
                star=data['star'],
                votes=votes,
                rank=rank,
                tip=tip,
                platform=platform
            )

        elif sub_cat == 'real':
            if len(Subject.objects.filter(id=data['id'])) != 0:
                continue
            eps = data['eps']
            director = data['director']
            author = data['author']
            actor = data['actor']
            tip = ''
            if eps != '':
                tip += eps + '话'
            if datestr != '':
                if tip != '':
                    tip += ' / '
                tip += datestr
            if director != '':
                if tip != '':
                    tip += ' / '
                tip += director
            if author != '':
                if tip != '':
                    tip += ' / '
                tip += author
            if actor != '':
                if tip != '':
                    tip += ' / '
                tip += actor
            tip = tip[: min(500, len(tip))]

            subject = Subject.objects.create(
                id=data['id'],
                sub_cat=sub_cat,
                img=data['img'],
                namechs=data['namechs'],
                namejp=data['namejp'],
                name=name,
                cat=data['cat'],
                dateid=dateid,
                date=date,
                star=data['star'],
                votes=votes,
                rank=rank,
                tip=tip,
                country=data['country']
            )
        for x in tag:
            Tag.objects.get_or_create(name=x, sub_cat=sub_cat)
            t = Tag.objects.get(name=x, sub_cat=sub_cat)
            t.cnt += 1
            subject.tag.add(t)
            t.save()
        subject.save()

    f.close()

if __name__ == "__main__":
    main()
    print('Done!')
