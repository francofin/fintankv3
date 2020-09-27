from django.shortcuts import render
from requests_html import HTMLSession
# newsapi = NewsApiClient(api_key='675e79029f9440db99995410d40edebb')
from requests_html import HTMLSession
from yahoo_fin.stock_info import *
from requests_html import HTMLSession
import newsapi as np
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='675e79029f9440db99995410d40edebb')

# Create your views here.
def index(request):
    import requests
    import json
    import pandas as pd
    from random import randrange

    subscription_key = "904298336d514d45babbf4e9aaf29fff"
    rapidapi_key = "feec356023msh7d505f582747ea5p199c91jsnd5a1909fc40a"
    search_term1 = "Economy"
    search_term2 = "S&P 500"
    search_term3 = "WTI"
    search_term4 = "Politics"
    search_term5 = "China"
    # search_term6 = "Europe"
    # search_term7 = "China"
    # search_term8 = "Small Business"
    # search_term9 = "Technology"
    # search_term10 = "Lifestyle"
    # search_term11 = "Motivation"
    # search_term12 = "Gadgets"
    #
    #
    def get_news(search_term, subscription_key):
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = json.loads(response.content)
        top_item = search_results['value'][0]

        return top_item

    def get_images(search_term, subscription_key):
        search_url1 = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url1, headers=headers, params=params)
        search_results1 = json.loads(response.content)

        top_item1 = search_results1['value'][randrange(len(search_results1['value']))]['thumbnailUrl']

        return top_item1

    def get_trending(search_term, subscription_key):
        search_url1 = "https://api.cognitive.microsoft.com/bing/v7.0/news"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q":search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url1, headers=headers, params=params)
        search_results1 = json.loads(response.content)

        top_item1 = search_results1['value']

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

    def tech_news(key):
        url = "https://newscafapi.p.rapidapi.com/apirapid/news/technology/"
        querystring = {"q":"news"}
        headers = {
            'x-rapidapi-host': "newscafapi.p.rapidapi.com",
            'x-rapidapi-key': key
            }
        response3 = requests.request("GET", url, headers=headers, params=querystring)
        content3 = json.loads(response3.content)

        return content3

    def health_news(key):
        url = "https://newscafapi.p.rapidapi.com/apirapid/news/health/"
        querystring = {"q":"news"}
        headers = {
            'x-rapidapi-host': "newscafapi.p.rapidapi.com",
            'x-rapidapi-key': key
            }
        response3 = requests.request("GET", url, headers=headers, params=querystring)
        content3 = json.loads(response3.content)
        return content3
    #
    economy = get_news(search_term1,subscription_key)
    sp500 = get_news(search_term2, subscription_key)
    oil = get_news(search_term3, subscription_key)
    # central_bank = get_news(search_term4, subscription_key)
    # globalization = get_news(search_term5, subscription_key)
    # europe = get_news(search_term6, subscription_key)
    # china = get_news(search_term7, subscription_key)
    # small_business = get_news(search_term8, subscription_key)
    # techno = get_news(search_term9, subscription_key)
    # lifestyle = get_news(search_term10, subscription_key)
    # motivation = get_news(search_term11, subscription_key)
    # gadgets = get_news(search_term12, subscription_key)
    #
    economy1 = get_images(search_term1,subscription_key)
    sp5001 = get_images(search_term2, subscription_key)
    oil1 = get_images(search_term3, subscription_key)
    trending1 = get_trending(search_term4, subscription_key)
    trending_images = get_images(search_term4, subscription_key)
    trending_images2 = get_images(search_term5, subscription_key)
    news_cafe1 = news_cafe('news', rapidapi_key)
    tech = tech_news(rapidapi_key)
    health = health_news(rapidapi_key)
    # central_bank1 = get_images(search_term4, subscription_key)
    # globalization1 = get_images(search_term5, subscription_key)
    # europe1 = get_images(search_term6, subscription_key)
    # china1 = get_images(search_term7, subscription_key)
    # small_business1 = get_images(search_term8, subscription_key)
    # techno1 = get_images(search_term9, subscription_key)
    # lifestyle1 = get_images(search_term10, subscription_key)
    # motivation1 = get_images(search_term11, subscription_key)
    # gadgets1 = get_images(search_term12, subscription_key)
    #
    econ_name = economy['name']
    econ_url = economy['url']
    econ_image = economy1
    econ_description = economy['description']
    econ_source = economy['provider'][0]['name']

    sp500_name = sp500['name']
    sp500_url = sp500['url']
    sp500_image = sp5001
    sp500_description = sp500['description']
    sp500_source = sp500['provider'][0]['name']

    oil_name = oil['name']
    oil_url = oil['url']
    oil_image = oil1
    oil_description = oil['description']
    oil_source = oil['provider'][0]['name']

    trending1_name = trending1[0]['name']
    trending1_url = trending1[0]['url']
    trending1_source = trending1[0]['provider'][0]['name']
    trending1_image = trending_images
    trending1_des = trending1[0]['description']

    trending2_name = trending1[1]['name']
    trending2_url = trending1[1]['url']
    trending2_source = trending1[1]['provider'][0]['name']
    trending2_image = trending_images2
    trending2_des = trending1[1]['description']

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

    tech1_name = tech[0]['title']
    tech1_url = tech[0]['source_url']
    tech1_source = tech[0]['source_name']
    tech1_image = tech[0]['img']
    tech1_des = tech[0]['category']

    tech2_name = tech[1]['title']
    tech2_url = tech[1]['source_url']
    tech2_source = tech[1]['source_name']
    tech2_image = tech[1]['img']
    tech2_des = tech[1]['category']

    tech3_name = tech[2]['title']
    tech3_url = tech[2]['source_url']
    tech3_source = tech[2]['source_name']
    tech3_image = tech[2]['img']
    tech3_des = tech[2]['category']
    tech3_content = tech[2]['content']

    tech4_name = tech[3]['title']
    tech4_url = tech[3]['source_url']
    tech4_source = tech[3]['source_name']
    tech4_image = tech[3]['img']
    tech4_des = tech[3]['category']
    tech4_content = tech[3]['content']

    tech5_name = tech[4]['title']
    tech5_url = tech[4]['source_url']
    tech5_source = tech[4]['source_name']
    tech5_image = tech[4]['img']
    tech5_des = tech[4]['category']

    health_name = health[0]['title']
    health_url = health[0]['source_url']
    health_source = health[0]['source_name']
    health_image = health[0]['img']
    health_des = health[0]['category']

    health1_name = health[1]['title']
    health1_url = health[1]['source_url']
    health1_source = health[1]['source_name']
    health1_image = health[1]['img']
    health1_des = health[1]['category']


    health2_name = health[2]['title']
    health2_url = health[2]['source_url']
    health2_source = health[2]['source_name']
    health2_image = health[2]['img']
    health2_des = health[2]['category']
    health2_content = health[2]['content']

    health3_name = health[3]['title']
    health3_url = health[3]['source_url']
    health3_source = health[3]['source_name']
    health3_image = health[3]['img']
    health3_des = health[3]['category']
    health3_content = health[3]['content']


    topheadlines = newsapi.get_everything(q='COVID-19',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines2 = newsapi.get_everything(q='Unemployment',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines3 = newsapi.get_everything(q='Economy',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines4 = newsapi.get_everything(q='Stocks',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
    topheadlines5 = newsapi.get_everything(q='Markets',sources='bloomberg, cnbc, business-insider, reuters, financial-post', domains = 'axios.com, afr.com, bloomberg.com, businessinsider.com, cnbc.com, business.financialpost.com, politico.com, reuters.com', language='en')
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


    img1 = get_images('COVID-19', subscription_key)
    img2 = get_images('Unemployment', subscription_key)
    img3 = get_images('Fiscal Stimulus', subscription_key)
    img4 = get_images('Stocks', subscription_key)
    img5 = get_images('Financial Markets', subscription_key)

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
    # techno_name = techno['name']
    # techno_url = techno['url']
    # techno_image = techno1
    # techno_description = techno['description']
    # techno_source = techno['provider'][0]['name']
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


    api = '3da6aaea4ffa4232c7ada6b09e15af62'
    markets = requests.get(f'https://fmpcloud.io/api/v3/quotes/index?apikey={api}')
    markets_df = pd.DataFrame(json.loads(markets.content)).set_index('symbol').T
    markets_df_clean1 = markets_df.loc['name':'change']
    home_indices = markets_df_clean1[['^DJI', '^GSPC', '^IXIC', '^GSPTSE', '^RUTTR', "^VIX", "^N225", "^HSI", "^FTSE", "DX-Y.NYB"]]
    dji = home_indices['^DJI']
    gspc = home_indices['^GSPC']
    ixic = home_indices['^IXIC']
    gsptse = home_indices['^GSPTSE']
    rut = home_indices['^RUTTR']
    nikkei = home_indices['^N225']
    hang = home_indices['^HSI']
    ftse = home_indices['^FTSE']
    dollar = home_indices['DX-Y.NYB']
    vix = home_indices['^VIX']

    vix_name = vix['name']
    vix_price = vix['price']
    vix_perc = vix['changesPercentage']
    vix_dollar = vix['change']

    dollar_name = dollar['name']
    dollar_price = dollar['price']
    dollar_perc = dollar['changesPercentage']
    dollar_dollar = dollar['change']

    ftse_name = ftse['name']
    ftse_price = ftse['price']
    ftse_perc = ftse['changesPercentage']
    ftse_dollar = ftse['change']

    hang_name = hang['name']
    hang_price = hang['price']
    hang_perc = hang['changesPercentage']
    hang_dollar = hang['change']

    dji_name = dji['name']
    dji_price = dji['price']
    dji_perc = dji['changesPercentage']
    dji_dollar = dji['change']

    gspc_name = gspc['name']
    gspc_price = gspc['price']
    gspc_perc = gspc['changesPercentage']
    gspc_dollar = gspc['change']

    ixic_name = ixic['name']
    ixic_price = ixic['price']
    ixic_perc = ixic['changesPercentage']
    ixic_dollar = ixic['change']

    gsptse_name = gsptse['name']
    gsptse_price = gsptse['price']
    gsptse_perc = gsptse['changesPercentage']
    gsptse_dollar = gsptse['change']

    rut_name = rut['name']
    rut_price = rut['price']
    rut_perc = rut['changesPercentage']
    rut_dollar = rut['change']

    nikkei_name = nikkei['name']
    nikkei_price = nikkei['price']
    nikkei_perc = nikkei['changesPercentage']
    nikkei_dollar = nikkei['change']


    context = {
        'vix_name':vix_name,
        'vix_price':vix_price,
        'vix_perc':vix_perc,
        'vix_dollar':vix_dollar,
        'dollar_name':dollar_name,
        'dollar_price':dollar_price,
        'dollar_perc':dollar_perc,
        'dollar_dollar':dollar_dollar,
        'ftse_name':ftse_name,
        'ftse_price':ftse_price,
        'ftse_perc':ftse_perc,
        'ftse_dollar':ftse_dollar,
        'hang_name':hang_name,
        'hang_price':hang_price,
        'hang_perc':hang_perc,
        'hang_dollar':hang_dollar,
        'dji_name':dji_name,
        'dji_price':dji_price,
        'dji_perc':dji_perc,
        'dji_dollar':dji_dollar,
        'gspc_name':gspc_name,
        'gspc_price':gspc_price,
        'gspc_perc':gspc_perc,
        'gspc_dollar':gspc_dollar,
        'gsptse_name':gsptse_name,
        'gsptse_price':gsptse_price,
        'gsptse_perc':gsptse_perc,
        'gsptse_dollar':gsptse_dollar,
        'ixic_name':ixic_name,
        'ixic_price':ixic_price,
        'ixic_perc':ixic_perc,
        'ixic_dollar':ixic_dollar,
        'rut_name':rut_name,
        'rut_price':rut_price,
        'rut_perc':rut_perc,
        'rut_dollar':rut_dollar,
        'nikkei_name':nikkei_name,
        'nikkei_price':nikkei_price,
        'nikkei_perc':nikkei_perc,
        'nikkei_dollar':nikkei_dollar,
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
        'econ_name':econ_name,
        'econ_url':econ_url,
        'econ_image':econ_image,
        'econ_description':econ_description,
        'econ_source':econ_source,
        'sp500_name':sp500_name,
        'sp500_url': sp500_url,
        'sp500_image':sp500_image,
        'sp500_description':sp500_description,
        'sp500_source':sp500_source,
        'oil_name':oil_name,
        'oil_url':oil_url,
        'oil_image':oil_image,
        'oil_description':oil_description,
        'oil_source':oil_source,
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
        'tech1_name':tech1_name,
        'tech1_url':tech1_url,
        'tech1_source':tech1_source,
        'tech1_image':tech1_image,
        'tech1_des':tech1_des,
        'tech2_name':tech2_name,
        'tech2_url':tech2_url,
        'tech2_source':tech2_source,
        'tech2_image':tech2_image,
        'tech2_des':tech2_des,
        'tech3_name':tech3_name,
        'tech3_url':tech3_url,
        'tech3_source':tech3_source,
        'tech3_image':tech3_image,
        'tech3_des':tech3_des,
        'tech3_content':tech3_content,
        'tech4_name':tech4_name,
        'tech4_url':tech4_url,
        'tech4_source':tech4_source,
        'tech4_image':tech4_image,
        'tech4_des':tech4_des,
        'tech4_content':tech4_content,
        'tech5_name':tech5_name,
        'tech5_url':tech5_url,
        'tech5_source':tech5_source,
        'tech5_image':tech5_image,
        'tech5_des':tech5_des,
        'health_name':health_name,
        'health_url':health_url,
        'health_source':health_source,
        'health_image':health_image,
        'health_des':health_des,
        'health1_name':health1_name,
        'health1_url':health1_url,
        'health1_source':health1_source,
        'health1_image':health1_image,
        'health1_des':health1_des,
        'health2_name':health2_name,
        'health2_url':health2_url,
        'health2_source':health2_source,
        'health2_image':health2_image,
        'health2_des':health2_des,
        'health2_content':health2_content,
        'health3_name':health3_name,
        'health3_url':health3_url,
        'health3_source':health3_source,
        'health3_image':health3_image,
        'health3_des':health3_des,
        'health3_content':health3_content,
    }

    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')
