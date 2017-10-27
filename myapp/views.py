#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import time
import random
from bs4 import BeautifulSoup

# Create your views here.

def home(request):
	string = '么么哒'
	return HttpResponse(string)

def bgmtools(request):
	a = ''
	b = ''
	f = open('log.txt', 'a')
	s = '***************new viewer****************'
	print s
	f.write(s + '\n')
	dic = {'rand' : random.randint(0, 6)}
	if request.method == 'POST':
		txt = request.POST['search_text']
		txt = txt.strip()
		txt = txt.split()
		mxcnt = 373679
		if len(txt) == 2:
			a = txt[0].strip()
			b = txt[1].strip()
		elif len(txt) == 1:
			a = txt[0].strip()
			b = str(random.randint(1, mxcnt))
		elif len(txt) == 0:
			a = str(random.randint(1, mxcnt))
			b = str(random.randint(1, mxcnt))
		ss = '-------------------new post---------------------  type ' + str(len(txt))
		print ss
		f.write(ss + '\n')
		dic = run(a, b, f)
		f.close()

	return render(request, 'bgmtools.html', {'dic' : dic})

def run(a, b, f):
	ss = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print ss
	f.write(ss + '\n')
	nicka = ''
	nickb = ''
	avatera = ''
	avaterb = ''
	itemsa = []
	itemsb = []
	id = []
	img = []
	namechs = []
	namejp = []
	tip = []
	stara = []
	starb = []
	tagsa = []
	tagsb = []
	datea = []
	dateb = []
	txta = []
	txtb = []
	rand = random.randint(0, 6)
	myheaders = {'User-Agent': 'Chrome/61.0.3163.100'}
	flaga = 1
	flagb = 1
	for i in range(1, 999999):
		print 'page' + str(i)
		f.write('page' + str(i) + '\n')
		if flaga == 1:
			urla = 'https://bgm.tv/anime/list/' + a + '/collect?page=' + str(i)
			reqa = urllib2.Request(url=urla, headers=myheaders)
			stra = urllib2.urlopen(reqa).read()
			soupa = BeautifulSoup(stra, 'html.parser', from_encoding='utf-8')
			titemsa = soupa.find('ul', class_='browserFull')
		if flagb == 1:
			urlb = 'https://bgm.tv/anime/list/' + b + '/collect?page=' + str(i)
			reqb = urllib2.Request(url=urlb, headers=myheaders)
			strb = urllib2.urlopen(reqb).read()
			soupb = BeautifulSoup(strb, 'html.parser', from_encoding='utf-8')
			titemsb = soupb.find('ul', class_='browserFull')

		if i == 1:
			if (stra.find('出错了') != -1 or strb.find('出错了') != -1):
				ss = 'error ' + a + ' ' + b
				print ss
				f.write(ss + '\n')
				return {'error': 'error', 'rand': random.randint(0, 6)}

			nicka = soupa.find('h1', class_='nameSingle').find('div', class_='inner').a.get_text()
			ta = soupa.find('h1', class_='nameSingle').find('small', class_='grey').get_text()
			a = ta[1 : ]
			avatera = str(soupa.find('span', class_='avatarNeue avatarSize75'))
			avatera = avatera[avatera.find('/') + 2 : avatera.find(')') - 1]

			nickb = soupb.find('h1', class_='nameSingle').find('div', class_='inner').a.get_text()
			tb = soupb.find('h1', class_='nameSingle').find('small', class_='grey').get_text()
			b = tb[1 : ]
			avaterb = str(soupb.find('span', class_='avatarNeue avatarSize75'))
			avaterb = avaterb[avaterb.find('/') + 2 : avaterb.find(')') - 1]

			print nicka,nickb
			ss = a + ' ' + b
			f.write(ss + '\n')

		if len(titemsa) == 0 and len(titemsb) == 0:
			break
		if len(titemsa) == 0:
			flaga = 0
		if len(titemsb) == 0:
			flagb = 0
		for itema in titemsa:
			itemsa.append(itema)
		for itemb in titemsb:
			itemsb.append(itemb)

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
	print ss
	f.write(ss + '\n')
	ss = 'suc end'
	print ss
	f.write(ss + '\n')
	dic = {'a' : a, 'b' : b, 'nicka' : nicka, 'nickb' : nickb, 'avatera' : avatera, 'avaterb' : avaterb, 'rand' : rand,
		'info' : zip(id, img, namechs, namejp, stara, starb, tagsa, tagsb, datea, dateb, txta, txtb, tip)}
	return dic


