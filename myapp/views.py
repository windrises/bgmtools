#coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import urllib2
import time
import random
from bs4 import BeautifulSoup
from myapp.models import AnimeTag
from myapp.models import Anime
from myapp.models import Book
from myapp.models import BookTag
from myapp.models import Music
from myapp.models import MusicTag
from myapp.models import Game
from myapp.models import GameTag
from myapp.models import Real
from myapp.models import RealTag
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf-8')
f = open('log.txt', 'a')

# Create your views here.
def mylog(s):
    print s
    f.write(s + '\n')

def home(request):
    string = '么么哒'
    return HttpResponse(string)

def bgmtools(request):
    string = '<a href="/bgmtools/contrast/">对比</a><br> \
             <a href="/bgmtools/multitag/">多标签</a>'
    return HttpResponse(string)

def contrast(request, url):
    a = ''
    b = ''
    s = '***************new viewer****************'
    mylog(s)
    dic = {'rand' : random.randint(0, 6)}
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
        return HttpResponseRedirect('/bgmtools/contrast/' + cat + '@' + a + '&' + b)
    elif url != '':
        mylog(url)
        url = url.split('@')
        cat = url[0]
        if cat != 'anime' and cat != 'book' and cat != 'music' and cat != 'game' and cat != 'real':
            return render(request, 'contrast.html', {'dic': {'error': 'error', 'rand': random.randint(0, 6)}})
        if len(url) != 2:
            url = ['', '']
        else:
            url = url[1].split('&')
        a = ''
        b = ''
        if len(url) == 2:
            a = url[0].strip()
            b = url[1].strip()
        elif len(url) == 1:
            a = url[0].strip()
        else:
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
        dic = run(a, b, f, cat)
    f.flush()
    return render(request, 'contrast.html', {'dic' : dic})

def getrand(times, cat):
    mxusr = 373679
    mxcnt = 0
    rt = ''
    for i in range(0 , times):
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
            tcnt = int(ss[p2 + 1 : p3])
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
        self.soup = ''

    def run(self):
        for page in self.pages:
            ss = 'page' + str(page)
            mylog(ss)
            url = 'https://bgm.tv/' + self.cat + '/list/' + self.uid + '/collect?page=' + str(page)
            myheaders = {'User-Agent': 'Chrome/61.0.3163.100'}
            req = urllib2.Request(url=url, headers=myheaders)
            self.str = urllib2.urlopen(req).read()
            self.soup = BeautifulSoup(self.str, 'html.parser', from_encoding='utf-8')
            self.result.extend(self.soup.find('ul', class_='browserFull'))
    def get_result(self):
        return self.result
    def get_soup(self):
        return self.soup

#@cache_page(60 * 15)
def get_items(cat, uid, pages):
    threads = []
    pages -= 1
    tdnum = min(pages, 6)
    for p in range(1, tdnum):
        threads.append(myThread(cat, uid, range(pages * p / tdnum + 1, pages * (p + 1) / tdnum + 1)))
    threads.append(myThread(cat, uid, range(pages * tdnum / tdnum + 1, pages + 2)))
    for x in threads:
        x.start()
    items = []
    for x in threads:
        x.join()
        titems = x.get_result()
        items.extend(titems)
    return items

def run(a, b, f, cat):
    ss = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print ss
    f.write(ss + '\n')
    nicka = ''; nickb = ''; avatera = ''; avaterb = ''
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
    a = ta[1 : ]
    avatera = str(soupa.find('span', class_='avatarNeue avatarSize75'))
    avatera = avatera[avatera.find('/') + 2 : avatera.find(')') - 1]
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
    b = tb[1 : ]
    avaterb = str(soupb.find('span', class_='avatarNeue avatarSize75'))
    avaterb = avaterb[avaterb.find('/') + 2 : avaterb.find(')') - 1]
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

    print nicka, nickb
    ss = a + ' ' + b
    f.write(ss + '\n')

    titemsa = threada.get_result()
    titemsb = threadb.get_result()
    itemsa.extend(titemsa)
    itemsb.extend(titemsb)
    if pagesa > 1:
        titemsa = get_items(cat, a, pagesa)
        itemsa.extend(titemsa)
    if pagesb > 1:
        titemsb = get_items(cat, b, pagesb)
        itemsb.extend(titemsb)

    for itema in itemsa:
        itemida = itema.a['href']
        itemida = itemida[itemida.rfind('/') + 1 : ]
        for itemb in itemsb:
            itemidb = itemb.a['href']
            itemidb = itemidb[itemidb.rfind('/') + 1 : ]
            if itemida == itemidb:
                id.append(itemida)
                img.append(itema.img['src'])
                tip.append(itema.find('p', class_='info tip').get_text())
                namechs.append(itema.find('a', class_='l').get_text())
                tnamejp = itema.find('small', class_='grey')
                if not tnamejp is None:
                    namejp.append(tnamejp.get_text())
                else:
                    namejp.append('')

                staraflag = 0
                for i in range(1, 11):
                    tstara = itema.find('span', class_='sstars' + str(i) + ' starsinfo')
                    if not tstara is None:
                        staraflag = 1
                        stara.append('sstars' + str(i) + ' starsinfo')
                        break
                if staraflag == 0:
                    stara.append('None')
                datea.append(itema.find('span', class_='tip_j').get_text())
                ttagsa = itema.find('span', class_='tip')
                if not ttagsa is None:
                    tagsa.append(ttagsa.get_text())
                else:
                    tagsa.append('')
                ttxta = itema.find('div', class_='text')
                if not ttxta is None:
                    txta.append(ttxta.get_text())
                else:
                    txta.append('')

                starbflag = 0
                for i in range(1, 11):
                    tstarb = itemb.find('span', class_='sstars' + str(i) + ' starsinfo')
                    if not tstarb is None:
                        starbflag = 1
                        starb.append('sstars' + str(i) + ' starsinfo')
                        break
                if starbflag == 0:
                    starb.append('None')
                dateb.append(itemb.find('span', class_='tip_j').get_text())
                ttagsb = itemb.find('span', class_='tip')
                if not ttagsb is None:
                    tagsb.append(ttagsb.get_text())
                else:
                    tagsb.append('')
                ttxtb = itemb.find('div', class_='text')
                if not ttxtb is None:
                    txtb.append(ttxtb.get_text())
                else:
                    txtb.append('')

                break
    ss = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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
            sa = int(stara[i][6 : stara[i].find(' ')])
            sb = int(starb[i][6 : starb[i].find(' ')])
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

    dic = {'a' : a, 'b' : b, 'nicka' : nicka, 'nickb' : nickb, 'avatera' : avatera, 'avaterb' : avaterb, 'rand' : rand, 'cat' : cat,
        'info0' : zip(id1[0], img1[0], namechs1[0], namejp1[0], stara1[0], starb1[0], tagsa1[0], tagsb1[0], datea1[0], dateb1[0], txta1[0], txtb1[0], tip1[0]),
        'info1': zip(id1[1], img1[1], namechs1[1], namejp1[1], stara1[1], starb1[1], tagsa1[1], tagsb1[1], datea1[1], dateb1[1], txta1[1], txtb1[1], tip1[1]),
        'info2': zip(id1[2], img1[2], namechs1[2], namejp1[2], stara1[2], starb1[2], tagsa1[2], tagsb1[2], datea1[2], dateb1[2], txta1[2], txtb1[2], tip1[2])}
    return dic

def getAll(url):
    if url == 'anime':
        return Anime.objects.all()
    elif url == 'book':
        return Book.objects.all()
    elif url == 'music':
        return Music.objects.all()
    elif url == 'game':
        return Game.objects.all()
    elif url == 'real':
        return Real.objects.all()

@cache_page(60 * 15)
def multitag(request, url):
    print request,url
    f.write(str(request) + '  ----------------  ' + str(url) + '\n')
    f.flush()
    if url != 'anime' and url != 'book' and url != 'music' and url != 'game' and url != 'real':
        url = 'anime'
    if request.method == 'POST':
        print request.POST
        f.write('++++++++++++++++++  ' + str(request.POST) + '\n')
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
                page = int(request.POST['page'])
            except:
                page = 1
        result = []
        if part == 'part1':
            tag = request.POST['data']
            print tag
            f.write(tag + '\n')
            f.flush()
            if tag == '':
                all = []
                if url == 'anime':
                    all = AnimeTag.objects.all()
                elif url == 'book':
                    all = BookTag.objects.all()
                elif url == 'music':
                    all = MusicTag.objects.all()
                elif url == 'game':
                    all = GameTag.objects.all()
                elif url == 'real':
                    all = RealTag.objects.all()
                all = all.order_by('-cnt')
                onepage = 80
                maxpage = (len(all) + onepage - 1)/ onepage
                if page > maxpage or page == 'maxpage':
                    page = maxpage
                if page < 1:
                    page = 1
                start = (page - 1) * onepage
                end = min(page * onepage, len(all))
                data = []
                for i in range(start, end):
                    data.append([all[i].name, all[i].cnt])
                return JsonResponse({'data': data, 'page' : page, 'maxpage' : maxpage})
            else:
                result = getAll(url)
                result = result.filter(tag__name=tag)
                result = result.order_by('name')
        else:
            tag = request.POST['tag']
            print tag
            f.write(tag + '\n')
            f.flush()
            cat = request.POST['cat']
            time = request.POST['time']
            sorttp = request.POST['sort']
            sorttp = sorttp.split(' ')
            tag = tag.split('&')
            result = getAll(url)
            for i in range(0, len(tag) - 1):
                result = result.filter(tag__name = tag[i])
            if cat != '全部':
                if cat == '其他':
                    cat = ''
                if url == 'game':
                    result = result.filter(platform__contains = cat)
                elif url == 'real':
                    result = result.filter(country__contains = cat)
                elif url == 'anime' or url == 'music':
                    result = result.filter(cat = cat)
            if time != 'timeall':
                result = result.filter(time__contains = time)

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
        hottag.sort(key=lambda d:d[1], reverse=True)
        hottag = hottag[ : 100]

        return JsonResponse({'data' : data,'rand' : random.randint(0, 6), 'tag' : hottag, 'page' : page, 'maxpage' : maxpage})
    return render(request, 'multitag_' + url + '.html')


