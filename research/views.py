from django.shortcuts import render
import html5lib
from research.market_indices import all_ratios
from yahoo_fin.stock_info import *
from yahoo_fin.options import *

# Create your views here.
def research(request):
    import pandas as pd
    import numpy as np
    from bokeh.plotting import figure
    from bokeh.io import output_file, show
    from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, PrintfTickFormatter
    from bokeh.models import ColumnDataSource
    from bokeh.palettes import Viridis
    from bokeh.palettes import Spectral6
    from bokeh.transform import factor_cmap
    from bokeh.palettes import Category20c
    from math import pi
    from bokeh.transform import cumsum
    from datetime import datetime
    from bokeh.models import HoverTool
    from numpy.core._multiarray_umath import ndarray
    from pandas_datareader import data
    from scipy.optimize import minimize
    import statsmodels.api as sm
    from requests_html import HTMLSession
    from datetime import date
    import requests
    import asyncio
    from scipy import stats
    import json
    import random
    from random import randrange

    session = HTMLSession()
    api = '3da6aaea4ffa4232c7ada6b09e15af62'
    date_format="%Y-%m-%d"
    subscription_key = "904298336d514d45babbf4e9aaf29fff"

    def get_fmp_news(search_term):
        search_url = f"https://fmpcloud.io/api/v3/stock_news?tickers="+search_term+"&limit=100&apikey=3da6aaea4ffa4232c7ada6b09e15af62"
        response = json.loads(requests.get(search_url).content)

        return response

    def get_news(search_term, subscription_key):
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = json.loads(response.content)
        top_item = search_results['value']

        return top_item

    def get_images(search_term, subscription_key):
        search_url1 = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url1, headers=headers, params=params)
        search_results1 = json.loads(response.content)

        top_item1 = search_results1['value']

        return top_item1

    nasdaq = json.loads(requests.get(f'https://fmpcloud.io/api/v3/symbol/available-nasdaq?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
    tsx = json.loads(requests.get(f'https://fmpcloud.io/api/v3/symbol/available-tsx?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
    euro = json.loads(requests.get(f'https://fmpcloud.io/api/v3/symbol/available-euronext?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
    sp500 = json.loads(requests.get(f'https://fmpcloud.io/api/v3/sp500_constituent?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)

    ratios_for_analysis = all_ratios

    # get random ticker function
    def get_ticker(exchange):
        ticker_list = []
        for i in exchange:
            ticker_list.append(i)
        choice = random.choice(ticker_list)

        return choice
    # select random ticker
    random_equity = random.choice([get_ticker(nasdaq), get_ticker(tsx), get_ticker(euro)])
    ticker_request = random_equity['symbol']
    try:
        ticker_currency = random_equity['currency']
    except:
        ticker_currency = 'USD'
    ticker_name = random_equity['name']
    try:
        ticker_exchange = random_equity['exchangeShortName']
    except:
        ticker_exchange = ''
    today = date.today()
    # d1 end date for chart
    end_date = str(date.today())
    # start date for chart
    start_for_chart = date(today.year-1,1,2)
    d2 = start_for_chart.strftime("%Y-%m-%d")
    date_2 = str(d2)
    symbol_chart = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/'+str(ticker_request)+'?from='+date_2+'&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])
    # Table information
    # json_results = []
    # raw_data = json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/'+str(ticker_request)+'?from='+date_2+'&to='+end_date+'&apikey='+api).content)['historical']
    # for item in raw_data:
    #     json_results.append(item)
    # json_data = json_results[0:10]
    dataframe = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/'+str(ticker_request)+'?from='+date_2+'&to='+end_date+'&apikey='+api).content)['historical']).set_index('date'))[[ 'close', 'volume', 'change', 'changePercent']].head(10)
    dataframe_clean = dataframe.rename(columns={'close':'Close', 'volume':'Volume', 'change':'$Change', 'changePercent':'Daily Change %'})
    ticker_info = dataframe_clean.sort_values(by=['date'], ascending=False).style.format('{:,.2f}').set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
    ytd_eqn = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/'+str(ticker_request)+'?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])
    symbol_chart['dates'] = pd.to_datetime(symbol_chart.index, format=date_format)
    ytd_formula = (ytd_eqn['adjClose'][-1]/ytd_eqn['adjClose'].iloc[0] - 1)*100
    ytd = format(ytd_formula, '.2f')+"%"
    # line chart
    TOOLTIPS = [("Price", "@y{$0.2f}")]
    p = figure(x_axis_type="datetime", plot_width=1000, plot_height = 500, title = str(ticker_request))
    p.line(x = symbol_chart['dates'], y = symbol_chart['adjClose'], line_color='#126AB6', line_width=3)
    p.legend.location = 'top_right'
    p.add_tools(HoverTool(tooltips=TOOLTIPS,mode='mouse'))
    script1, div1 = components(p)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    # stock profile

    stock_profile = json.loads(requests.get(f'https://fmpcloud.io/api/v3/profile/'+str(ticker_request)+'?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
    profile = stock_profile[0]['description']
    sector = stock_profile[0]['sector']
    if sector == None:
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"
        querystring = {"region":"US","symbol":"GAZP.ME"}
        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "feec356023msh7d505f582747ea5p199c91jsnd5a1909fc40a"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        sector = json.loads(response.content)['assetProfile']['sector']
    else:
        sector = sector

    image = stock_profile[0]['image']
    try:
        beta = format(stock_profile[0]['beta'], ".2f")
    except:
        print('nan')
    try:
        price = get_live_price(ticker_request)
        live_price = format(price, '.2f')
    except:
        price = ''
        live_price = ''


    # Sector ranks
    sector_data = pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector='+sector+'&limit=200&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content))
    stock_beta = json.loads(requests.get(f'https://fmpcloud.io/api/v3/quote/'+str(ticker_request)+'?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
    sector_data['Index'] = sector_data.index
    stock_beta_data = stock_profile[0]['beta']
    stock_div = stock_profile[0]['lastDiv']
    stock_mcap = stock_beta[0]['marketCap']
    stock_price = stock_beta[0]['price']
    test_data = pd.DataFrame({'symbol':stock_beta[0]['symbol'],'marketCap':stock_mcap, 'price':stock_price, 'beta':stock_beta_data, 'lastAnnualDividend':stock_div, 'Index':len(sector_data)}, index =[len(sector_data)] )
    sector_data = sector_data.append(test_data)

    def apply_rank(dataset, stock,item):
        data = dataset
        mean = dataset[item].mean()
        i = 0
        while i < len(data[item]):
            if data['symbol'][i] == stock:
                data.loc[i, item+' Rank'] = stock
            elif data[item][i] > mean:
                data.loc[i, item+' Rank'] = 'Above Average'
            else:
                data.loc[i, item+' Rank'] = 'Below Average'
            i+=1
        return data

    rank_data = apply_rank(sector_data, str(ticker_request), 'beta')
    rank_data = apply_rank(sector_data, str(ticker_request), 'price')
    rank_data = apply_rank(sector_data, str(ticker_request), 'lastAnnualDividend')
    rank_data = apply_rank(sector_data, str(ticker_request), 'marketCap')

    final_rank_data = rank_data.drop([rank_data.nlargest(5, 'price').index[0], rank_data.nlargest(5, 'price').index[1], rank_data.nlargest(5, 'price').index[2], rank_data.nlargest(5, 'price').index[3], rank_data.nlargest(5, 'price').index[4], rank_data.nlargest(2, 'lastAnnualDividend').index[0], rank_data.nlargest(2, 'lastAnnualDividend').index[1]])
    mcap_data = rank_data.drop(list(rank_data[rank_data['marketCap']==0].index), axis=0)
    mcap_data = mcap_data.drop([mcap_data.nlargest(2, 'price').index[0], mcap_data.nlargest(2, 'price').index[1]])

    x = [str(ticker_request), 'Above Average', 'Below Average']

    # Beta Rank
    q = figure(plot_width=600, plot_height=450, title = str(ticker_request)+" Beta Rank",toolbar_location=None, tools="hover", tooltips="@symbol: @beta")
    q.scatter('Index','beta',source=final_rank_data, legend_field = 'beta Rank', fill_alpha=0.6, size=10, color=factor_cmap('beta Rank', 'Category10_3', x))
    q.xaxis.axis_label = 'Universe'
    q.yaxis.axis_label = 'Rank'
    q.legend.location = "top_left"

    script2, div2 = components(q)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files


    # Price Rank
    z = figure(plot_width=600, plot_height=450, title = str(ticker_request)+" Price Rank",toolbar_location=None, tools="hover", tooltips="@symbol: @price")
    z.scatter('Index','price',source=final_rank_data,legend_field = 'price Rank', fill_alpha=0.6, size=10, color=factor_cmap('price Rank', 'Category10_3', x))
    z.xaxis.axis_label = 'Universe'
    z.yaxis.axis_label = 'Rank'
    z.legend.location = "top_left"

    script3, div3 = components(z)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    # Dividend Rank
    y = figure(plot_width=600, plot_height=450, title = str(ticker_request)+" Dividend Rank",toolbar_location=None, tools="hover", tooltips="@symbol: @lastAnnualDividend")
    y.scatter('Index','lastAnnualDividend',source=final_rank_data,legend_field = 'lastAnnualDividend Rank', fill_alpha=0.6, size=10, color=factor_cmap('lastAnnualDividend Rank', 'Category10_3', x))
    y.xaxis.axis_label = 'Universe'
    y.yaxis.axis_label = 'Rank'
    y.legend.location = "top_left"

    script4, div4 = components(y)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    # Market Cap Rank
    wy = figure(plot_width=600, plot_height=450, title = str(ticker_request)+" Cap Rank",toolbar_location=None, tools="hover", tooltips="@symbol: @marketCap")
    wy.scatter('Index','marketCap',source=mcap_data,legend_field = 'marketCap Rank', fill_alpha=0.6, size=10, color=factor_cmap('marketCap Rank', 'Category10_3', x))
    wy.xaxis.axis_label = 'Universe'
    wy.yaxis.axis_label = 'Rank'
    wy.legend.location = "top_left"

    script5, div5 = components(wy)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    # sector performances
    re = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLRE?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Real Estate'})
    tech = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLK?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Tech'})
    utilities = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLU?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Utilities'})
    materials = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLB?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Materials'})
    industrials = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLI?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Industrials'})
    health = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLV?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Health Care'})
    financials = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLF?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Financials'})
    energy = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLV?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Energy'})
    staples = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLP?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Cons Staples'})
    disc = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLY?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Cons Disc'})
    comm = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLC?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Communications'})
    sp500 = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/^GSPC?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'S&P500'})

    total_sector = re.join([tech, utilities, industrials, health, financials, energy, staples, disc, comm])
    total_sector_market = total_sector.join(sp500)

    sdf5 = (total_sector_market/100+1).cumprod()*100*100
    sdf7 = total_sector/100

    colour = [ "#DA1717", "#7217DA", "#1799DA", "#17DA72", "#EFEF0B", "#3D7073", "#2C06C1", "black", "#C106B5", "#06C119", "#C14B06", "#22A884", "#A8A822"]
    rand_colours = [random.choice(colour) for i in range(15)]
    output = list(sdf5.columns)
    sdf5['dates'] = pd.to_datetime(sdf5.index)

    f = figure(x_axis_type='datetime', width=1200, height=500, title = "YTD Growth of $10,000", toolbar_location=None, tools="hover", tooltips="@y")
    for (col, rand_col, leg) in zip(sdf5, colour, output):
        plot = f.line(sdf5['dates'], sdf5[col], color = rand_col, legend_label=leg, line_width=2)
    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Growth"
    f.legend.location="top_left"
    f.legend.click_policy="hide"


    script6, div6 = components(f)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    if '-' in ticker_request:
        index = ticker_request.find('-')
        ticker_search = ticker_request[0:index]
    else:
        ticker_search = ticker_request

    exchange_list = ['NASDAQ', 'NYSE']
    if ticker_exchange in exchange_list:
        news = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock_news?tickers='+ticker_search+'&limit=100&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
        images = get_images('stock market', subscription_key)
        if len(news) > 10:
            article1 = news[0]['text'][0:200]
            article1_site = news[0]['site']
            article1_url = news[0]['url']
            article1_image = images[0]['thumbnailUrl']
            article2 = news[1]['text'][0:200]
            article2_site = news[1]['site']
            article2_url = news[1]['url']
            article2_image = images[1]['thumbnailUrl']
            article3 = news[2]['text'][0:200]
            article3_site = news[2]['site']
            article3_url = news[2]['url']
            article3_image = images[2]['thumbnailUrl']
            article4 = news[3]['text'][0:200]
            article4_site = news[3]['site']
            article4_url = news[3]['url']
            article4_image = images[3]['thumbnailUrl']
            article5 = news[4]['text'][0:200]
            article5_site = news[4]['site']
            article5_url = news[4]['url']
            article5_image = images[4]['thumbnailUrl']
            article6 = news[5]['text'][0:200]
            article6_site = news[5]['site']
            article6_url = news[5]['url']
            article6_image = images[5]['thumbnailUrl']
            article7 = news[6]['text'][0:200]
            article7_site = news[6]['site']
            article7_url = news[6]['url']
            article7_image = images[6]['thumbnailUrl']
            article8 = news[7]['text'][0:200]
            article8_site = news[7]['site']
            article8_url = news[7]['url']
            article8_image = images[7]['thumbnailUrl']
            article9 = news[8]['text'][0:200]
            article9_site = news[8]['site']
            article9_url = news[8]['url']
            article9_image = images[8]['thumbnailUrl']
        else:
            news=json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock_news?limit=50&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
            article1 = news[0]['title']
            article1_site = news[0]['site']
            article1_url = news[0]['url']
            article1_image = news[0]['image']
            article2 = news[1]['title']
            article2_site = news[1]['site']
            article2_url = news[1]['url']
            article2_image = news[1]['image']
            article3 = news[2]['title']
            article3_site = news[2]['site']
            article3_url = news[2]['url']
            article3_image = news[2]['image']
            article4 = news[3]['title']
            article4_site = news[3]['site']
            article4_url = news[3]['url']
            article4_image = news[3]['image']
            article5 = news[4]['title']
            article5_site = news[4]['site']
            article5_url = news[4]['url']
            article5_image = news[4]['image']
            article6 = news[5]['title']
            article6_site = news[5]['site']
            article6_url = news[5]['url']
            article6_image = news[5]['image']
            article7 = news[6]['title']
            article7_site = news[6]['site']
            article7_url = news[6]['url']
            article7_image = news[6]['image']
            article8 = news[7]['title']
            article8_site = news[7]['site']
            article8_url = news[7]['url']
            article8_image = news[7]['image']
            article9 = news[8]['title']
            article9_site = news[8]['site']
            article9_url = news[8]['url']
            article9_image = news[8]['image']
    else:
        news=json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock_news?limit=50&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
        article1 = news[0]['title']
        article1_site = news[0]['site']
        article1_url = news[0]['url']
        article1_image = news[0]['image']
        article2 = news[1]['title']
        article2_site = news[1]['site']
        article2_url = news[1]['url']
        article2_image = news[1]['image']
        article3 = news[2]['title']
        article3_site = news[2]['site']
        article3_url = news[2]['url']
        article3_image = news[2]['image']
        article4 = news[3]['title']
        article4_site = news[3]['site']
        article4_url = news[3]['url']
        article4_image = news[3]['image']
        article5 = news[4]['title']
        article5_site = news[4]['site']
        article5_url = news[4]['url']
        article5_image = news[4]['image']
        article6 = news[5]['title']
        article6_site = news[5]['site']
        article6_url = news[5]['url']
        article6_image = news[5]['image']
        article7 = news[6]['title']
        article7_site = news[6]['site']
        article7_url = news[6]['url']
        article7_image = news[6]['image']
        article8 = news[7]['title']
        article8_site = news[7]['site']
        article8_url = news[7]['url']
        article8_image = news[7]['image']
        article9 = news[8]['title']
        article9_site = news[8]['site']
        article9_url = news[8]['url']
        article9_image = news[8]['image']


    # ratings

    def get_ratings(stock):
        grades = json.loads(requests.get(f'https://fmpcloud.io/api/v3/grade/'+stock+'?limit=500&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
        grade_df = pd.DataFrame(grades)
        outperform = 0
        buy = 0
        strong_buy = 0
        neutral = 0
        underperform = 0
        sell = 0
        positive = 0
        negative = 0
        other = 0
        i = 0
        while i < len(grade_df['newGrade']):
            if grade_df['newGrade'][i] == 'Outperform':
                outperform+=1
            elif grade_df['newGrade'][i] == 'Buy':
                buy+=1
            elif grade_df['newGrade'][i] == 'Strong Buy':
                buy+=1
            elif grade_df['newGrade'][i] == 'Neutral':
                neutral+=1
            elif grade_df['newGrade'][i] == 'Underperform':
                underperform+=1
            elif grade_df['newGrade'][i] == 'Sell':
                sell+=1
            elif grade_df['newGrade'][i] == 'Positive':
                positive+=1
            elif grade_df['newGrade'][i] == 'Negative':
                positive+=1
            else:
                other+=1
            i+=1
        grade_list = [outperform, buy, strong_buy, positive, neutral, underperform, sell, negative, other]
        ratings = ['Outperform', 'Buy', 'Strong Buy', 'Positive', 'Neutral', 'Underperform', 'Sell', 'Negative', 'Other']
        return grade_list, ratings

    # recommendations
    def analyst_recommendations(stock):
        recommendations = json.loads(requests.get(f'https://fmpcloud.io/api/v3/analyst-stock-recommendations/'+stock+'?limit=60&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
        rec_df = pd.DataFrame(recommendations).set_index('date').drop('symbol', axis=1).iloc[::-1]

        return rec_df

    message0 = 'Ratings Not Available for Stock'
    message1 = 'Other Includes Ratings such os overweight, underweight, sector weight, reduce, perform and market outperform.'
    try:
        stock_grades = get_ratings(ticker_request)
        grades = stock_grades[0]
        analyst_ratings = stock_grades[1]

        data = {
            'ratings':analyst_ratings,
            'grade':grades
            }
        rating_chart = figure(x_range=analyst_ratings, plot_height=250, title="Stock Grade",
                   toolbar_location=None, tools="hover", tooltips="@ratings: @grade")
        rating_chart.vbar(x='ratings', top='grade', source=data, width=0.9)
        rating_chart.y_range.start = 0
        script7, div7 = components(rating_chart)
        message = message1
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files
    except:
        grades = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        analyst_ratings = ['Outperform', 'Buy', 'Strong Buy', 'Positive', 'Neutral', 'Underperform', 'Sell', 'Negative', 'Other']
        data = {
            'ratings':analyst_ratings,
            'grade':grades
            }
        rating_chart = figure(x_range=analyst_ratings, plot_height=250, title="Stock Grade",
                   toolbar_location=None, tools="hover", tooltips="@ratings: @grade")
        rating_chart.vbar(x='ratings', top='grade', source=data, width=0.9)
        rating_chart.y_range.start = 0
        message = message0
        script7, div7 = components(rating_chart)
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files



    data = {
        'script1':script1,
        'div1':div1,
        'profile':profile,
        'sector':sector,
        'beta':beta,
        'ticker_name':ticker_name,
        'ticker_currency':ticker_currency,
        'ticker_request':ticker_request,
        'live_price':live_price,
        'ticker_exchange':ticker_exchange,
        'script2':script2,
        'div2':div2,
        'script3':script3,
        'div3':div3,
        'script4':script4,
        'div4':div4,
        'script5':script5,
        'div5':div5,
        'script6':script6,
        'div6':div6,
        'script7':script7,
        'div7':div7,
        'message':message,
        'ticker_info':ticker_info,
        'image':image,
        'ytd':ytd,
        'article1':article1,
        'article1_site':article1_site,
        'article1_url':article1_url,
        'article1_image':article1_image,
        'article2':article2,
        'article2_site':article2_site,
        'article2_url':article2_url,
        'article2_image':article2_image,
        'article3':article3,
        'article3_site':article3_site,
        'article3_url':article3_url,
        'article3_image':article3_image,
        'article4':article4,
        'article4_site':article4_site,
        'article4_url':article4_url,
        'article4_image':article4_image,
        'article5':article5,
        'article5_site':article5_site,
        'article5_url':article5_url,
        'article5_image':article5_image,
        'article6':article6,
        'article6_site':article6_site,
        'article6_url':article6_url,
        'article6_image':article6_image,
        'article7':article7,
        'article7_site':article7_site,
        'article7_url':article7_url,
        'article7_image':article7_image,
        'article8':article8,
        'article8_site':article8_site,
        'article8_url':article8_url,
        'article8_image':article8_image,
        'article9':article9,
        'article9_site':article9_site,
        'article9_url':article9_url,
        'article9_image':article9_image,
    }

    return render(request, 'research/research.html', data)
