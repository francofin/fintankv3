from django.shortcuts import render

# Create your views here.
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
    
    return render(request, 'screener/screener.html')
