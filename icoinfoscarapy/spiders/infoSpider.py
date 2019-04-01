import scrapy
from icoinfoscarapy.items import IcoinfoscarapyItem  # 引入item
import time
import random

#同时爬去详情页面信息
class itemSpider(scrapy.Spider):
    # beginpage=1
    # endpage=500
    # pageT=20
    # witeTime=30#秒
    # pageN = beginpage
    name = 'infoSpider'

    rootUrl="https://icobench.com"

    def start_requests(self):
         # 获取值，也就是爬取时传过来的参数
        self.beginpage =int(getattr(self, 'beginpage', 1))
        self.endpage =int(getattr(self, 'endpage', 5))
        self.pageT = int(getattr(self, 'pageT', 20))
        self.witeTime =int(getattr(self, 'witeTime', 30))
        self.pageN = self.beginpage
        url = 'https://icobench.com/icos?page=%s&filterSort=started-asc' % self.beginpage
        yield scrapy.Request(url, self.parse)  # 发送请求爬取参数内容

    def parse(self, response):
        icos = response.css('div.ico_list tr')
        subN=1
        for v in icos:
            item = IcoinfoscarapyItem()
            ico=v.css('td')
            if ico is None or len(ico)==0:
                continue
            #名称
            item['name']=ico.css('td.ico_data div.content a.name::text').extract_first()
            #详情链接
            item['info_href']=self.rootUrl+ico.css('td.ico_data div.content a.name::attr(href)').extract_first()
            #介绍
            other_info=ico.css('td.ico_data div.content p *::text').extract()
            item['other']=other_info[0]
            # Restrictions,Whitelist,countries
            item['restrictions_KYC'], item['whitelist'], item['countries'] = 'None', 'None', 'None'
            for it in range(1,len(other_info)):
                if other_info[it] == 'Restrictions KYC:':
                    item['restrictions_KYC'] = other_info[it + 1]
                if other_info[it] == 'Whitelist:':
                    item['whitelist'] = other_info[it + 1]
                if other_info[it] == 'Countries:':
                    item['countries'] = other_info[it + 1]
            # [
            #     'Volentix is building a decentralized digital assets exchange connected with a secure multi-currency cross-blockchain peer-to-peer wallet.',
            #     'Restrictions KYC:',
            #     ' Yes ',
            #     '|',
            #     ' ',
            #     'Whitelist:',
            #     ' Yes ',
            #     '|',
            #     ' ',
            #     'Countries:',
            #     ' USA, China']
            #时间，评分
            rmv=ico.css('td.rmv *::text').extract()
            #数据类型
            item['rate']=float(rmv[2])
            item['start'] = self.formatDate(rmv[0])
            item['end'] = self.formatDate(rmv[1])
            #页码
            item['page']=self.pageN
            #页内序号
            item['subN'] = subN
            subN+=1

            #item['team'], item['tags'], item['whitepaper_url'], item['introduction'], item[
            #    'about'] = 'None', 'None', 'None', 'None', 'None'
            #详情页面的爬取
            # 每爬一个网页的等待0～1秒
            time.sleep(random.random())
            yield scrapy.Request(item['info_href'], meta={'item': item}, callback=self.info_parse)

            #yield item
        next_page = self.rootUrl+response.css('div.pages a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.pageN+=1
            #控制
            if self.pageN%self.pageT==0:
                time.sleep(self.witeTime)
            if self.pageN>self.endpage:
                return ;
            #每爬一个网页的列表随机等待2+秒
            time.sleep(2+ 4*random.random())
            yield scrapy.Request(next_page, callback=self.parse)

    def formatDate(self,string):
        #07 Jan 2019
        slist=string.split(" ")
        e2n = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
               'Nov': 11, 'Dec': 12}
        if len(slist)==3:
            return "%s/%s/%s" %(slist[2] ,e2n[slist[1]] ,slist[0])
        else:
            return "1/1/1";


    def info_parse(self,response):

        item = response.meta['item']
        # 一级内页数据提取
        ico_information = response.css('div.ico_information')
        item['team'] = ico_information.css('div.name h2::text').extract_first()
        item['introduction'] = ico_information.css('p::text').extract_first()
        item['tags'] = ','.join(ico_information.css('div.categories *::text').extract())
        item['whitepaper_url'] = response.css('div.navigation_mobile div.tabs a[href$=".pdf"]::attr(href)').extract_first()
        item['about'] = '\n'.join(response.css('div.tab_content#about p::text').extract())
        #item['introduction'],item['about']='None','None'

        # 保存数据
        yield item
