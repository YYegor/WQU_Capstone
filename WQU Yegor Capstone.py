# WQU Capstone project
# Yegor Yeremenko
# 2017, April

import pandas as pd
import datetime as dt
from pandas_datareader import data, wb
import csv

# set False for more output
SILENT = True

# source files
source_file_data = 'WQU Yegor Capstone source data.xlsx'

# stock data
source_file_stocks = 'WQU Yegor Capstone source data Stocks.xlsx'

# output for results
output_file_csv = 'WQU Yegor results.csv'


def get_source_data(tab_name_country, ticker, year):
    '''
    The function loads source financial data from formed excel.
    :param tab_name_country: Excel with source data has tabs named by country name
    :param ticker:
    :param year: year of financials
    :return:
    '''
    try:
        xl = pd.ExcelFile(source_file_data)
    except:
        print 'Error: Can\'t read \'' + str(source_file_data) + '\''
        return None

    try:
        df = xl.parse(tab_name_country)
    except:
        print 'Error: Can\'t find tab', tab_name_country
        return None

    try:
        # list_values = df.loc[(df['year'] == year) & (df['ticker'] == ticker)].values.tolist()[0]
        df_out = df.loc[(df['year'] == year) & (df['ticker'] == ticker)]
    except:
        print 'Error: Can\'t access data for', ticker, 'and', year
        return None

    return df_out


def calc_f_score(net_income, extraord_items, cfo, net_income_prev,
                 extraord_items_prev, long_term_debt,
                 long_term_debt_prev,
                 total_assets,
                 total_liab,
                 total_assets_prev, total_liab_prev,
                 total_revenue, cost_revenue,
                 total_revenue_prev, cost_revenue_prev,
                 eq_offer=False):
    '''
    Calculates Piotroski's f-score

    :param net_income: 2
    :param extraord_items: 3
    :param cfo: 4
    :param net_income_prev:
    :param extraord_items_prev:
    :param long_term_debt:
    :param long_term_debt_prev:
    :param total_assets:
    :param total_liab:
    :param total_assets_prev:
    :param total_liab_prev:
    :param total_revenue:
    :param cost_revenue:
    :param total_revenue_prev:
    :param cost_revenue_prev:
    :param eq_offer: True False for additional offerings
    :return: f-SCORE
    '''

    # counter of undefined f-score component
    undefined_values = 0

    try:
        f_roa = 1 if (float(net_income) - float(extraord_items)) > 0 else 0
        if not SILENT: print 'ROA', f_roa
    except:
        undefined_values += 1
        f_roa = 0
        if not SILENT: print 'ROA undefined'

    try:
        f_d_roa = 1 if float(net_income) - float(extraord_items) > float(net_income_prev) - float(
            extraord_items_prev) else 0
        if not SILENT: print 'dROA', f_d_roa
    except:
        if not SILENT: print 'dROA undefined'
        undefined_values += 1
        f_d_roa = 0

    try:
        f_cfo = 1 if float(cfo) > 0 else 0
        if not SILENT: print 'CFO', f_cfo
    except:
        if not SILENT: print 'CFO undefined'
        f_cfo = 0
        undefined_values += 1

    try:
        f_accrual = 1 if float(cfo) > (float(net_income) - float(extraord_items)) else 0
        if not SILENT: print 'ACCRUAL', f_accrual

    except:
        if not SILENT: print 'ACCRUAL undefined'
        f_accrual = 0
        undefined_values += 1

    try:

        f_d_lever = 1 if ((float(long_term_debt) / float(total_assets)) - (
        float(long_term_debt_prev) / float(total_assets_prev))) < 0 else  0
        if not SILENT: print 'LEVER', f_d_lever

    except:
        # div by 0
        f_d_lever = 0
        undefined_values += 1
        if not SILENT: print 'LEVER undefined'

    try:
        f_d_liquid = 1 if ((float(total_assets) / float(total_liab)) - (
        float(total_assets_prev) / float(total_liab_prev))) > 0 else 0
        if not SILENT: print 'dLIQUID', f_d_liquid
    except:
        # div by 0
        f_d_liquid = 0
        undefined_values += 1
        if not SILENT: print 'dLIQUID undefined'

    try:
        f_eq_offer = 1 if int(eq_offer) == 0 else 0
        if not SILENT: print 'EQ_OFFER', f_eq_offer

    except:
        if not SILENT: print 'EQ_OFFER undefined'
        undefined_values += 1
        f_eq_offer = 0

    try:
        f_d_margin = 1 if (((float(cost_revenue)) / float(total_revenue)) - (
            (float(cost_revenue_prev)) / float(total_revenue_prev))) > 0 else 0
        if not SILENT: print 'dMARGIN', f_d_margin

    except:
        f_d_margin = 0
        undefined_values += 1
        if not SILENT: print 'dMARGIN undefined'

    try:
        f_d_turn = 1 if ((float(total_revenue) / float(total_assets)) - (
        float(total_revenue_prev) / float(total_assets_prev))) > 0 else 0
        if not SILENT: print 'dTURNOVER', f_d_turn
    except:
        f_d_turn = 0
        undefined_values += 1
        if not SILENT: print 'dTURNOVER undefined'

    if undefined_values > 0:
        if not SILENT: print 'Undefined variables ', undefined_values, 'of 9'
    else:
        if not SILENT: print 'No Undefined variables'

    # combine f-score
    f_score = f_roa + f_cfo + f_d_roa + f_accrual + f_d_lever + \
              f_d_liquid + f_eq_offer + f_d_margin + f_d_turn

    if undefined_values == 9:
        return None

    # print 'F-Score', f_score

    return f_score


def make_portfolio(stocks, number_of_stocks):
    # TODO
    pass


def load_list_stocks(tab_name_country):
    '''
    Loads data from predefined excel file
    :param tab_name_country:
    :return: stocks for the tested country
    '''
    try:
        xl = pd.ExcelFile(source_file_stocks)
    except:
        print 'Error: Can\'t read \'' + str(source_file_stocks) + '\''
        return None, None

    try:
        df = xl.parse(tab_name_country)
    except:
        print 'Can\'t find tab', tab_name_country

    try:
        stocks = df['stocks'].values.tolist()
        currency = df['currency'].values.tolist()[0]
    except:
        print 'Error with stock column'
        return None, None

    return stocks, currency


# def get_currency_name(country):
#     if country == 'Russia':
#         return 'RUB'
#     else:
#         return None

def get_price_special(ticker, year):
    '''
    loads price for 1st May of the year (or closest day)
    :param ticker:
    :param year:
    :return:
    '''


    startdate = dt.datetime(year, 5, 1)
    enddate = dt.datetime(year, 5, 1)

    try:
        price = data.DataReader(ticker, 'yahoo', startdate, enddate)['Adj Close']

    except:
        if not SILENT: print 'Unable to access data for ' + ticker
        return None

    try:
        p = float(price)
    except:
        p = None
    return p


######################START HERE######################
#define years for test
year_list = [2016, 2015, 2014, 2013, 2012, 2011]

# define countries to test
countries_list = ['Russia', 'India', 'Brazil', 'China', 'UK', 'Germany', 'France']

# year_list = [2014 ]
# countries_list = ['Russia']

#resulting set
results = []

#counter of tests
counter = 0

# iterate all countries
for test_country in countries_list:

    #iterate all years
    for test_year in year_list:

        print 'Country:', test_country, '\nYear:', test_year
        stocks_l, cur = load_list_stocks(test_country)

        if stocks_l is None or cur is None:
            print 'Error: no stock list for', test_country
            continue

        print 'Stock list:', stocks_l
        print 'Stock currency:', cur

        # iterate all stocks
        for tick in stocks_l:

            # calc all test
            counter += 1

            # load financials for ticker for test year and for prevoius
            y_1 = get_source_data(test_country, tick, test_year)
            y_0 = get_source_data(test_country, tick, test_year - 1)

            # calc F-Score
            f_score = calc_f_score(
                y_1['net_income'], \
                y_1['extraord_items'], \
                y_1['cfo'], \
                y_0['net_income'], \
                y_0['extraord_items'], \
                y_1['long_term_debt'], \
                y_0['long_term_debt'], \
                y_1['total_assets'], \
                y_1['total_liab'], \
                y_0['total_assets'], \
                y_0['total_liab'], \
                y_1['total_revenue'], \
                y_1['cost_revenue'], \
                y_0['total_revenue'], \
                y_0['cost_revenue'], \
                y_1['eq_offer'])

            # print tick+':', f_score
            if f_score is None:
                print '\nUndefined score for', tick, 'skip'
                continue

            # stock price for the testing year = test_year
            p_1 = get_price_special(tick, test_year)

            # stock price for the previous year = test_year -1
            p_0 = get_price_special(tick, test_year - 1)

            if p_0 is None:
                print '\nNo prices for', tick, test_year - 1, 'skip'
                continue

            if p_1 is None:
                print '\nNo prices for', tick, test_year, 'skip'
                continue

            confirmed_test = ''

            # high f-score case
            if f_score >= 7:

                if p_1 > p_0:
                    confirmed_test = 'Confirmed'

                else:
                    confirmed_test = 'NOT confirmed'

            # low f-score case
            if f_score < 7:

                if p_1 < p_0:
                    confirmed_test = 'Confirmed'
                else:
                    confirmed_test = 'NOT confirmed'

            # calc pnl based on stock prices
            pnl = (p_1 - p_0) / p_0

            print '\n', tick, 'from', p_0, 'to', p_1, str(
                round(pnl * 100.0, 2)) + '%', 'F-Score', f_score, '[', confirmed_test, ']'

            # append the results to the list
            results.append([test_country, tick, test_year, f_score, p_0, p_1, pnl, confirmed_test])


print counter, 'test(s) done'


# print results, save to csv
# accessing the output file
try:
    myfile = open(output_file_csv, 'wb')

except:
    print 'Error: Can\'t open output file', output_file_csv
    print results
    print 'Exiting'
    exit(1)

wr = csv.writer(myfile, delimiter=';')
#write column names
wr.writerow(['test_country', 'ticker', 'test_year', 'f_score', 'price_prev', 'price_cur', 'pnl', 'confirmed_test'])

# write data into file
for res_line in results:
    wr.writerow(res_line)
myfile.close()

# output test results
print len(results), ' result(s) are saved in \'', output_file_csv, '\''
######################ENDS HERE######################