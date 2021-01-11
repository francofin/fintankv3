# import pandas as pd
# import json
# import requests
#
# api = '3da6aaea4ffa4232c7ada6b09e15af62'
# sp500 = json.loads(requests.get(f'https://fmpcloud.io/api/v3/sp500_constituent?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content)
# s_p_tickers = []
# sp_index = 0
# while sp_index < len(sp500):
#     symbol = sp500[sp_index]['symbol']
#     s_p_tickers.append(symbol)
#     sp_index+=1
# s_p_tickers.pop(418)
# s_p_tickers.pop(437)
# s_p_tickers.pop(447)
#
#
# def get_ratios(ticker_list):
#     ratio_df =  pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/ratios-ttm/'+ticker_list[0]+'?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content))
#     ratio_df['symbol'] = ticker_list[0]
#     ratio_df = ratio_df.set_index('symbol')
#     i = 1
#     while i < 200:
#         df = pd.DataFrame(json.loads(requests.get(f'https://fmpcloud.io/api/v3/ratios-ttm/'+ticker_list[i]+'?apikey=3da6aaea4ffa4232c7ada6b09e15af62').content))
#         df['symbol'] = ticker_list[i]
#         df = df.set_index('symbol')
#         ratio_df = pd.concat([ratio_df, df])
#         i+=1
#
#     return ratio_df
#
#
# all_ratios = get_ratios(s_p_tickers)
# ranked_ratios = all_ratios[['dividendYielPercentageTTM', 'peRatioTTM', 'pegRatioTTM', 'currentRatioTTM', 'cashRatioTTM','daysOfInventoryOutstandingTTM', 'daysOfPayablesOutstandingTTM', 'grossProfitMarginTTM', 'operatingProfitMarginTTM','netProfitMarginTTM', 'returnOnEquityTTM', 'returnOnCapitalEmployedTTM', 'ebitPerRevenueTTM', 'debtRatioTTM', 'debtEquityRatioTTM', 'totalDebtToCapitalizationTTM', 'interestCoverageTTM', 'cashFlowToDebtRatioTTM', 'inventoryTurnoverTTM', 'operatingCashFlowPerShareTTM', 'operatingCashFlowSalesRatioTTM', 'cashFlowCoverageRatiosTTM', 'shortTermCoverageRatiosTTM', 'priceToBookRatioTTM', 'priceToSalesRatioTTM','priceEarningsRatioTTM', 'priceToFreeCashFlowsRatioTTM', 'priceCashFlowRatioTTM', 'dividendYieldTTM', 'enterpriseValueMultipleTTM']]
