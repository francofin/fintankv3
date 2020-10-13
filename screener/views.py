from django.shortcuts import render

# Create your views here.

def screen(request):
    return render(request, 'screener/screener.html')


def screener(request):
    import pandas as pd
    import numpy as np
    from bokeh.plotting import figure
    from bokeh.io import output_file, show
    from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.models import ColumnDataSource
    from bokeh.resources import CDN
    import matplotlib.pyplot as plt
    from datetime import datetime
    from bokeh.models import HoverTool
    import requests
    import json

    if request.method == 'POST':
        sector_raw = request.POST['option']
        sector = str(sector_raw)
        size_raw = request.POST['option2']
        size = str(size_raw)
        if sector and size:
            sector_size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector='+sector+'&marketCapMoreThan='+size+'&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
            screen_df_raw = pd.DataFrame(sector_size_screen).set_index('symbol')
            screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
        elif sector:
            sector_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?sector='+sector+'&limit=100&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
            screen_df_raw = pd.DataFrame(sector_screen).set_index('symbol')
            screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
        elif size:
            if size == "200000000000":
                size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
                screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
                screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
            elif size == "10000000000":
                size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=180000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
                screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
                screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
            elif size == "2000000000":
                size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=10000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
                screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
                screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
            elif size == "300000000":
                size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=2000000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
                screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
                screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()
            elif size == "50000000":
                size_screen = json.loads(requests.get(f'https://fmpcloud.io/api/v3/stock-screener?marketCapMoreThan='+size+'&marketCapLowerThan=300000000&limit=4000&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
                screen_df_raw = pd.DataFrame(size_screen).set_index('symbol')
                screen_df = screen_df_raw.style.set_table_attributes("class='table table-sm table-striped table-bordered table-hover'").render()

        context = {
        'screen_df': screen_df,
        }

        return render(request, 'screener/screener.html', context)
