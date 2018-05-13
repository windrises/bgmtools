#coding=utf-8
import collections
import json
import sys
import scrapy
reload(sys)
sys.setdefaultencoding('utf-8')

def getCookie():
    s = '*******************************'
    cookie = {}
    s = s.replace(' ', '').split(';')
    for x in s:
        x = x.split('=')
        cookie[x[0]] = x[1]
    return cookie

class subject(scrapy.spiders.Spider):
    f = open('subject.json', 'a')
    f2 = open('comment.json', 'a')
    error = open('subject_error.txt', 'a')
    # ff = open('./copy2/subject.json')
    # has = {}
    name = 'subject'
    cookie = getCookie()
    #allowed_domains = ['https://bgm.tv']
    start_urls = []
    # ii = 1
    # for line in ff:
    #     data = ''
    #     try:
    #         data = json.loads(line)
    #     except:
    #         line = line.replace('\\', '').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
    #         try:
    #             data = json.loads(line)
    #         except:
    #             print ii
    #         print ii
    #         print '-----------------------------'
    #     ii += 1
    #     id = data['id']
    #     has[id] = 1
    for i in range(1, 245555):
    # # for i in range(1, 236597):
    #     # if has.has_key(i) == False:
        start_urls.append('https://bgm.tv/subject/' + str(i))
    #     start_urls.append('https://mirror.bgm.rin.cat/subject/' + str(i))
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=self.cookie)

    def parse(self, response):
        id = response.url
        id = id[id.rfind('/') + 1:]
        message = response.xpath('//*[@id="colunmNotice"]/div/h2/text()').extract()
        if len(message) != 0:
            self.error.write(id + '\n')
            self.error.flush()
            return
        # if self.has.has_key(int(id)) == True:
        #     return
        sub_cat = response.xpath('//a[@class="focus chl"]/@href').extract()
        if len(sub_cat) == 0:
            sub_cat = response.xpath('//a[@class="focus chl anime"]/@href').extract()
        if len(sub_cat) == 0:
            sub_cat = response.xpath('//a[@class="focus chl real"]/@href').extract()
        if len(sub_cat) == 0:
            self.error.write('--------' + id + '\n')
            self.error.flush()
            return
        sub_cat = sub_cat[0]
        sub_cat = sub_cat[1:]

        tag = response.xpath('//div[@class="subject_tag_section"]/div/a/span/text()').extract()
        img = response.xpath('//div[@id="bangumiInfo"]/div/div/a/img/@src').extract()
        namechs = response.xpath(u'//span[./text()="中文名: "]/following::text()[1]').extract()
        namejp = response.xpath('//h1[@class="nameSingle"]/a/text()').extract()
        cat = response.xpath('//h1[@class="nameSingle"]/small/text()').extract()
        star = response.xpath('//span[@class="number"]/text()').extract()
        rank = response.xpath('//small[@class="alarm"]/text()').extract()
        if len(rank) == 1:
            rank[0] = rank[0][1:]
        votes = response.xpath('//div[@id="ChartWarpper"]/div/small/span/text()').extract()
        period = 0

        all = []
        allkey = []

        if sub_cat == 'anime':
            eps = response.xpath(u'//span[./text()="话数: "]/following::text()[1]').extract()
            date = response.xpath(u'//span[./text()="放送开始: "]/following::text()[1]').extract()
            if len(date) == 0:
                date = response.xpath(u'//span[./text()="上映年度: "]/following::text()[1]').extract()
            if len(date) == 0:
                date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
            author = response.xpath(u'//span[./text()="原作: "]/following::text()[1]').extract()
            director = response.xpath(u'//span[./text()="导演: "]/following::text()[1]').extract()
            personset = response.xpath(u'//span[./text()="人物设定: "]/following::text()[1]').extract()
            period = response.xpath('//*[@id="subject_detail"]/div[1]/ul/li').extract()
            period = len(period)
            if len(cat) > 0 and cat[0] == u'剧场版':
                if period == 0:
                    period = 1
                period *= 90
            else:
                if period == 0:
                    period = 13
                period *= 24
            all = [namechs, namejp, cat, eps, date, star, rank, votes, author, director, personset, img]
            allkey = ['namechs', 'namejp', 'cat', 'eps', 'date', 'star', 'rank', 'votes', 'author', 'director', 'personset', 'img']
        elif sub_cat == 'book':
            eps = response.xpath(u'//span[./text()="话数: "]/following::text()[1]').extract()
            date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
            painter = response.xpath(u'//span[./text()="作画: "]/following::text()[1]').extract()
            author = response.xpath(u'//span[./text()="作者: "]/following::text()[1]').extract()
            pub = response.xpath(u'//span[./text()="出版社: "]/following::text()[1]').extract()
            pages = response.xpath(u'//span[./text()="页数: "]/following::text()[1]').extract()
            all = [namechs, namejp, cat, eps, date, star, rank, votes, painter, author, pub, pages, img]
            allkey = ['namechs', 'namejp', 'cat', 'eps', 'date', 'star', 'rank', 'votes', 'painter', 'author',
                      'pub', 'pages', 'img']
        elif sub_cat == 'music':
            date = response.xpath(u'//span[./text()="发售日期: "]/following::text()[1]').extract()
            artist = response.xpath(u'//span[./text()="艺术家: "]/following::text()[1]').extract()
            all = [namechs, namejp, cat, date, star, rank, votes, artist, img]
            allkey = ['namechs', 'namejp', 'cat', 'date', 'star', 'rank', 'votes', 'artist', 'img']
        elif sub_cat == 'game':
            date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
            if len(date) == 0:
                date = response.xpath(u'//span[./text()="发行日期: "]/following::text()[1]').extract()
            platform = response.xpath(u'//span[./text()="平台: "]/following::text()[1]').extract()
            for i in range(1, len(platform)):
                platform[0] += '、' + platform[i]
            type = response.xpath(u'//span[./text()="游戏类型: "]/following::text()[1]').extract()
            develop = response.xpath(u'//span[./text()="开发: "]/following::text()[1]').extract()
            all = [namechs, namejp, cat, date, star, rank, votes, platform, type, develop, img]
            allkey = ['namechs', 'namejp', 'cat', 'date', 'star', 'rank', 'votes', 'platform',
                      'type', 'develop', 'img']
        elif sub_cat == 'real':
            eps = response.xpath(u'//span[./text()="集数: "]/following::text()[1]').extract()
            date = response.xpath(u'//span[./text()="开始: "]/following::text()[1]').extract()
            director = response.xpath(u'//span[./text()="导演: "]/following::text()[1]').extract()
            author = response.xpath(u'//span[./text()="编剧: "]/following::text()[1]').extract()
            actor = response.xpath(u'//span[./text()="主演: "]/following::text()[1]').extract()
            country = response.xpath(u'//span[./text()="国家/地区: "]/following::text()[1]').extract()
            all = [namechs, namejp, cat, eps, date, star, rank, votes, director, author, actor, country, img]
            allkey = ['namechs', 'namejp', 'cat', 'eps', 'date', 'star', 'rank', 'votes', 'director', 'author',
                        'actor', 'country', 'img']

        cur = collections.OrderedDict()
        cur['id'] = int(id)
        cur['sub_cat'] = sub_cat
        for i in range(0, len(all)):
            if len(all[i]) >= 1:
                cur[allkey[i]] = all[i][0].strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace('\\', '\\\\').replace('"', '\\"')
            else:
                cur[allkey[i]] = ''
        cur['period'] = period
        if len(tag) > 0:
            for i in range(0, len(tag)):
                tag[i] = tag[i].replace('\\', '\\\\').replace('"', '\\"')
            cur['tag'] = tag
        else:
            cur['tag'] = []

        ss = json.dumps(cur)
        self.f.write(str(str(ss).decode('unicode_escape')) + '\n')
        if int(id) % 100 == 0:
            self.f.flush()
            self.f2.flush()

        suf = ['/wishes', '/collections', '/doings', '/on_hold', '/dropped']
        if sub_cat == 'anime':
            for s in suf:
                yield scrapy.Request(url=response.url + s, meta={'flag': 1}, cookies=self.cookie, callback=self.parse2)

    def parse2(self, response):
        url = response.url.split('/')
        sid = int(url[-2])
        cat = url[-1].split('?')[0]
        all = response.xpath('//*[@id="memberUserList"]/li')
        for x in all:
            user_name = x.xpath('div/strong/a/@href').extract()[0]
            user_name = user_name[user_name.rfind('/') + 1:]
            star = x.xpath('div/strong/a/span[2]/@class').extract()
            if len(star) == 0:
                star = 0
            else:
                star = star[0]
                star = int(star[5: star.find(' ')])
            time = x.xpath('div/p/text()').extract()[0]
            comment = x.xpath('div/text()').extract()[-1]
            comment = comment.strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace('\\', '\\\\').replace('"', '\\"')
            # print uid,avatar,star,uname,time,comments
            cur = collections.OrderedDict()
            cur['user_name'] = user_name
            cur['sid'] = sid
            cur['cat'] = cat
            cur['star'] = star
            cur['time'] = time
            cur['comment'] = comment
            ss = json.dumps(cur)
            self.f2.write(str(str(ss).decode('unicode_escape')) + '\n')
        flag = response.meta['flag']
        if flag == 1 and len(all) > 0:
            pages = response.xpath('//*[@id="multipage"]/div/a/@href').extract()
            page_num = 1
            if len(pages) != 0:
                pa = pages[-1]
                pb = pages[-2]
                pa = int(pa[pa.find('=') + 1:])
                pb = int(pb[pb.find('=') + 1:])
                page_num = max(pa, pb)
            for i in range(2, page_num + 1):
                yield scrapy.Request(url=response.url + '?page=' + str(i), meta={'flag': 2}, cookies=self.cookie, callback=self.parse2)

class user(scrapy.spiders.Spider):
    f = open('user.json', 'a')
    error = open('user_error.txt', 'a')
    nick_error = open('nick_error.txt', 'a')
    # ff = open('./copy2/user.json')
    # has = {}
    name = 'user'
    #allowed_domains = ['https://bgm.tv']
    start_urls = []
    # ii = 1
    # for line in ff:
    #     data = ''
    #     try:
    #         data = json.loads(line)
    #     except:
    #         line = line.replace('\\', '').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
    #         try:
    #             data = json.loads(line)
    #         except:
    #             print ii
    #         print ii
    #         print '-----------------------------'
    #     ii += 1
    #     id = data['id']
    #     has[id] = 1
    start_urls.append('https://mirror.bgm.rin.cat/user/1')
    def parse(self, response):
        for i in range(1, 418036):
            # if self.has.has_key(i) == False:
            yield scrapy.Request(url='https://mirror.bgm.rin.cat/user/' + str(i), meta={'id': i}, callback=self.parse2)

    def parse2(self, response):
        id = response.meta['id']
        user_name = response.url
        user_name = user_name[user_name.rfind('/') + 1:]
        avatar = response.xpath('//*[@id="headerProfile"]/div/div[1]/h1/div[2]/a/span/@style').extract()
        if len(avatar) == 0:
            self.error.write(user_name + '\n')
            self.error.flush()
            return
        nick_name = response.xpath('//*[@id="headerProfile"]/div/div[1]/h1/div[3]/a/text()').extract()
        if len(nick_name) > 0:
            nick_name = nick_name[0]
        else:
            nick_name = ''
            self.nick_error.write(str(id) + '\n')
        avatar = avatar[0]
        avatar = avatar[avatar.find('(') + 2: avatar.find('?')]
        if avatar[-1] == '\'':
            avatar = avatar[:-1]
        signup_time = response.xpath('//*[@id="user_home"]/div[1]/ul/li[1]/span[2]/text()').extract()[0]
        signup_time = signup_time[: signup_time.find(' ')]
        ban = response.xpath('//*[@id="main"]/div/div[2]/h3').extract()
        ban = len(ban)
        cur = collections.OrderedDict()
        cur['id'] = id
        cur['user_name'] = user_name
        cur['nick_name'] = nick_name.strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace('\\', '\\\\').replace('"', '\\"')
        cur['signup_time'] = signup_time
        cur['ban'] = ban
        cur['avatar'] = avatar
        ss = json.dumps(cur)
        self.f.write(str(str(ss).decode('unicode_escape')) + '\n')
        if id % 1000 == 0:
            self.f.flush()
