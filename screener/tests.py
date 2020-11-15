# from django.shortcuts import render
#
# # Create your views here.
#
# def screen(request):
#     return render(request, 'screener/screener.html')
#
#
# def screener(request):
#     import pandas as pd
#     import numpy as np
#     from bokeh.plotting import figure
#     from bokeh.io import output_file, show
#     from bokeh.models.annotations import Title
#     from bokeh.embed import components
#     from bokeh.resources import CDN
#     from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, PrintfTickFormatter
#     from bokeh.models import ColumnDataSource
#     from bokeh.palettes import Viridis
#     from bokeh.palettes import Spectral6
#     from bokeh.transform import factor_cmap
#     from bokeh.palettes import Category20c
#     from math import pi
#     from bokeh.transform import cumsum
#     from datetime import datetime
#     from bokeh.models import HoverTool
#     from numpy.core._multiarray_umath import ndarray
#     from pandas_datareader import data
#     from scipy.optimize import minimize
#     import statsmodels.api as sm
#     from requests_html import HTMLSession
#     from datetime import date
#     import requests
#     import asyncio
#     from scipy import stats
#     import json
#     import random
#     from random import randrange
#     date_format="%Y-%m-%d"
#     end_date = str(date.today())
#     api = '3da6aaea4ffa4232c7ada6b09e15af62'
#
#     if request.method == 'POST':
#         sector_raw = request.POST['option']
#         sector = str(sector_raw)
#         size_raw = request.POST['option2']
#         size = str(size_raw)
#         if ((sector!='') and (size!='')):
#             sector_size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector='+sector+'&marketCapMoreThan='+size+'&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#             screen_df_raw = pd.DataFrame(sector_size_screen).set_index('symbol')
#             screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#             length = len(screen_df)
#         elif sector and size == '':
#             sector_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector='+sector+'&limit=100&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#             screen_df_raw = pd.DataFrame(sector_screen).set_index('symbol')
#             screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#             length = len(screen_df)
#         elif size and sector == '':
#             if size == "200000000000":
#                 size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan=180000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#                 screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
#                 screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#                 length = len(screen_df)
#             elif size == "10000000000":
#                 size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=180000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#                 screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
#                 screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#                 length = len(screen_df)
#             elif size == "2000000000":
#                 size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=10000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#                 screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
#                 screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#                 length = len(screen_df)
#             elif size == "300000000":
#                 size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=2000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#                 screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
#                 screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#                 length = len(screen_df)
#             elif size == "50000000":
#                 size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=300000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
#                 screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
#                 screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
#                 length = len(screen_df)
#
#         # sector performances
#         re = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLRE?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Real Estate'})
#         tech = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLK?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Tech'})
#         utilities = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLU?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Utilities'})
#         materials = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLB?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Materials'})
#         industrials = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLI?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Industrials'})
#         health = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLV?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Health Care'})
#         financials = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLF?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Financials'})
#         energy = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLV?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Energy'})
#         staples = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLP?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Cons Staples'})
#         disc = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLY?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Cons Disc'})
#         comm = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/XLC?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'Communications'})
#         sp500 = (pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/historical-price-full/^GSPC?from=2020-01-01&to='+end_date+'&apikey='+api).content)['historical']).set_index('date').iloc[::-1])[['changePercent']].rename(columns={'changePercent':'S&P500'})
#
#         total_sector = re.join([tech, utilities, industrials, health, financials, energy, staples, disc, comm])
#         total_sector_market = total_sector.join(sp500)
#
#         sdf5 = (total_sector_market/100+1).cumprod()*100*100
#         sdf7 = total_sector/100
#
#         colour = [ "#DA1717", "#7217DA", "#1799DA", "#17DA72", "#EFEF0B", "#3D7073", "#2C06C1", "black", "#C106B5", "#06C119", "#C14B06", "#22A884", "#A8A822"]
#         rand_colours = [random.choice(colour) for i in range(15)]
#         output = list(sdf5.columns)
#         sdf5['dates'] = pd.to_datetime(sdf5.index)
#
#         f = figure(x_axis_type='datetime', width=1300, height=500, title = "YTD Growth of $10,000", toolbar_location=None, tools="hover", tooltips="@y")
#         for (col, rand_col, leg) in zip(sdf5, colour, output):
#             plot = f.line(sdf5['dates'], sdf5[col], color = rand_col, legend_label=leg, line_width=2)
#         f.xaxis.axis_label = "Date"
#         f.yaxis.axis_label = "Growth"
#         f.legend.location="top_left"
#         f.legend.click_policy="hide"
#
#
#         script6, div6 = components(f)
#         cdn_js = CDN.js_files
#         cdn_css = CDN.css_files
#
#         context = {
#         'screen_df': screen_df,
#         'sector': sector,
#         'length': length,
#         'script6':script6,
#         'div6':div6,
#         }
#
#         return render(request, 'screener/screener.html', context)
# from django.test import TestCase
#
# # Create your tests here.
