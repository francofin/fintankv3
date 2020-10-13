from django.shortcuts import render
from requests_html import HTMLSession
# newsapi = NewsApiClient(api_key='675e79029f9440db99995410d40edebb')
from requests_html import HTMLSession
from yahoo_fin.stock_info import *
from requests_html import HTMLSession
import newsapi as np
from newsapi import NewsApiClient
from pages.models import Francois
newsapi = NewsApiClient(api_key='675e79029f9440db99995410d40edebb')
# Create your views here.
def lifestyle(request):
    import requests
    import json
    import pandas as pd
    from random import randrange

    subscription_key = "904298336d514d45babbf4e9aaf29fff"
    rapidapi_key = "feec356023msh7d505f582747ea5p199c91jsnd5a1909fc40a"
    search_term1 = "Covid"
    search_term2 = "Lifestyle"
    search_term3 = "Opinion"
    search_term4 = "Health"
    search_term5 = "Trending"
    # search_term6 = "Europe"
    # search_term7 = "China"
    # search_term8 = "Small Business"
    # search_term9 = "entnology"
    # search_term10 = "Lifestyle"
    # search_term11 = "Motivation"
    # search_term12 = "Gadgets"
    #
    #
    def get_news(search_term, subscription_key):
        url = "https://rapidapi.p.rapidapi.com/search"
        querystring = {"q":search_term,"language":"en"}
        headers = {
            'x-rapidapi-host': "webit-news-search.p.rapidapi.com",
            'x-rapidapi-key': subscription_key
        }
        response1 = requests.request("GET", url, headers=headers, params=querystring)
        content = json.loads(response1.content)

        return content

    def get_images(search_term, subscription_key):
        search_url1 = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url1, headers=headers, params=params)
        search_results1 = json.loads(response.content)

        top_item1 = search_results1['value'][randrange(len(search_results1['value']))]['thumbnailUrl']

        return top_item1

    def news_cafe(query, key):
        url = "https://newscafapi.p.rapidapi.com/apirapid/news/"
        querystring = {"q":query}
        headers = {
            'x-rapidapi-host': "newscafapi.p.rapidapi.com",
            'x-rapidapi-key': key
            }
        response1 = requests.request("GET", url, headers=headers, params=querystring)
        content = json.loads(response1.content)
        return content

    def get_trending(subscription_key):
        url = "https://rapidapi.p.rapidapi.com/trending"
        querystring = {"language":"en"}
        headers = {
            'x-rapidapi-host': "webit-news-search.p.rapidapi.com",
            'x-rapidapi-key': subscription_key
        }
        response1 = requests.request("GET", url, headers=headers, params=querystring)
        content = json.loads(response1.content)

        return content

    def ent_news(key):
        url = "https://newscafapi.p.rapidapi.com/apirapid/news/entertainment/"
        querystring = {"q":"news"}
        headers = {
            'x-rapidapi-host': "newscafapi.p.rapidapi.com",
            'x-rapidapi-key': key
            }
        response3 = requests.request("GET", url, headers=headers, params=querystring)
        content3 = json.loads(response3.content)

        return content3

    def sports_news(key):
        url = "https://newscafapi.p.rapidapi.com/apirapid/news/sports/"
        querystring = {"q":"news"}
        headers = {
            'x-rapidapi-host': "newscafapi.p.rapidapi.com",
            'x-rapidapi-key': key
            }
        response3 = requests.request("GET", url, headers=headers, params=querystring)
        content3 = json.loads(response3.content)
        return content3
    #
    covid = get_news(search_term1,rapidapi_key)
    lifestyle = get_news(search_term2, rapidapi_key)
    opinion = get_news(search_term3, rapidapi_key)
    # central_bank = get_news(search_term4, subscription_key)
    # globalization = get_news(search_term5, subscription_key)
    # europe = get_news(search_term6, subscription_key)
    # china = get_news(search_term7, subscription_key)
    # small_business = get_news(search_term8, subscription_key)
    # entno = get_news(search_term9, subscription_key)
    # lifestyle = get_news(search_term10, subscription_key)
    # motivation = get_news(search_term11, subscription_key)
    # gadgets = get_news(search_term12, subscription_key)
    #
    covid1 = get_images(search_term1,subscription_key)
    lifestyle1 = get_images(search_term2, subscription_key)
    opinion1 = get_images(search_term3, subscription_key)
    trending1 = get_news(search_term4, rapidapi_key)
    trending_images = get_images(search_term4, subscription_key)
    trending_images2 = get_images(search_term4, subscription_key)
    news_cafe1 = news_cafe('lifestyle', rapidapi_key)
    ent = ent_news(rapidapi_key)
    sports = sports_news(rapidapi_key)
    # central_bank1 = get_images(search_term4, subscription_key)
    # globalization1 = get_images(search_term5, subscription_key)
    # europe1 = get_images(search_term6, subscription_key)
    # china1 = get_images(search_term7, subscription_key)
    # small_business1 = get_images(search_term8, subscription_key)
    # entno1 = get_images(search_term9, subscription_key)
    # lifestyle1 = get_images(search_term10, subscription_key)
    # motivation1 = get_images(search_term11, subscription_key)
    # gadgets1 = get_images(search_term12, subscription_key)
    #
    covid_name = covid['data']['results'][0]['title']
    covid_url = covid['data']['results'][0]['url']
    covid_image = covid1
    covid_description = covid['data']['results'][0]['description']
    covid_source = covid['data']['results'][1]['url'].split('/')[2]

    lifestyle_name = lifestyle['data']['results'][0]['title']
    lifestyle_url = lifestyle['data']['results'][0]['url']
    lifestyle_image = lifestyle1
    lifestyle_description = lifestyle['data']['results'][0]['description']
    lifestyle_source = lifestyle['data']['results'][1]['url'].split('/')[2]

    opinion_name = opinion['data']['results'][0]['title']
    opinion_url = opinion['data']['results'][0]['url']
    opinion_image = opinion1
    opinion_description = opinion['data']['results'][0]['description']
    opinion_source = opinion['data']['results'][1]['url'].split('/')[2]

    trending1_name = trending1['data']['results'][0]['title']
    trending1_url = trending1['data']['results'][0]['url']
    trending1_source = trending1['data']['results'][0]['url'].split('/')[2]
    trending1_image = trending_images
    trending1_des = trending1['data']['results'][0]['description']

    trending2_name = trending1['data']['results'][1]['title']
    trending2_url = trending1['data']['results'][1]['url']
    trending2_source = trending1['data']['results'][1]['url'].split('/')[2]
    trending2_image = trending_images2
    trending2_des = trending1['data']['results'][1]['description']

    trending3_name = news_cafe1[0]['title']
    trending3_url = news_cafe1[0]['source_url']
    trending3_source = news_cafe1[0]['source_name']
    trending3_image = news_cafe1[0]['img']
    trending3_des = news_cafe1[0]['category']

    trending4_name = news_cafe1[1]['title']
    trending4_url = news_cafe1[1]['source_url']
    trending4_source = news_cafe1[1]['source_name']
    trending4_image = news_cafe1[1]['img']
    trending4_des = news_cafe1[1]['category']

    trending5_name = news_cafe1[2]['title']
    trending5_url = news_cafe1[2]['source_url']
    trending5_source = news_cafe1[2]['source_name']
    trending5_image = news_cafe1[2]['img']
    trending5_des = news_cafe1[2]['category']

    trending6_name = news_cafe1[3]['title']
    trending6_url = news_cafe1[3]['source_url']
    trending6_source = news_cafe1[3]['source_name']
    trending6_image = news_cafe1[3]['img']
    trending6_des = news_cafe1[3]['category']

    trending7_name = news_cafe1[4]['title']
    trending7_url = news_cafe1[4]['source_url']
    trending7_source = news_cafe1[4]['source_name']
    trending7_image = news_cafe1[4]['img']
    trending7_des = news_cafe1[4]['category']

    trending8_name = news_cafe1[5]['title']
    trending8_url = news_cafe1[5]['source_url']
    trending8_source = news_cafe1[5]['source_name']
    trending8_image = news_cafe1[5]['img']
    trending8_des = news_cafe1[5]['category']

    trending9_name = news_cafe1[6]['title']
    trending9_url = news_cafe1[6]['source_url']
    trending9_source = news_cafe1[6]['source_name']
    trending9_image = news_cafe1[6]['img']
    trending9_des = news_cafe1[6]['category']

    trending10_name = news_cafe1[7]['title']
    trending10_url = news_cafe1[7]['source_url']
    trending10_source = news_cafe1[7]['source_name']
    trending10_image = news_cafe1[7]['img']
    trending10_des = news_cafe1[7]['category']

    ent1_name = ent[0]['title']
    ent1_url = ent[0]['source_url']
    ent1_source = ent[0]['source_name']
    ent1_image = ent[0]['img']
    ent1_des = ent[0]['category']

    ent2_name = ent[1]['title']
    ent2_url = ent[1]['source_url']
    ent2_source = ent[1]['source_name']
    ent2_image = ent[1]['img']
    ent2_des = ent[1]['category']

    ent3_name = ent[2]['title']
    ent3_url = ent[2]['source_url']
    ent3_source = ent[2]['source_name']
    ent3_image = ent[2]['img']
    ent3_des = ent[2]['category']
    ent3_content = ent[2]['content']

    ent4_name = ent[3]['title']
    ent4_url = ent[3]['source_url']
    ent4_source = ent[3]['source_name']
    ent4_image = ent[3]['img']
    ent4_des = ent[3]['category']
    ent4_content = ent[3]['content']

    ent5_name = ent[4]['title']
    ent5_url = ent[4]['source_url']
    ent5_source = ent[4]['source_name']
    ent5_image = ent[4]['img']
    ent5_des = ent[4]['category']

    sports_name = sports[0]['title']
    sports_url = sports[0]['source_url']
    sports_source = sports[0]['source_name']
    sports_image = sports[0]['img']
    sports_des = sports[0]['category']

    sports1_name = sports[1]['title']
    sports1_url = sports[1]['source_url']
    sports1_source = sports[1]['source_name']
    sports1_image = sports[1]['img']
    sports1_des = sports[1]['category']


    sports2_name = sports[2]['title']
    sports2_url = sports[2]['source_url']
    sports2_source = sports[2]['source_name']
    sports2_image = sports[2]['img']
    sports2_des = sports[2]['category']
    sports2_content = sports[2]['content']

    sports3_name = sports[3]['title']
    sports3_url = sports[3]['source_url']
    sports3_source = sports[3]['source_name']
    sports3_image = sports[3]['img']
    sports3_des = sports[3]['category']
    sports3_content = sports[3]['content']


    topheadlines = newsapi.get_everything(q='Elections',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines2 = newsapi.get_everything(q='Culture',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines3 = newsapi.get_everything(q='Travel',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines4 = newsapi.get_everything(q='Exercise',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines5 = newsapi.get_everything(q='Retirement',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines6 = newsapi.get_everything(q='Global',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')

    url1 = topheadlines['articles'][0]['url']
    url2 = topheadlines2['articles'][1]['url']
    url3 = topheadlines3['articles'][1]['url']
    url4 = topheadlines4['articles'][1]['url']
    url5 = topheadlines5['articles'][1]['url']
    url6 = topheadlines6['articles'][1]['url']

    title1 = topheadlines['articles'][0]['title']
    title2 = topheadlines2['articles'][0]['title']
    title3 = topheadlines3['articles'][0]['title']
    title4 = topheadlines4['articles'][0]['title']
    title5 = topheadlines5['articles'][0]['title']
    title6 = topheadlines6['articles'][0]['title']

    source1a = topheadlines['articles'][0]['source']['name']
    source2a = topheadlines2['articles'][0]['source']['name']
    source3a = topheadlines3['articles'][0]['source']['name']
    source4a = topheadlines4['articles'][0]['source']['name']
    source5a = topheadlines5['articles'][0]['source']['name']
    source6a = topheadlines6['articles'][0]['source']['name']

    des6 = topheadlines6['articles'][0]['description']


    img1 = get_images('Elections', subscription_key)
    img2 = get_images('Culture', subscription_key)
    img3 = get_images('Travel', subscription_key)
    img4 = get_images('Exercise', subscription_key)
    img5 = get_images('Retirement', subscription_key)

    # central_bank_name = central_bank['name']
    # central_bankurl = central_bank['url']
    # central_bank_image = central_bank1
    # central_bank_description = central_bank['description']
    # central_bank_source = central_bank['provider'][0]['name']
    #
    # globalization_name = globalization['name']
    # globalization_url = globalization['url']
    # globalization_image = globalization1
    # globalization_description = globalization['description']
    # globalization_source = globalization['provider'][0]['name']
    #
    # europe_name = europe['name']
    # europe_url = europe['url']
    # europe_image = europe1
    # europe_description = europe['description']
    # europe_source = europe['provider'][0]['name']
    #
    # china_name = china['name']
    # china_url = china['url']
    # china_image = china1
    # china_description = china['description']
    # china_source = china['provider'][0]['name']
    #
    # small_business_name = small_business['name']
    # small_business_url = small_business['url']
    # small_business_image = small_business1
    # small_business_description = small_business['description']
    # small_business_source = small_business['provider'][0]['name']
    #
    # entno_name = entno['name']
    # entno_url = entno['url']
    # entno_image = entno1
    # entno_description = entno['description']
    # entno_source = entno['provider'][0]['name']
    #
    # lifestyle_name = lifestyle['name']
    # lifestyle_url = lifestyle['url']
    # lifestyle_image = lifestyle1
    # lifestyle_description = lifestyle['description']
    # lifestyle_source = lifestyle['provider'][0]['name']
    #
    # motivation_name = motivation['name']
    # motivation_url = motivation['url']
    # motivation_image = motivation1
    # motivation_description = motivation['description']
    # motivation_source = motivation['provider'][0]['name']
    #
    # gadgets_name = gadgets['name']
    # gadgets_url = gadgets['url']
    # gadgets_image = gadgets1
    # gadgets_description = gadgets['description']
    # gadgets_source = gadgets['provider'][0]['name']

    gainers = get_day_gainers()

    gainer1 = gainers.iloc[0]['Name']
    gainer1_price = gainers.iloc[0]['Price (Intraday)']
    gainer1_change = gainers.iloc[0]['% Change']

    gainer2 = gainers.iloc[1]['Name']
    gainer2_price = gainers.iloc[1]['Price (Intraday)']
    gainer2_change = gainers.iloc[1]['% Change']

    gainer3 = gainers.iloc[3]['Name']
    gainer3_price = gainers.iloc[3]['Price (Intraday)']
    gainer3_change = gainers.iloc[3]['% Change']

    gainer4 = gainers.iloc[4]['Name']
    gainer4_price = gainers.iloc[4]['Price (Intraday)']
    gainer4_change = gainers.iloc[4]['% Change']

    gainer5 = gainers.iloc[5]['Name']
    gainer5_price = gainers.iloc[5]['Price (Intraday)']
    gainer5_change = gainers.iloc[5]['% Change']


    francois = Francois.objects.all()

    context = {
        'gainer1':gainer1,
        'gainer2':gainer2,
        'gainer3':gainer3,
        'gainer4':gainer4,
        'gainer5':gainer5,
        'gainer1_change':gainer1_change,
        'gainer2_change':gainer2_change,
        'gainer3_change':gainer3_change,
        'gainer4_change':gainer4_change,
        'gainer5_change':gainer5_change,
        'covid_name':covid_name,
        'covid_url':covid_url,
        'covid_image':covid_image,
        'covid_description':covid_description,
        'covid_source':covid_source,
        'lifestyle_name':lifestyle_name,
        'lifestyle_url': lifestyle_url,
        'lifestyle_image':lifestyle_image,
        'lifestyle_description':lifestyle_description,
        'lifestyle_source':lifestyle_source,
        'opinion_name':opinion_name,
        'opinion_url':opinion_url,
        'opinion_image':opinion_image,
        'opinion_description':opinion_description,
        'opinion_source':opinion_source,
        'url1':url1,
        'url2':url2,
        'url3':url3,
        'url4':url4,
        'url5':url5,
        'url6':url6,
        'title1':title1,
        'title2':title2,
        'title3':title3,
        'title4':title4,
        'title5':title5,
        'title6':title6,
        'source1a':source1a,
        'source2a':source2a,
        'source3a':source3a,
        'source4a':source4a,
        'source5a':source5a,
        'source6a':source6a,
        'des6':des6,
        'img1':img1,
        'img2':img2,
        'img3':img3,
        'img4':img4,
        'img5':img5,
        'trending1_name':trending1_name,
        'trending1_url':trending1_url,
        'trending1_source':trending1_source,
        'trending1_image':trending1_image,
        'trending1_des':trending1_des,
        'trending2_name':trending2_name,
        'trending2_url':trending2_url,
        'trending2_source':trending2_source,
        'trending2_image':trending2_image,
        'trending2_des':trending2_des,
        'trending3_name':trending3_name,
        'trending3_url':trending3_url,
        'trending3_source':trending3_source,
        'trending3_image':trending3_image,
        'trending3_des':trending3_des,
        'trending4_name':trending4_name,
        'trending4_url':trending4_url,
        'trending4_source':trending4_source,
        'trending4_image':trending4_image,
        'trending4_des':trending4_des,
        'trending5_name':trending5_name,
        'trending5_url':trending5_url,
        'trending5_source':trending5_source,
        'trending5_image':trending5_image,
        'trending5_des':trending5_des,
        'trending6_name':trending6_name,
        'trending6_url':trending6_url,
        'trending6_source':trending6_source,
        'trending6_image':trending6_image,
        'trending6_des':trending6_des,
        'trending7_name':trending7_name,
        'trending7_url':trending7_url,
        'trending7_source':trending7_source,
        'trending7_image':trending7_image,
        'trending7_des':trending7_des,
        'trending8_name':trending8_name,
        'trending8_url':trending8_url,
        'trending8_source':trending8_source,
        'trending8_image':trending8_image,
        'trending8_des':trending8_des,
        'trending9_name':trending9_name,
        'trending9_url':trending9_url,
        'trending9_source':trending9_source,
        'trending9_image':trending9_image,
        'trending9_des':trending9_des,
        'trending10_name':trending10_name,
        'trending10_url':trending10_url,
        'trending10_source':trending10_source,
        'trending10_image':trending10_image,
        'trending10_des':trending10_des,
        'ent1_name':ent1_name,
        'ent1_url':ent1_url,
        'ent1_source':ent1_source,
        'ent1_image':ent1_image,
        'ent1_des':ent1_des,
        'ent2_name':ent2_name,
        'ent2_url':ent2_url,
        'ent2_source':ent2_source,
        'ent2_image':ent2_image,
        'ent2_des':ent2_des,
        'ent3_name':ent3_name,
        'ent3_url':ent3_url,
        'ent3_source':ent3_source,
        'ent3_image':ent3_image,
        'ent3_des':ent3_des,
        'ent3_content':ent3_content,
        'ent4_name':ent4_name,
        'ent4_url':ent4_url,
        'ent4_source':ent4_source,
        'ent4_image':ent4_image,
        'ent4_des':ent4_des,
        'ent4_content':ent4_content,
        'ent5_name':ent5_name,
        'ent5_url':ent5_url,
        'ent5_source':ent5_source,
        'ent5_image':ent5_image,
        'ent5_des':ent5_des,
        'sports_name':sports_name,
        'sports_url':sports_url,
        'sports_source':sports_source,
        'sports_image':sports_image,
        'sports_des':sports_des,
        'sports1_name':sports1_name,
        'sports1_url':sports1_url,
        'sports1_source':sports1_source,
        'sports1_image':sports1_image,
        'sports1_des':sports1_des,
        'sports2_name':sports2_name,
        'sports2_url':sports2_url,
        'sports2_source':sports2_source,
        'sports2_image':sports2_image,
        'sports2_des':sports2_des,
        'sports2_content':sports2_content,
        'sports3_name':sports3_name,
        'sports3_url':sports3_url,
        'sports3_source':sports3_source,
        'sports3_image':sports3_image,
        'sports3_des':sports3_des,
        'sports3_content':sports3_content,
        'francois':francois,
    }

    return render(request, 'lifestyle/lifestyle.html', context)
