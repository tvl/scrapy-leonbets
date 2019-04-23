# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from leonbets.items import MatchInfo
from urllib.parse import parse_qs
from datetime import date, datetime, timezone, timedelta


class LeonbetsSpider(Spider):
    name = "line"
    allowed_domains = ['leonbets.com']
    today  = date.today()
    tomorrow  = date.today()+timedelta(days=1)
    start_urls = [
            'https://www.leonbets.com/events/Soccer'
            ]

    def start_requests(self):
        for u in self.start_urls:
            request = Request(url=u, callback=self.parse_index)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse_index(self, response):
        start_url = 'http://www.soccerway.mobi/'
        links = response.xpath('//th[@class="competition-link"]//a/@href').extract()
        for l in links:
            #self.log('URL: {}'.format(start_url+l))
            request = Request(url=start_url+l, callback=self.parse_competition)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse_round(self, response):
        start_url = 'http://www.soccerway.mobi/'
        links = response.xpath('//td[@class="score-time status"]//a/@href').extract()
        for l in links:
            #self.log('URL: {}'.format(start_url+l))
            request = Request(url=start_url+l, callback=self.parse_match)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request


    def parse_group(self, response):
        start_url = 'http://www.soccerway.mobi/'
        links = response.xpath('//td[@class="score-time status"]//a/@href').extract()
        for l in links:
            #self.log('URL: {}'.format(start_url+l))
            request = Request(url=start_url+l, callback=self.parse_match)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request


    def parse_competition(self, response):
        start_url = 'http://www.soccerway.mobi/'
        links = response.xpath('//td[@class="score-time status"]//a/@href').extract()
        for l in links:
            #self.log('URL: {}'.format(start_url+l))
            request = Request(url=start_url+l, callback=self.parse_match)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request
        groups = response.xpath('//select[@name="group_id"]/option/@value').extract()
        for g in groups:
            request = Request(url=start_url+g, callback=self.parse_group)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request
        competition_id = int(parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract_first())['id'][0])
        if competition_id in [308, 327, 366, 570]:
            rounds = response.xpath('//select[@name="round_id"]/option/@value').extract()
            for r in rounds:
                request = Request(url=start_url+r, callback=self.parse_round)
                request.meta['proxy'] = 'http://127.0.0.1:8118'
                yield request


    def parse_match(self, response):
        item = MatchInfo()
        item['id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a/@href').extract()[3])['id'][0]
        item['area'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/text()').extract()[1]
        item['competition'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/text()').extract()[2]
        item['home_team'] = response.xpath('//div[@class="container left"]//a/text()').extract_first()
        item['away_team'] = response.xpath('//div[@class="container right"]//a/text()').extract_first()
        item['ht_last5'] = ''.join(response.xpath('//div[@class="container left"]//a/text()').extract()[1:6])
        item['at_last5'] = ''.join(response.xpath('//div[@class="container right"]//a/text()').extract()[1:6])
        item['datetime'] = datetime.fromtimestamp(int(response.xpath('//div[@class="details clearfix"]/dl/dt[.="Date"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Date"]//span/@data-value').extract_first()), timezone.utc).isoformat(' ')
        #item['competition'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Competition"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Competition"]/a/text()').extract_first()
        item['game_week'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Game week"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Game week"]/text()').extract_first()
        item['kick_off'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Kick-off"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Kick-off"]//span/text()').extract_first()
        item['venue'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Venue"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Venue"]//a/text()').extract_first()
        item['updated'] = datetime.utcnow().isoformat(' ')
        yield item
        return item
        #self.log('URL: {}'.format(response.url))

