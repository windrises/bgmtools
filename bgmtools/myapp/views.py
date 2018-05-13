#coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import urllib2
import time
import random
import datetime
import calendar
import json
from bs4 import BeautifulSoup
import django.utils.timezone as timezone
from myapp.models import Tag
from myapp.models import Subject
from myapp.models import User
from myapp.models import Comment
from myapp.models import AverageScore
from myapp.models import AllAverageScore
from myapp.models import Cache
from myapp.models import RcmdIndex
from myapp.models import RcmdedList
from myapp.models import RcmdItem
from myapp.models import RcmdSub
from myapp.models import RcmdUser
from myapp.models import Settings
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf-8')
f = open('log.txt', 'a')
timeout = 0

# Create your views here.
def mylog(s):
    print s
    f.write(s + '\n')
    f.flush()

def access_control(data):
    response = HttpResponse(json.dumps(data))
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response

def home(request):
    string = '么么哒'
    return HttpResponse(string)

def bgmtools(request):
    string = '<a href="/bgmtools/contrast/">对比</a><br> \
             <a href="/bgmtools/multitag/">多标签</a> \
             <a href="/bgmtools/review/">时光机</a>'
    return HttpResponse(string)

def contrast(request, url):
    a = ''
    b = ''
    s = '***************new viewer****************'
    mylog(s)
    dic = {'rand': random.randint(0, 6)}
    if request.method == 'POST':
        cat = request.POST['cat']
        txt = request.POST['search_text']
        txt = txt.strip()
        txt = txt.split()

        if len(txt) == 2:
            a = txt[0].strip()
            b = txt[1].strip()
        elif len(txt) == 1:
            a = txt[0].strip()
            b = getrand(5, cat)
        elif len(txt) == 0:
            a = getrand(3, cat)
            b = getrand(3, cat)
        ss = '-------------------new post---------------------  ' + a + ' ' + b + ' type ' + str(len(txt)) + '  cat ' + cat
        mylog(ss)
        return HttpResponseRedirect('/bgmtools/contrast/?category=' + cat + '&id1=' + a + '&id2=' + b)
    elif url != '' or len(request.GET.keys()) > 0:
        mylog(url)
        cat = ''
        a = ''
        b = ''
        if url.find('@') != -1:
            url = url.split('@')
            cat = url[0]
            if len(url) != 2:
                url = ['', '']
            else:
                url = url[1].split('&')

            if len(url) == 2:
                a = url[0].strip()
                b = url[1].strip()
            elif len(url) == 1:
                a = url[0].strip()
            else:
                return render(request, 'contrast.html', {'dic': {'error': 'error', 'rand': random.randint(0, 6)}})
        else:
            cat = request.GET.get('category')
            a = request.GET.get('id1')
            b = request.GET.get('id2')
            if cat is None or a is None or b is None:
                return render(request, 'contrast.html', {'dic': {'error': 'error', 'rand': random.randint(0, 6)}})
        if cat != 'anime' and cat != 'book' and cat != 'music' and cat != 'game' and cat != 'real':
            return render(request, 'contrast.html', {'dic': {'error': 'error', 'rand': random.randint(0, 6)}})
        tp = 2
        if a == '' and b == '':
            a = getrand(3, cat)
            b = getrand(3, cat)
            tp = 0
        elif a == '':
            a = getrand(5, cat)
            tp = 1
        elif b == '':
            b = getrand(5, cat)
            tp = 1
        ss = '-------------------new post---------------------  ' + a + ' ' + b + ' type ' + str(tp) + '  cat ' + cat
        mylog(ss)
        global timeout
        timeout = 0
        dic = run(a, b, f, cat)
    f.flush()
    return render(request, 'contrast.html', {'dic': dic})

def getrand(times, cat):
    mxusr = 399029
    mxcnt = 0
    rt = ''
    for i in range(0, times):
        tcnt = 0
        a = str(random.randint(1, mxusr))
        myheaders = {'User-Agent': 'Chrome/61.0.3163.100'}
        urla = 'https://bgm.tv/' + cat + '/list/' + a + '/collect'
        reqa = urllib2.Request(url=urla, headers=myheaders)
        stra = urllib2.urlopen(reqa).read()
        soupa = BeautifulSoup(stra, 'html.parser', from_encoding='utf-8')
        ss = str(soupa.find('ul', class_='navSubTabs'))
        p1 = ss.find('过')
        if p1 == -1:
            tcnt = 0
        else:
            p2 = ss.find('(', p1)
            p3 = ss.find(')', p2)
            tcnt = int(ss[p2 + 1: p3])
        if tcnt >= mxcnt:
            rt = a
            mxcnt = tcnt
    return rt

class myThread(threading.Thread):
    def __init__(self, cat, uid, pages):
        threading.Thread.__init__(self)
        self.cat = cat
        self.uid = uid
        self.pages = pages
        self.result = []
        self.str = ''
        self.soup = BeautifulSoup(self.str, 'html.parser', from_encoding='utf-8')

    def run(self):
        global timeout
        for page in self.pages:
            url = 'https://bgm.tv/' + self.cat + '/list/' + self.uid + '/collect?page=' + str(page)
            myheaders = {'User-Agent': 'Chrome/61.0.3163.100'}
            req = urllib2.Request(url=url, headers=myheaders)
            try:
                self.str = urllib2.urlopen(req, timeout=8)
            except:
                timeout = 1
                ss = 'page' + str(page) + ' timeout!'
                mylog(ss)
            else:
                try:
                    self.str = self.str.read()
                except:
                    timeout = 1
                    ss = 'page' + str(page) + ' read timeout!'
                    mylog(ss)
                else:
                    self.soup = BeautifulSoup(self.str, 'html.parser', from_encoding='utf-8')
                    try:
                        self.result.extend(self.soup.find('ul', class_='browserFull'))
                    except:
                        pass
                    ss = 'page' + str(page) + ' done!'
                    mylog(ss)
    def get_result(self):
        return self.result
    def get_soup(self):
        return self.soup

#@cache_page(60 * 15)
def get_items(cat, uid, pages):
    threads = []
    pages -= 1
    tdnum = min(pages, 6)
    for p in range(0, tdnum):
        threads.append(myThread(cat, uid, range(pages * p / tdnum + 2, pages * (p + 1) / tdnum + 2)))
    threads.append(myThread(cat, uid, range(pages * tdnum / tdnum + 2, pages + 2)))
    for x in threads:
        x.start()
    items = []
    for x in threads:
        x.join()
        titems = x.get_result()
        items.extend(titems)
    return items

def run(a, b, f, cat):
    ss = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    mylog(ss)
    global timeout
    nicka = ''; nickb = ''; avatara = ''; avatarb = ''
    itemsa = []; itemsb = []
    id = []; img = []; namechs = []; namejp = []; tip = []
    stara = []; starb = []; tagsa = []; tagsb = []
    datea = []; dateb = []; txta = []; txtb = []
    rand = random.randint(0, 6)

    threada = myThread(cat, a, range(1, 2))
    threadb = myThread(cat, b, range(1, 2))
    threada.start()
    threadb.start()
    threada.join()
    soupa = threada.get_soup()
    nicka = soupa.find('h1', class_='nameSingle')
    if nicka == None:
        ss = 'error ' + a + ' ' + b
        mylog(ss)
        return {'error': 'error', 'rand': random.randint(0, 6)}
    nicka = nicka.find('div', class_='inner').a.get_text()
    ta = soupa.find('h1', class_='nameSingle').find('small', class_='grey').get_text()
    a = ta[1:]
    avatara = str(soupa.find('span', class_='avatarNeue avatarSize75'))
    avatara = avatara[avatara.find('/') + 2: avatara.find(')') - 1]
    pagesa = soupa.find_all('a', class_='p')
    if len(pagesa) == 0:
        pagesa = 1
    else:
        p1 = pagesa[-1]['href']
        p2 = pagesa[-2]['href']
        p1 = p1[p1.find('=') + 1:]
        p2 = p2[p2.find('=') + 1:]
        p1 = int(p1)
        p2 = int(p2)
        pagesa = max(p1, p2)

    threadb.join()
    soupb = threadb.get_soup()
    nickb = soupb.find('h1', class_='nameSingle')
    if nickb == None:
        ss = 'error ' + a + ' ' + b
        mylog(ss)
        return {'error': 'error', 'rand': random.randint(0, 6)}
    nickb = nickb.find('div', class_='inner').a.get_text()
    tb = soupb.find('h1', class_='nameSingle').find('small', class_='grey').get_text()
    b = tb[1:]
    avatarb = str(soupb.find('span', class_='avatarNeue avatarSize75'))
    avatarb = avatarb[avatarb.find('/') + 2: avatarb.find(')') - 1]
    pagesb = soupb.find_all('a', class_='p')
    if len(pagesb) == 0:
        pagesb = 1
    else:
        p1 = pagesb[-1]['href']
        p2 = pagesb[-2]['href']
        p1 = p1[p1.find('=') + 1:]
        p2 = p2[p2.find('=') + 1:]
        p1 = int(p1)
        p2 = int(p2)
        pagesb = max(p1, p2)

    ss = a + ' ' + nicka + ' ' + b + ' ' + nickb
    mylog(ss)

    titemsa = threada.get_result()
    titemsb = threadb.get_result()
    if len(titemsa) > 0 and len(titemsb) > 0:
        itemsa.extend(titemsa)
        itemsb.extend(titemsb)
        if pagesa > 1:
            titemsa = get_items(cat, a, pagesa)
            itemsa.extend(titemsa)
        if pagesb > 1:
            if a != b:
                titemsb = get_items(cat, b, pagesb)
                itemsb.extend(titemsb)
            else:
                itemsb.extend(titemsa)

    for itema in itemsa:
        itemida = itema.a['href']
        itemida = itemida[itemida.rfind('/') + 1:]
        for itemb in itemsb:
            itemidb = itemb.a['href']
            itemidb = itemidb[itemidb.rfind('/') + 1:]
            if itemida == itemidb:
                id.append(itemida)
                img.append(itema.img['src'])
                tip.append(itema.find('p', class_='info tip').get_text())
                namechs.append(itema.find('a', class_='l').get_text())
                tnamejp = itema.find('small', class_='grey')
                if tnamejp is not None:
                    namejp.append(tnamejp.get_text())
                else:
                    namejp.append('')

                staraflag = 0
                for i in range(1, 11):
                    tstara = itema.find('span', class_='sstars' + str(i) + ' starsinfo')
                    if tstara is not None:
                        staraflag = 1
                        stara.append('sstars' + str(i) + ' starsinfo')
                        break
                if staraflag == 0:
                    stara.append('None')
                datea.append(itema.find('span', class_='tip_j').get_text())
                ttagsa = itema.find('span', class_='tip')
                if ttagsa is not None:
                    tagsa.append(ttagsa.get_text())
                else:
                    tagsa.append('')
                ttxta = itema.find('div', class_='text')
                if ttxta is not None:
                    txta.append(ttxta.get_text())
                else:
                    txta.append('')

                starbflag = 0
                for i in range(1, 11):
                    tstarb = itemb.find('span', class_='sstars' + str(i) + ' starsinfo')
                    if tstarb is not None:
                        starbflag = 1
                        starb.append('sstars' + str(i) + ' starsinfo')
                        break
                if starbflag == 0:
                    starb.append('None')
                dateb.append(itemb.find('span', class_='tip_j').get_text())
                ttagsb = itemb.find('span', class_='tip')
                if ttagsb is not None:
                    tagsb.append(ttagsb.get_text())
                else:
                    tagsb.append('')
                ttxtb = itemb.find('div', class_='text')
                if ttxtb is not None:
                    txtb.append(ttxtb.get_text())
                else:
                    txtb.append('')
                break
    ss = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    mylog(ss)
    ss = 'suc end'
    mylog(ss)
    id1 = [[], [], []]; img1 = [[], [], []]; namechs1 = [[], [], []]; namejp1 = [[], [], []]; stara1 = [[], [], []]; starb1 = [[], [], []]
    tagsa1 = [[], [], []]; tagsb1 = [[], [], []]; datea1 = [[], [], []]; dateb1 = [[], [], []]; txta1 = [[], [], []]; txtb1 = [[], [], []]; tip1 = [[], [], []]

    for i in range(0, len(id)):
        if stara[i] == 'None' or starb[i] == 'None':
            sa = 10
            sb = 1
        else:
            sa = int(stara[i][6: stara[i].find(' ')])
            sb = int(starb[i][6: starb[i].find(' ')])
        if sa >= 7 and sb >= 7:
            id1[0].append(id[i]); img1[0].append(img[i]); namechs1[0].append(namechs[i]); namejp1[0].append(namejp[i])
            stara1[0].append(stara[i]); starb1[0].append(starb[i]); tagsa1[0].append(tagsa[i]); tagsb1[0].append(tagsb[i])
            datea1[0].append(datea[i]); dateb1[0].append(dateb[i]); txta1[0].append(txta[i]); txtb1[0].append(txtb[i]); tip1[0].append(tip[i])
        elif sa < 7 and sb < 7:
            id1[1].append(id[i]); img1[1].append(img[i]); namechs1[1].append(namechs[i]); namejp1[1].append(namejp[i])
            stara1[1].append(stara[i]); starb1[1].append(starb[i]); tagsa1[1].append(tagsa[i]); tagsb1[1].append(tagsb[i])
            datea1[1].append(datea[i]); dateb1[1].append(dateb[i]); txta1[1].append(txta[i]); txtb1[1].append(txtb[i]); tip1[1].append(tip[i])
        else:
            id1[2].append(id[i]); img1[2].append(img[i]); namechs1[2].append(namechs[i]); namejp1[2].append(namejp[i])
            stara1[2].append(stara[i]); starb1[2].append(starb[i]); tagsa1[2].append(tagsa[i]); tagsb1[2].append(tagsb[i])
            datea1[2].append(datea[i]); dateb1[2].append(dateb[i]); txta1[2].append(txta[i]); txtb1[2].append(txtb[i]); tip1[2].append(tip[i])

    dic = {'a': a, 'b': b, 'nicka': nicka, 'nickb': nickb, 'avatara': avatara, 'avatarb': avatarb, 'rand': rand, 'cat': cat, 'timeout': timeout,
        'info0': zip(id1[0], img1[0], namechs1[0], namejp1[0], stara1[0], starb1[0], tagsa1[0], tagsb1[0], datea1[0], dateb1[0], txta1[0], txtb1[0], tip1[0]),
        'info1': zip(id1[1], img1[1], namechs1[1], namejp1[1], stara1[1], starb1[1], tagsa1[1], tagsb1[1], datea1[1], dateb1[1], txta1[1], txtb1[1], tip1[1]),
        'info2': zip(id1[2], img1[2], namechs1[2], namejp1[2], stara1[2], starb1[2], tagsa1[2], tagsb1[2], datea1[2], dateb1[2], txta1[2], txtb1[2], tip1[2])}
    return dic

@cache_page(60 * 15)
def multitag(request, url):
    ss = str(request) + '  ----------------  ' + url
    mylog(ss)
    url = url.replace('/', '')
    if url != 'anime' and url != 'book' and url != 'music' and url != 'game' and url != 'real':
        url = 'anime'
    if request.method == 'POST':
        ss = '++++++++++++++++++  ' + str(request.POST)
        mylog(ss)
        part = request.POST['part']
        page = request.POST['page']
        curpage = request.POST['curpage']
        if page == '|‹':
            page = 1
        elif page == '‹‹':
            page = int(curpage) - 1
        elif page == '››':
            page = int(curpage) + 1
        elif page == '›|':
            page = 'maxpage'
        else:
            try:
                page = int(page)
            except:
                page = 1
        result = []
        if part == 'part1':
            tag = request.POST['data']
            mylog(tag)
            if tag == '':
                all = Tag.objects.filter(sub_cat=url)
                all = all.order_by('-cnt')
                onepage = 80
                maxpage = (len(all) + onepage - 1) / onepage
                if page > maxpage or page == 'maxpage':
                    page = maxpage
                if page < 1:
                    page = 1
                start = (page - 1) * onepage
                end = min(page * onepage, len(all))
                data = []
                for i in range(start, end):
                    data.append([all[i].name, all[i].cnt])
                return JsonResponse({'data': data, 'page': page, 'maxpage': maxpage})
            else:
                result = Subject.objects.filter(sub_cat=url, tag__name=tag)
                result = result.order_by('name')
        else:
            tag = request.POST['tag']
            mylog(tag)
            cat = request.POST['cat']
            time = request.POST['time']
            sorttp = request.POST['sort']
            sorttp = sorttp.split(' ')
            tag = tag.split('&')
            result = Subject.objects.filter(sub_cat=url)
            for i in range(0, len(tag) - 1):
                result = result.filter(tag__name=tag[i])
            if cat != '全部':
                if cat == '其他':
                    cat = ''
                if url == 'game':
                    result = result.filter(platform__contains=cat)
                elif url == 'real':
                    result = result.filter(country__contains=cat)
                elif url == 'anime' or url == 'music':
                    result = result.filter(cat=cat)
            if time != 'timeall':
                result = result.filter(date__contains=time)

            pre = ''
            if sorttp[1] == '1':
                pre = '-'
            if sorttp[0] == 'sortbyname':
                result = result.order_by(pre + 'name')
            elif sorttp[0] == 'sortbydate':
                result = result.order_by(pre + 'date')
            elif sorttp[0] == 'sortbyrank':
                result = result.order_by(pre + 'rank')
            elif sorttp[0] == 'sortbyvotes':
                result = result.order_by(pre + 'votes')
        onepage = 20
        maxpage = (len(result) + onepage - 1) / onepage
        if page > maxpage or page == 'maxpage':
            page = maxpage
        if page < 1:
            page = 1
        start = (page - 1) * onepage
        end = min(page * onepage, len(result))
        data = []
        for i in range(start, end):
            x = result[i]
            dic = {}
            star = x.star
            starstr = ''
            if star == '0.0':
                star = ''
            if star != '':
                starstr = 'sstars' + str(int(round(float(star)))) + ' starsinfo'
            votes = x.votes
            if votes == 0:
                votes = ''
            elif votes < 10:
                votes = '(少于10人评分)'
            else:
                votes = '(' + str(votes) + '人评分)'
            img = x.img
            img = img.replace('/c/', '/s/')

            dic['id'] = x.id; dic['img'] = img
            dic['namechs'] = x.namechs; dic['namejp'] = x.namejp
            dic['tip'] = x.tip; dic['star'] = star
            dic['rank'] = x.rank; dic['votes'] = votes
            dic['starstr'] = starstr
            data.append(dic)

        hottag = []
        cache_tag = ''
        cache_value = ''
        if part == 'part1':
            cache_tag = tag
        else:
            if len(tag) == 2:
                cache_tag = tag[0]
            elif len(tag) == 1:
                cache_tag = ' '
        if len(hottag) == 0:
            if cache_tag != '':
                key = 'multitag ' + url + ' ' + cache_tag
                cache_value = Cache.objects.filter(key=key)
                if len(cache_value) != 0:
                    cache_value = cache_value[0].value
                else:
                    cache_value = ''
            if cache_value == '':
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
            else:
                cache_value = cache_value.split(',')
                for x in cache_value:
                    x = x.split(' ')
                    hottag.append((x[0], x[1]))

        return JsonResponse({'data': data, 'tag': hottag, 'page': page, 'maxpage': maxpage})
    cat_dic = {'anime': '动画', 'book': '书籍', 'music': '音乐', 'game': '游戏', 'real': '三次元'}
    return render(request, 'multitag.html', {'cat': url, 'cat_chs': cat_dic[url],'cat_focus': json.dumps(url)})

def get_timeid(time, interval):
    time = time.split('.')
    dt1 = datetime.datetime(1900, 1, 1)
    dt2 = ''
    dt3 = ''
    try:
        if len(time) == 3:
            dt2 = datetime.datetime(int(time[0]), int(time[1]), int(time[2]))
            dt3 = dt2
        elif len(time) == 2:
            year = int(time[0])
            month = int(time[1])
            dt2 = datetime.datetime(year, month, 1)
            dt3 = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
        elif len(time) == 1:
            year = int(time[0])
            dt2 = datetime.datetime(year, 1, 1)
            dt3 = datetime.datetime(year, 12, calendar.monthrange(year, 12)[1])
        else:
            raise Exception()
    except:
        return [-1, -1]
    start = (dt2 - dt1).days
    start = (start + interval - 1) / interval * interval
    end = (dt3 - dt1).days
    end = (end + interval - 1) / interval * interval
    return [start, end]

# @cache_page(60 * 15)
def review_chart(request, url):
    ss = str(request) + '  ----------------  ' + url
    mylog(ss)
    url = url.replace('/', '')
    if request.method == 'POST' or url == 'api':
        id = ''; rank = ''
        period  = ''; check = ''; cat = ''
        request_type = 1
        interval = 7
        if request.method == 'POST':
            ss = '++++++++++++++++++  ' + str(request.POST)
            mylog(ss)
            id = request.POST['id']
            rank = request.POST['rank']
            period = request.POST['period']
            check = request.POST['check']
            cat = request.POST['category']
            if check == '':
                check = 'true'
            if cat == '':
                cat = 'anime'
        else:
            request_type = 2
            id = request.GET.get('id')
            rank = request.GET.get('rank')
            period = request.GET.get('period')
            check = request.GET.get('check')
            cat = request.GET.get('category')
            if id is None and rank is None:
                return JsonResponse({'error': '你还没有指定条目呢'})
            if id is not None and rank is not None:
                return JsonResponse({"error": "条目和名次检索只能选择一个哦"})
            if check is None:
                check = 'true'
            if cat is None:
                cat = 'anime'
        if (check != 'true' and check != 'false') or (cat != 'anime' and cat != 'book' and cat != 'music' and cat != 'game' and cat != 'real'):
            return JsonResponse({'error': '请求错误'})

        if cat != 'anime':
            interval = 21
        subjects = []
        if (request_type == 1 and id != '') or (request_type == 2 and id is not None):
            id = id.split('|')
            distinct = {}
            for x in id:
                try:
                    x = int(x)
                except:
                    return JsonResponse({'error': '输入的条目数据不对哦'})
                subject = Subject.objects.filter(id=x)
                if len(subject) == 0:
                    if request_type == 1:
                        return JsonResponse({'error': '没有查询到该条目'})
                    else:
                        return access_control({'error': '该条目暂时还未收录'})
                if x not in distinct:
                    distinct[x] = 1
                    subjects.append(subject[0])
        else:
            rank = rank.split('|')
            rank_time = 0
            if rank[0].find('.') != -1:
                if len(rank[0].split('.')) != 3:
                    return JsonResponse({'error': '输入的排名日期不对哦'})
                rank_time = get_timeid(rank[0], interval)[0]
                if rank_time == -1:
                    return JsonResponse({'error': '输入的排名日期不对哦'})
                if len(rank) == 1:
                    return JsonResponse({'error': '输入的排名数据不对哦'})
            for i, x in enumerate(rank):
                if i == 0:
                    if rank_time != 0:
                        continue
                    else:
                        if cat == 'anime':
                            rank_time = 43127
                        else:
                            rank_time = 43113
                start = end = 0
                pos = x.find('~')
                try:
                    if pos == -1:
                        start = end = int(x)
                    else:
                        start = int(x[: pos])
                        end = int(x[pos + 1:])
                    if start * end <= 0:
                        raise Exception()
                    average_scores = AverageScore.objects.filter(timeid=rank_time, subject__sub_cat=cat).exclude(rank=0).order_by('rank')
                    tot = len(average_scores)
                    if start < 0:
                        start += tot + 1
                        end += tot + 1
                    if start > end:
                        start, end = end, start
                    if start <= 0 or end > tot:
                        raise Exception()
                    if end - start >= 100:
                        return JsonResponse({'error': '条目太多了展示效果会很差的哦'})
                    for j in range(start, end + 1):
                        subjects.append(average_scores[j - 1].subject)
                except:
                    return JsonResponse({'error': '输入的排名数据不对哦'})
        if len(subjects) > 100:
            return JsonResponse({'error': '条目太多了展示效果会很差的哦'})

        period_array = []
        if (request_type == 1 and period != '') or (request_type == 2 and period is not None):
            period = period.split('|')
            for x in period:
                start = end = 0
                pos = x.find('~')
                if pos == -1:
                    [start, end] = get_timeid(x, interval)
                else:
                    start = x[: pos]
                    end = x[pos + 1:]
                    if start == '':
                        start = 0
                    else:
                        start = get_timeid(start, interval)[0]
                    if end == '':
                        if cat == 'anime':
                            end = 43127
                        else:
                            end = 43113
                    else:
                        end = get_timeid(end, interval)[0]
                if start == -1 or end == -1:
                    return JsonResponse({'error': '输入的日期数据不对哦'})
                start -= interval
                period_array.append([start, end])

        data = {'name': [], 'score': [], 'rank': [], 'people': []}
        type = 1
        if len(subjects) == 1:
            subject = subjects[0]
            name = subject.namechs
            if name == '':
                name = subject.namejp
            if name == '':
                name = str(subject.id)
            mylog(name)
            data['name'] = name
            data['time'] = []
            average_scores = ''
            if check == 'false':
                average_scores = subject.averagescore_set.all().order_by('timeid')
            else:
                average_scores = subject.averagescore_set.all().exclude(rank=0).order_by('timeid')
            for x in average_scores:
                flag = 0
                for y in period_array:
                    if y[0] <= x.timeid <= y[1]:
                        flag = 1
                        break
                if len(period_array) == 0 or flag == 1:
                    data['time'].append(x.timestr)
                    data['score'].append(round(x.score, 6))
                    data['rank'].append(x.rank)
                    data['people'].append(x.people)
        else:
            type = 2
            all_name = []
            all_score_data = []
            all_rank_data = []
            all_people_data = []
            all_timeid = []
            all_timestr = []
            tot = 0
            sparse = 1
            for subject in subjects:
                name = subject.namechs
                if name == '':
                    name = subject.namejp
                if name == '':
                    name = str(subject.id)
                score_data = []
                rank_data = []
                people_data = []
                timeid = []
                timestr= []
                average_scores = ''
                if check == 'false':
                    average_scores = subject.averagescore_set.all().order_by('timeid')
                else:
                    average_scores = subject.averagescore_set.all().exclude(rank=0).order_by('timeid')
                for x in average_scores:
                    flag = 0
                    for y in period_array:
                        if y[0] <= x.timeid <= y[1]:
                            flag = 1
                            break
                    if len(period_array) == 0 or flag == 1:
                        score_data.append(round(x.score, 4))
                        rank_data.append(x.rank)
                        people_data.append(x.people)
                        timeid.append(x.timeid)
                        timestr.append(x.timestr)
                        tot += 1
                all_name.append(name)
                all_score_data.append(score_data)
                all_rank_data.append(rank_data)
                all_people_data.append(people_data)
                all_timeid.append(timeid)
                all_timestr.append(timestr)
            if tot >= 600:
                sparse = tot / 300 * interval
            for i, name in enumerate(all_name):
                score_data = []
                rank_data = []
                people_data = []
                for j, timeid in enumerate(all_timeid[i]):
                    if timeid % sparse == 0:
                        score_data.append([all_timestr[i][j], all_score_data[i][j]])
                        rank_data.append([all_timestr[i][j], all_rank_data[i][j]])
                        people_data.append([all_timestr[i][j], all_people_data[i][j]])
                data['score'].append({'name': name, 'data': score_data})
                data['rank'].append({'name': name, 'data': rank_data})
                data['people'].append({'name': name, 'data': people_data})
        if request_type == 1:
            return JsonResponse({'data': data, 'type': type})
        else:
            return access_control(data)
    return render(request, 'review_chart.html')

@cache_page(60 * 15)
def review_list(request, url):
    ss = str(request) + '  ----------------  ' + url
    mylog(ss)
    url = url.replace('/', '')
    if url != 'anime' and url != 'book' and url != 'music' and url != 'game' and url != 'real':
        url = 'anime'
    if request.method == 'POST':
        ss = '++++++++++++++++++  ' + str(request.POST)
        mylog(ss)
        page = request.POST['page']
        curpage = request.POST['curpage']
        if page == '|‹':
            page = 1
        elif page == '‹‹':
            page = int(curpage) - 1
        elif page == '››':
            page = int(curpage) + 1
        elif page == '›|':
            page = 'maxpage'
        else:
            try:
                page = int(page)
            except:
                return JsonResponse({'error': 'error'})
        time = request.POST['time']
        timeid = 0
        if time == 'last':
            if url == 'anime':
                timeid = 43127
            else:
                timeid = 43113
        else:
            interval = 7
            if url != 'anime':
                interval = 21
            time = time.replace('-', '.')
            timeid = get_timeid(time, interval)[0]
        if timeid == -1:
            return JsonResponse({'error': 'error'})
        sort = request.POST['sort']
        sort = sort.split('-')
        if len(sort) != 2 or (sort[0] != 'name' and sort[0] != 'rank' and sort[0] != 'votes' and sort[0] != 'people') or (sort[1] != '0' and sort[1] != '1'):
            return JsonResponse({'error': 'error'})
        result = AverageScore.objects.filter(timeid=timeid, subject__sub_cat=url).exclude(rank=0)
        pre = ''
        if sort[0] == 'name':
            pre += 'subject__'
        elif sort[1] == '1':
            pre += '-'
        result = result.order_by(pre + sort[0])
        if sort[0] == 'name' and sort[1] == '1':
            result = result.reverse()
        onepage = 24
        maxpage = (len(result) + onepage - 1) / onepage
        if page > maxpage or page == 'maxpage':
            page = maxpage
        if page < 1:
            page = 1
        start = (page - 1) * onepage
        end = min(page * onepage, len(result))
        data = []
        for i in range(start, end):
            x = result[i]
            y = x.subject
            dic = {}
            star = x.score
            starstr = ''
            if star == 0:
                star = ''
            if star != '':
                starstr = 'sstars' + str(int(round(star))) + ' starsinfo'
                star = '%.1f' % star
            votes = x.votes
            if votes == 0:
                votes = ''
            elif votes < 10:
                votes = '(少于10人评分)'
            else:
                votes = '(' + str(votes) + '人评分)'
            img = y.img
            img = img.replace('/c/', '/s/')

            dic['id'] = y.id; dic['img'] = img
            dic['namechs'] = y.namechs; dic['namejp'] = y.namejp
            dic['tip'] = y.tip; dic['star'] = star
            dic['rank'] = x.rank; dic['votes'] = votes
            dic['starstr'] = starstr
            data.append(dic)

        return JsonResponse({'data': data, 'page': page, 'maxpage': maxpage})
    return render(request, 'review_list.html', {'cat_focus': json.dumps(url)})

def get_rcmd_index(user):
    rcmd_all = user.rcmd_index.all().filter(marked=0)
    rcmd = random.sample(rcmd_all, min(1, len(rcmd_all)))
    return rcmd

def get_rcmd_item(user, num):
    comments = user.comment_set.all().filter(subject__sub_cat='anime', star__gte=8)
    comments = random.sample(comments, num)
    rcmd = []
    for x in comments:
        rcmd_all = x.subject.rcmd_item.all()
        rcmd_all = rcmd_all[:len(rcmd_all) / 2]
        cnt = min(3, len(rcmd_all))
        rcmd += zip([x.subject.id] * cnt, random.sample(rcmd_all, cnt))
    random.shuffle(rcmd)
    return rcmd

def check_settings(sub, settings):
    if settings.score_below != 0 and float(sub.star) < settings.score_below:
        if random.random() < 0.8:
            return 0
    if settings.score_above != 0 and float(sub.star) > settings.score_above:
        if random.random() < 0.8:
            return 0
    if settings.rank_below != 0 and sub.rank < settings.rank_below:
        if random.random() < 0.8:
            return 0
    if settings.rank_above != 0 and sub.rank > settings.rank_above:
        if random.random() < 0.8:
            return 0
    if settings.rating_below != 0 and sub.votes < settings.rating_below:
        if random.random() < 0.8:
            return 0
    if settings.rating_above != 0 and sub.votes > settings.rating_above:
        if random.random() < 0.8:
            return 0
    if settings.filter_tag != '':
        for x in settings.filter_tag.split(' '):
            for y in sub.tag.all():
                if x == y.name:
                    return 0
    return 1

def recommend(request, url):
    ss = str(request) + '  ...............  ' + url
    mylog(ss)
    url = url.replace('/', '')
    if request.method == 'POST' or request.method == 'GET':
        if request.method == 'POST':
            ss = '...............  ' + str(request.POST)
            mylog(ss)
            type = request.POST['type']
            if type == 'settings_submit':
                score_below = ''; score_above = ''
                rank_below = ''; rank_above = ''
                rating_below = ''; rating_above = ''
                try:
                    score_below = float(request.POST['score_below'])
                    score_above = float(request.POST['score_above'])
                    rank_below = int(request.POST['rank_below'])
                    rank_above = int(request.POST['rank_above'])
                    rating_below = int(request.POST['rating_below'])
                    rating_above = int(request.POST['rating_above'])
                except:
                    return access_control({'status': 'value error'})
                filter_tag = request.POST['filter_tag']
                user_name = request.POST['user_name']
                user = ''
                try:
                    user = User.objects.get(user_name=user_name)
                except:
                    return access_control({'status': 'not found'})
                settings = Settings.objects.get(user=user)
                settings.score_below = score_below
                settings.score_above = score_above
                settings.rank_below = rank_below
                settings.rank_above = rank_above
                settings.rating_below = rating_below
                settings.rating_above = rating_above
                settings.filter_tag = filter_tag
                settings.save()
                return access_control({'status': '已保存'})
            elif type == 'settings_update':
                return access_control({'status': '暂未实现'})
            else:
                return access_control({'status': 'error'})
        else:
            ss = '...............  ' + str(request.GET)
            mylog(ss)
            data = {}
            type = request.GET.get('type')
            if type == 'subject':
                id = 0
                subject = ''
                try:
                    id = int(request.GET.get('id'))
                    subject = Subject.objects.get(id=id)
                except:
                    return access_control({'error': 'not found'})
                ss = subject.name
                mylog(ss)
                data = {'item': [], 'sub': []}
                for x in subject.rcmd_item.all().order_by('-weight'):
                    data['item'].append({'id': x.rcmd.id, 'img': x.rcmd.img,
                                         'name': x.rcmd.name, 'namechs': x.rcmd.namechs})
                for x in subject.rcmd_sub.all().order_by('-similarity'):
                    data['sub'].append({'id': x.rcmd.id, 'img': x.rcmd.img,
                                         'name': x.rcmd.name, 'namechs': x.rcmd.namechs})
            elif type == 'index':
                user_name = request.GET.get('user_name')
                user = ''
                try:
                    user = User.objects.get(user_name=user_name)
                except:
                    return access_control({'error': 'not found'})
                data = {'index': []}
                date = timezone.now
                rcmd_index = []
                rcmd_item = []
                if len(user.rcmd_list.all().filter(user=user, date=date)) > 0:
                    rcmd_index = user.rcmd_list.all().filter(user=user, date=date, type=0)
                    rcmd_item = user.rcmd_list.all().filter(user=user, date=date).exclude(type=0)
                else:
                    settings = Settings.objects.filter(user=user)
                    if len(settings) == 0:
                        settings = Settings.objects.create(user=user)
                    else:
                        settings = settings[0]
                    for i in range(8):
                        rcmd = get_rcmd_index(user)
                        if len(rcmd) == 0:
                            break
                        rcmd = rcmd[0]
                        if check_settings(rcmd.rcmd, settings) == 0:
                            rcmd = get_rcmd_index(user)[0]
                        flag = 1
                        for x in rcmd_index:
                            if x == rcmd:
                                flag = 0
                                break
                        if flag == 0:
                            continue
                        rcmd_index.append(rcmd)
                        marked = 0
                        if len(rcmd_index) <= 2:
                            rcmd.marked = 1
                            rcmd.save()
                            marked = 1
                        RcmdedList.objects.create(
                            user=user,
                            rcmd=rcmd.rcmd,
                            type=0,
                            marked=marked
                        )
                    rcmd_item_all = get_rcmd_item(user, 20)
                    for x in rcmd_item_all:
                        if len(rcmd_item) + len(rcmd_index) == 12:
                            break
                        if len(user.comment_set.all().filter(subject=x[1].rcmd)) == 0 \
                                and check_settings(x[1].rcmd, settings) == 1 \
                                and len(user.rcmd_list.filter(rcmd=x[1].rcmd, marked=1)) == 0:
                            rcmd_item.append(x[1])
                            marked = 0
                            if len(rcmd_item) == 1:
                                marked = 1
                            RcmdedList.objects.create(
                                user=user,
                                rcmd=x[1].rcmd,
                                type=x[0],
                                marked=marked
                            )
                rcmd_page = (len(rcmd_index) + len(rcmd_item) + 2) / 3
                for i in range(rcmd_page):
                    left = len(rcmd_index) * i / rcmd_page
                    right = len(rcmd_index) * (i + 1) / rcmd_page
                    for x in rcmd_index[left:right]:
                        data['index'].append({'id': x.rcmd.id, 'img': x.rcmd.img,
                                             'name': x.rcmd.name, 'namechs': x.rcmd.namechs})
                    left = len(rcmd_item) * i / rcmd_page
                    right = len(rcmd_item) * (i + 1) / rcmd_page
                    for x in rcmd_item[left:right]:
                        data['index'].append({'id': x.rcmd.id, 'img': x.rcmd.img,
                                              'name': x.rcmd.name, 'namechs': x.rcmd.namechs})
            elif type == 'user':
                user_name = request.GET.get('user_name')
                user = ''
                try:
                    user = User.objects.get(user_name=user_name)
                except:
                    return access_control({'error': 'not found'})
                data = {'user': []}
                for x in user.rcmd_user.all().order_by('-similarity'):
                    avatar = x.rcmd.avatar.replace('user/l', 'user/m')
                    if avatar[-1] == '\'':
                        avatar = avatar[:-1]
                    data['user'].append({'user_name': x.rcmd.user_name, 'avatar': avatar,
                                        'nick_name': x.rcmd.nick_name})
            elif type == 'recommended':
                user_name = request.GET.get('user_name')
                user = ''
                try:
                    user = User.objects.get(user_name=user_name)
                except:
                    return access_control({'error': 'not found'})
                data = {'recommended': []}
                for x in user.rcmd_list.filter(marked=1).order_by('-date'):
                    name = ''
                    if x.type != 0:
                        name = Subject.objects.get(id=x.type).name
                    data['recommended'].append({'id': x.rcmd.id, 'name': x.rcmd.name,
                                        'namechs': x.rcmd.namechs, 'date': str(x.date),
                                        'type': {'id': x.type, 'name': name}})
            elif type == 'settings':
                user_name = request.GET.get('user_name')
                user = ''
                try:
                    user = User.objects.get(user_name=user_name)
                except:
                    return access_control({'error': 'not found'})
                settings = Settings.objects.filter(user=user)
                if len(settings) == 0:
                    settings = Settings.objects.create(user=user)
                else:
                    settings = settings[0]
                data['score_below'] = settings.score_below
                data['score_above'] = settings.score_above
                data['rank_below'] = settings.rank_below
                data['rank_above'] = settings.rank_above
                data['rating_below'] = settings.rating_below
                data['rating_above'] = settings.rating_above
                data['filter_tag'] = settings.filter_tag
            else:
                return access_control({'error': 'type error'})
            return access_control(data)

    return HttpResponse('hello')
