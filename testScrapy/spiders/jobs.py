# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import os
from testScrapy.items import Match

class JobsSpider(scrapy.Spider):
    name = "jobs"
    # recibe argumentos de main_liga
    def __init__(self, *args, **kwargs):
        super(JobsSpider, self).__init__(*args, **kwargs) 

        pais = kwargs.get('pais')
        if not pais:
            raise ValueError('No pais given')
        
        temporada = kwargs.get('temporada')
        if not temporada:
            raise ValueError('No temporada given')        
        
        self.detailedStats = True
        self.allowed_domains = ["football-data.mx-api.enetscores.com",'json.mx-api.enetscores.com']
        self.start_urls = [
        "http://football-data.mx-api.enetscores.com/page/xhr/standings/"
        ]
        #countries = ['Mexico']
        self.countries = [pais]
        self.seasons = [temporada]
        #seasons = ['2009/2010','2008/2009']
        #seasons = ['2012/2013','2011/2012','2010/2011']
        #seasons = ['2015/2016','2014/2015','2013/2014']       
        self.stages = []
        self.matches = []
        #self.liga="Mexico Liga MX"
        #self.liga="England Premier League"
        seasons_subs=str(temporada)+"_"+str(temporada[8:2])
        print(seasons_subs)

 #COUNTRY
    def parse(self,response):      
        for country in self.countries:
            href = response.xpath('//li[text()[contains(.,"'+country+'")]]/@data-snippetparams').re_first('"params":"(.+)"')
            url = 'http://football-data.mx-api.enetscores.com/page/xhr/standings/' + str(href)
            yield scrapy.Request(url, callback=self.parseLeague,meta={'country':country})
    
    #LEAGUE
    def parseLeague(self,response):
        country = response.meta['country']
        #selection = response.xpath('//div[@class="mx-dropdown mx-country-template-stage-selector"]/ul/li/text()').extract()
        selection = response.xpath('(//div[@class="mx-dropdown mx-country-template-stage-selector"])[2]/ul/li/text()').extract()        
        print(selection)
        i='1'
        print("Please choose a league from "+str(country)+" :")
        for idx, element in enumerate(selection):
            print("{}) {}".format(idx+1,element))
        i = input("Enter number: ")
        try:
            if 0 < int(i) <= len(selection):
                league_sel=selection[int(i)-1]               
        except:
        for el in selection:
            if el==league_sel:
                league = el
        href = response.xpath('//li[text()[contains(.,"'+league+'")]]/@data-snippetparams').re_first('"params":"(.+)"')
        url = 'http://football-data.mx-api.enetscores.com/page/xhr/standings/' + href
        yield scrapy.Request(url, callback=self.parseSeason,meta={'country':country,'league':league})
      
    #SEASON  
    def parseSeason(self,response):
        country = response.meta['country']
        league = response.meta['league']
        for season in self.seasons:
            href = response.xpath('//li[text()[contains(.,"'+season+'")]]/@data-snippetparams').re_first('"params":"(.+)"')
            url = 'http://football-data.mx-api.enetscores.com/page/xhr/standings/' + str(href)
        yield scrapy.Request(url, callback=self.parseMatches,meta={'country':country,'league':league,'season':season})
    
    #OPEN SEASON
    def parseMatches(self,response):
        country = response.meta['country']
        league = response.meta['league']
        season = response.meta['season']
        href = response.xpath('//div[contains(@class,"mx-matches-finished-betting_extended")]/@data-params').re_first('params":"(.+)/')
        url = 'http://football-data.mx-api.enetscores.com/page/xhr/stage_results/' + href
        first_stage_url = url + '/1'
        yield scrapy.Request(first_stage_url, callback=self.parseStage, meta={'href':href,'country':country,'league':league,'season':season})
    
    #LOOP STAGES
    def parseStage(self,response):
        country = response.meta['country']
        league = response.meta['league']
        season = response.meta['season']
        href = response.meta['href']   
        url = 'http://football-data.mx-api.enetscores.com/page/xhr/stage_results/' + href
        totalPages = response.xpath('//span[contains(@class,"mx-pager-next")]/@data-params').re_first('total_pages": "([0-9]+)"')
        if not self.stages:
            iterateStages = range(1,int(totalPages)+1)
        else:
            iterateStages = self.stages
            
        for stage in iterateStages:
            full_stage_url = url + '/' + str(stage)
            yield scrapy.Request(full_stage_url, callback=self.parseAllMatchesInStage,dont_filter = True, meta={'stage':stage,'country':country,'league':league,'season':season})

    #MATCHES IN STAGE  
    def parseAllMatchesInStage(self, response):
        country = response.meta['country']
        league = response.meta['league']
        season = response.meta['season']
        stage = response.meta['stage']
        #print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII3")

        #matchesDataEventList = response.xpath('//a[@class="mx-link mx-hide"]/@data-event').extract()
        #nueva linea
        matchesDataEventList = response.xpath('//a[@class="mx-link mx-hide mx-translate-attributes"]/@data-event').extract()
        #nueva lineas
        
        timestamp_date      =response.xpath('//span[contains(@class,"mx-time-startdate")]/text()').extract()
        id_teams_home_away  =response.xpath('//a[contains(@class,"mx-link")]/@data-team').extract()
        teams_home_away     =response.xpath('//a[contains(@class,"mx-link")]/text()').re(r'[aA-zZ].+')
        score_home       =response.xpath('//span[contains(@class,"mx-js-res-home mx-res-home")]/text()').extract()
        score_away       =response.xpath('//span[contains(@class,"mx-js-res-away mx-res-away")]/text()').extract()
        #print("aqui esta esto mero :")
        List_time=list()
        col = 3
        row = int(len(timestamp_date)/col)
        List_time = [timestamp_date[col*i : col*(i+1)] for i in range(row)]
              #print(i)
            #print(timestamp_date[0]+timestamp_date[1]+timestamp_date[2])
        #print("bien")
        #print(List_time)

        #print(teams_home_away[0]+teams_home_away[1])
        #print(id_teams_home_away[0]+id_teams_home_away[2])
        #print(score_home[0])
        #print(score_away[0])
        #nueva lineas
        
        dateList = response.xpath('//span[@class="mx-time-startdatetime"]/text()').extract()
        #print("aaaaaaaaaaaaaaaa:"+str(matchesDataEventList))
        matchList = list()
        if len(self.matches) >= 1:
            for match in self.matches:
                matchList.append(matchesDataEventList[match-1])
        else:
            matchList = list(matchesDataEventList)
            #print("00000000000"+str(matchList))
            
        counter = 0
        for matchId in matchList:
            match = Match()
            match["matchId"] = matchId
            match["country"] = country
            match["league"] = league
            match["season"] = season
            date = dateList[counter]
            match["date"] = date
            
            url = 'http://football-data.mx-api.enetscores.com/page/xhr/match_center/' + matchId + '/'
            counter += 1
            #print("############################################################################")
            #print(matchList)
            #print(url)
            #print("############################################################################")
           
            yield scrapy.Request(url, callback=self.parseMatchGeneralStats,meta={'match':match})


    #MATCH GENERAL STATS
    def parseMatchGeneralStats(self, response):
        match = response.meta['match']
        
        stage = response.xpath('//span[@class="mx-stage-name"]/text()').re_first('\s([0-9]+)')
        match["stage"] = stage
        
        #validate_status= response.xpath('//span[@class="mx-time mx-show-notstarted"]').re('\t+([^\n]+[^\t]+)\n+\t+')
        validate_status= response.xpath('//div[@class="mx-team-home-name mx-break-small"]/a/@data-team').extract()
        
        print("############################################################################")
        print(match)        
        print(stage)        
        print(str(validate_status)+"status"        )
        print("############################################################################")

        if validate_status==['']:
            print("############################################################################")
            print("Aqui")
            teamId_h = response.xpath('//div[@class="mx-team-home-name mx-break-small"]/a/@data-team').extract()
            teamId_a = response.xpath('//div[@class="mx-team-away-name mx-break-small"]/a/@data-team').extract()
            teamAcronym_h = response.xpath('//div[@class="mx-team-home-name mx-show-small"]/a/text()').re('\t+([^\n]+[^\t]+)\n+\t+')
            teamAcronym_a = response.xpath('//div[@class="mx-team-away-name mx-show-small"]/a/text()').re('\t+([^\n]+[^\t]+)\n+\t+')
            homeTeamGoal = response.xpath('//div[@class="mx-res-home "]/@data-res').extract_first()
            awayTeamGoal = response.xpath('//div[@class="mx-res-away "]/@data-res').extract_first()
            match['homeTeamFullName'] = 'no_hay_datos'
            match['awayTeamFullName'] = 'no_hay_datos'
            match['homeTeamAcronym'] = teamAcronym_h[0]
            match['awayTeamAcronym'] = teamAcronym_a[0]
            match['homeTeamId'] = teamId_h[0]
            match['awayTeamId'] = teamId_a[0]
            match['homeTeamGoal'] = homeTeamGoal
            match['awayTeamGoal'] = awayTeamGoal
        else:
            print("############################################################################")
            print("Aqui22")
            fullTeamName_h = response.xpath('//div[@class="mx-team-home-name mx-break-small"]/a/text()').re('\t+([^\n]+[^\t]+)\n+\t+')
            fullTeamName_a = response.xpath('//div[@class="mx-team-away-name mx-break-small"]/a/text()').re('\t+([^\n]+[^\t]+)\n+\t+')
            teamId_h = response.xpath('//div[@class="mx-team-home-name mx-break-small"]/a/@data-team').extract()
            teamId_a = response.xpath('//div[@class="mx-team-away-name mx-break-small"]/a/@data-team').extract()
            teamAcronym_h = response.xpath('//div[@class="mx-team-home-name mx-show-small"]/a/text()').re('\t+([^\n]+[^\t]+)\n+\t+')
            teamAcronym_a = response.xpath('//div[@class="mx-team-away-name mx-show-small"]/a/text()').re('\t+([^\n]+[^\t]+)\n+\t+')
            homeTeamGoal = response.xpath('//div[@class="mx-res-home "]/@data-res').extract_first()
            awayTeamGoal = response.xpath('//div[@class="mx-res-away "]/@data-res').extract_first()
            #print ("0_1_2_3_4_5_6_7_8_9_a"+str(stage))
            match['homeTeamFullName'] = fullTeamName_h[0]
            match['awayTeamFullName'] = fullTeamName_a[0]
            match['homeTeamAcronym'] = teamAcronym_h[0]
            match['awayTeamAcronym'] = teamAcronym_a[0]
            match['homeTeamId'] = teamId_h[0]
            match['awayTeamId'] = teamId_a[0]
            match['homeTeamGoal'] = homeTeamGoal
            match['awayTeamGoal'] = awayTeamGoal
        matchId = match['matchId']
        
        #print ("0_1_2_3_4_5_6_7_8_9_g"+str(matchId))
        url = 'http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/' + matchId + '%2Fv2_lineup/'
        yield scrapy.Request(url, callback=self.parseSquad,meta={'match':match})


    #MATCH SQUADS
    def parseSquad(self, response):
        match = response.meta['match']
        #players = response.xpath('//div[@class="mx-lineup-incident-name"]/text()').extract()
        players =  response.xpath('//a[contains(@class,"mx-link")]/text()').re(r'[aA-zZ].+')
        playersId = response.xpath('//a/@data-player').extract()
        subsId = response.xpath('//div[@class="mx-lineup-container mx-float-left"]//div[@class="mx-collapsable-content"]//a/@data-player').extract()
        titularPlayerId = [x for x in playersId if x not in subsId]
        # player x y pitch position
        playersX = response.xpath('//div[contains(@class,"mx-lineup-pos")]/@class').re('mx-pos-row-([0-9]+)\s')
        playersY = response.xpath('//div[contains(@class,"mx-lineup-pos")]/@class').re('mx-pos-col-([0-9]+)\s')
        playersPos = response.xpath('//div[contains(@class,"mx-lineup-pos")]/@class').re('mx-pos-([0-9]+)\s')
        """print("###PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        print("players:"+str(players))
        print("###IDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDID")
        print("playersId:"+str(playersId))
        print("###XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("playersX:"+str(playersX))        
        print("###YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
        print("playersY:"+str(playersY))
        print("###TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        print("playersY:"+str(titularPlayerId))
        print("###POSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOSPOS")
        print("playersY:"+str(playersPos))
        """

        #print("playersY:"+str(players[11:22]))
        #print("playersPos:"+str(titularPlayerId))

        match['homePlayers'] = players[:18]
        match['homePlayersId'] = playersId[:18]
        #match['homePlayersX'] = playersX[11:18]
        #match['homePlayersY'] = titularPlayerId[11:18]      
       
        match['awayPlayers'] = players[18:36]
        match['awayPlayersId'] = playersId[18:36]
        #match['awayPlayersX'] = playersX[29:36]
        #match['awayPlayersY'] = titularPlayerId[29:36]
        
        matchId = match['matchId']
        if self.detailedStats:
            url = 'http://json.mx-api.enetscores.com/live_data/actionzones/' + matchId + '/0?_=1'
            
            yield scrapy.Request(url, callback=self.parseMatchEvents,meta={'match':match})
        else:
            yield match


    #MATCH EVENTS
    def parseMatchEvents(self, response):
        #match = response.meta['match']
        #matchId = match['matchId']
        #url = 'http://json.mx-api.enetscores.com/live_data/actionzones/' + matchId + '/0?_=1'
        match = response.meta['match']
        jsonresponse = json.loads(response.body_as_unicode())
        
        try:
           
            goal = [{"id_team":s["team"],"min":s["elapsed"],"comment":s["comment"],"id_player":s["player1"],"type_goal":s["goal_type"]}  for s in jsonresponse["i"] if s['type']=='goal']            
                
            shoton = [{"id_team":s["team"],"id_jugador":s["player1"],"min":s["elapsed"],"tipo_disparo":s["subtype"]}  for s in jsonresponse["i"] if s['type']=='shoton']
            card = [{"id_team":s["team"],"id_jugador":s["player1"],"min":s["elapsed"],"tarjeta":s["card_type"]}  for s in jsonresponse["i"] if s['type']=='card']
            shotoff = [s for s in jsonresponse["i"] if s['type']=='shotoff']
            foulcommit = [s for s in jsonresponse["i"] if s['type']=='foulcommit']
            corner = [s for s in jsonresponse["i"] if s['type']=='corner']
            subtypes = [s for s in jsonresponse["i"] if 'subtype' in s]
            cross = [s for s in subtypes if s['subtype']=='cross']            
            possession_a = [{"min":s["elapsed"],"homepos":s["homepos"],"awaypos":s["awaypos"]} for s in subtypes if s['subtype']=='possession']
            a=0
            b=0
            for i in possession_a:
              a=a+int(i['homepos'])
              b=b+int(i['awaypos'])
            possession=[{"home_pos_prom":a/len(possession_a),"away_pos_prom":b/len(possession_a)}]
            
            match['goal'] = goal
            match['shoton'] = shoton
            match['shotoff'] = 'shotoff'
            match['foulcommit'] = 'foulcommit'
            match['card'] = card
            match['cross'] = 'cross'
            match['corner'] = 'corner'
            match['possession'] = possession
        
        except:
            e = sys.exc_info()[0]
            print ('No Match Events: ' + str(e))
            
        yield match


#print("Inicia limpieza de csv")
#os.system("CleanCsv.py "+self.seasons_subs)


