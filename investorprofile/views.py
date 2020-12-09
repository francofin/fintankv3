from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Portfolio_2
from .forms import PortfolioForm
from django import template

register = template.Library()
# Create your views here.
def register_user(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        password_min = 6

        if len(password) < password_min:
            messages.error(request, 'Your Password is Too Short, Please choose a password at least 6 characters long!')
            return redirect('register_user')
        else:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username Already Exists')
                    return redirect('register_user')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email Already Exists!')
                        return redirect('register_user')
                    else:
                        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password)
                        auth.login(request, user)
                        messages.success(request, 'you are now logged in')
                        return redirect('dashboard')
                        user.save()
                        messages.succes(request, 'Account Successfully Created. Welcome')
                        return redirect('index')
            else:
                messages.error(request, 'Passwords Do Not Match!')
                return redirect('register_user')
    else:
        return render(request, 'pages/register.html')
#
# @login_required(login_url='login')
# def add_to_portfolio(request):
#     if request.method == 'POST':
#         user_id = request.POST['user_id']
#         ticker = request.POST['ticker']
#
#         portfolio = Portfolio(user_id = user_id, ticker=ticker)
#         portfolio.save()
#         messages.success(request, str(ticker)+' Has been Successfully Added to Your Portfolio')
#         return redirect('/research/')


@login_required(login_url='login')
def add_to_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST or None, request.user)
        if form.is_valid():
            ticker = form.save(commit=False)
            ticker.user = request.user
            ticker.save()
            return redirect('/research/')

@login_required(login_url='login')
def delete_stock(request, stock_id):
    item = Portfolio_2.objects.all().filter(user=request.user).filter(pk=stock_id)
    item.delete()
    return redirect('/investorprofile/dashboard')


def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You Are Successfully Logged In! Welcome')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid LogIn Credentials')
            return redirect('login')
    return render(request, 'pages/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('login')
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    import pandas as pd
    import numpy as np
    from scipy.optimize import minimize
    from scipy import stats
    from scipy.stats import norm
    import requests
    import json

    def make_portfolio_df(portfolio, tickers):
        data_df =  pd.DataFrame(data = portfolio[0])[['date','adjClose']].rename(columns={'adjClose':tickers[0]}).set_index('date')
        i = 1
        while i < len(portfolio):
            data = pd.DataFrame(portfolio[i])[['date','adjClose']].set_index('date')
            data_df[tickers[i]] = data['adjClose']
            i +=1
            return data_df

    def get_prices(data):
        i = 0
        output = []
        while i < len(data):
            batch = json.loads(requests.get(f' https://fmpcloud.io/api/v3/historical-price-full/'+data[i]+'?from=2018-03-12&to=2019-03-12&apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
            output.append(batch['historical'])
            i+=1
        return output

    def price_normalization(dataframe):
        norm_price = (dataframe / dataframe.shift(1)) -1
        return norm_price.dropna()

    def log_return(dataframe):
        log_r = np.log(dataframe/dataframe.shift(1))
        return log_r

    def cor_table(dataframe):
        ret_table = log_return(dataframe)

        return ret_table.corr()

    def cov_table(dataframe):
        ret_table = log_return(dataframe)
        return ret_table.cov()

    def monte_carlo_sim(r_table_mean, r_cov, a_list, num_trials=5000):
        all_weights = np.zeros((num_trials, len(a_list)))
        ret_arr = np.zeros(num_trials)
        vol_arr = np.zeros(num_trials)
        sharpe_arr = np.zeros(num_trials)

        for trial in range(num_trials):
            weights = np.array(np.random.random(len(a_list)))
            weights = weights / np.sum(weights)
            all_weights[trial, :] = weights
            ret_arr[trial] = np.sum((r_table_mean * weights) *252)
            vol_arr[trial] = np.sqrt(np.dot(weights.T, np.dot(r_cov, weights)))
            sharpe_arr[trial] = ret_arr[trial] / vol_arr[trial]

        max_sharpe = sharpe_arr.max()
        max_sr_ret = ret_arr[sharpe_arr.argmax()]
        best_vol = vol_arr[sharpe_arr.argmax()]
        best_weights = np.round(all_weights[sharpe_arr.argmax(),:], 4)

        return ret_arr, vol_arr, sharpe_arr, format(max_sharpe, ".2f"), str(format(max_sr_ret *100, ".2f")) +"%", str(format(best_vol*100, ".2f")) +"%", best_weights

    def get_ret_vol_sr(w_array):
        weight = np.array(w_array)
        ret = np.sum(annualized_returns * weight)
        vol = np.sqrt(np.dot(weight.T, np.dot(cov_df, weight)))
        sr = ret / vol
        return ret, vol, sr

    def minimize_function(w_array, a_list, r_table_mean, r_cov):

        def neg_sharpe(w):
            return  get_ret_vol_sr(w)[2] * -1

        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = ((0, 1),) * len(a_list)
        init_guess = w_array
        opt_results = minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bound, constraints=cons)
        ret = get_ret_vol_sr(opt_results.x)[0]*100
        vol = get_ret_vol_sr(opt_results.x)[1]*100
        sr = get_ret_vol_sr(opt_results.x)[2]
        return str(format(ret, ".2f")) +"%", str(format(vol, ".2f")) +"%", str(format(sr, ".2f"))+"%", opt_results.x

    # user_stocks = Portfolio_2.objects.all().filter(user_id=request.user.id)
    user_stocks = Portfolio_2.objects.all().filter(user=request.user)
    user_portfolio = []
    #for the price data
    # data_list = []
    for stock in user_stocks:
        user_portfolio.append(str(stock))

    batch = json.loads(requests.get(f' https://fmpcloud.io/api/v3/quote/'+','.join(user_portfolio)+'?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)

    prices = get_prices(user_portfolio)
    if len(user_portfolio) != 0:
        prices_df = make_portfolio_df(prices, user_portfolio)
        log_returns = log_return(prices_df)
        mean_returns = log_returns.mean()
        annualized_returns = mean_returns* 252
        cov_df = cov_table(prices_df) * 252
        return_array, volatility_array, sharpe_array, max_sharpe_ratio, max_sharpe_return, best_volatility, port_weights = monte_carlo_sim(mean_returns, cov_df, user_portfolio)
        stocks = {
            'user_stocks': user_stocks,
            'user_portfolio':user_portfolio,
            'batch':batch,
            'return_array': return_array,
            'volatility_array':volatility_array,
            'sharpe_array':sharpe_array,
            'max_sharpe_ratio':max_sharpe_ratio,
            'port_weights':port_weights
                }
        # weight_array = port_weights
        # minimized_ret, minimized_vol, minimized_sr, optimum_weights = minimize_function(sum_to_one_weights, user_portfolio, annualized_returns, cov_df)
    else:
        stocks = {
        'user_stocks': user_stocks,
        'user_portfolio':user_portfolio,
        'batch':batch,
            }
    return render(request, 'pages/dashboard.html', stocks)
