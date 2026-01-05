""""""  		  	   		 	   			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	   			  		 			     			  	 
All Rights Reserved  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	   			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	   			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	   			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   			  		 			     			  	 
or edited.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	   			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	   			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   			  		 			     			  	 
GT honor code violation.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		 	   			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		 	   			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		 	   			  		 			     			  	 
"""  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import datetime as dt  		  	   		 	   			  		 			     			  	 
import os  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import numpy as np  		  	   		 	   			  		 			     			  	 
import matplotlib.pyplot as plt
import pandas as pd  		  	   		 	   			  		 			     			  	 
from util import get_data, plot_data
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
def compute_portvals(  		  	   		 	   			  		 			     			  	 
    orders_file="orders.csv",
    start_val=1000000,  		  	   		 	   			  		 			     			  	 
    commission=9.95,  		  	   		 	   			  		 			     			  	 
    impact=0.005,  		  	   		 	   			  		 			     			  	 
):  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    Computes the portfolio values.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		 	   			  		 			     			  	 
    :type orders_file: str or file object  		  	   		 	   			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		 	   			  		 			     			  	 
    :type start_val: int  		  	   		 	   			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	   			  		 			     			  	 
    :type commission: float  		  	   		 	   			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	   			  		 			     			  	 
    :type impact: float  		  	   		 	   			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	   			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		 	   			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		 	   			  		 			     			  	 
    # code should work correctly with either input  		  	   		 	   			  		 			     			  	 
    # TODO: Your code here
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    orders = pd.read_csv(orders_file)

    syms = orders["Symbol"].unique()
    prices_all = get_data(syms,pd.date_range(start_date, end_date))
    prices_all.index.name = "Date"
    # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
    prices.loc[:,"cash"] = 1

    trades_temp = orders.copy(deep=True)
    trades_temp['Mod. Shares'] = trades_temp.apply(lambda row: row['Shares'] if row['Order'] == 'BUY' else -row['Shares'], axis=1)
    trades_temp = trades_temp.set_index('Date')

    print(prices)
    print(trades_temp)

    # Create a copy of dataframe1
    new_dataframe = prices.copy()

    # Merge the dataframes on appropriate columns
    merged_df = new_dataframe.merge(trades_temp, left_index=True, right_index=True, how='left')

    # Set all values to zero except for modified shares
    for symbol in syms:
        merged_df[symbol] = np.where(merged_df['Symbol'] == symbol, merged_df['Mod. Shares'], 0)

    # Calculate the cash column
    for symbol in syms:
        merged_df['cash'] += np.where(merged_df['Symbol'] == symbol, -1 * merged_df['Mod. Shares'] * prices[symbol], 0)

    # Set other cash values to zero
    merged_df['cash'] *= np.where(merged_df['Symbol'].isna(), 0, 1).round().astype(int)

    # Drop unnecessary columns
    merged_df.drop(['Symbol', 'Order', 'Shares', 'Mod. Shares'], axis=1, inplace=True)

    # Group by date and sum up the values
    trades = merged_df.groupby(merged_df.index).sum()


    """result_df = prices_all.merge(trades_temp, how='left')

    # Set the index back to the original index from dataframe1
    result_df.set_index('index', inplace=True)

    # Fill NaN values with zeros
    result_df.fillna(0, inplace=True)"""

    # The final merged dataframe
    print(trades)

    """result_df = prices_all.merge(trades_temp, left_index=True, right_on='Date', how='left').fillna(0)
    print(result_df)
    print(result_df.size)

    result_df.reset_index(drop=True, inplace=True)
    holdings = result_df.groupby(['Date', 'Symbol']).sum().drop('Shares', axis=1).pivot_table(index='Date', columns='Symbol', values='Mod. Shares', aggfunc='sum').fillna(0).drop(0, axis=1)"""

    holdings = trades.copy()
    # Add each value to the previous one
    for col in holdings.columns:
        holdings[col] = holdings[col].cumsum()

    holdings['cash'] = start_val + holdings.sum(axis=1)



    # Display the resulting holdings DataFrame
    print(holdings)

    
    values_df = prices_all * holdings

    portvals = (values_df.sum(axis=1))


    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months  		  	   		 	   			  		 			     			  	 

    """portvals = get_data(["IBM"], pd.date_range(start_date, end_date))  		  	   		 	   			  		 			     			  	 
    portvals = portvals[["IBM"]]  # remove SPY  """
    rv = pd.DataFrame(index=portvals.index, data=portvals.values)  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    return rv  		  	   		 	   			  		 			     			  	 
    return portvals  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
def test_code():  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    Helper function to test code  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		 	   			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		 	   			  		 			     			  	 
    # Define input parameters  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    of = "additional_orders/orders2.csv"
    sv = 1000000  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    # Process orders  		  	   		 	   			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)  		  	   		 	   			  		 			     			  	 
    if isinstance(portvals, pd.DataFrame):  		  	   		 	   			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:  		  	   		 	   			  		 			     			  	 
        "warning, code did not return a DataFrame"  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    # Get portfolio stats  		  	   		 	   			  		 			     			  	 
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		 	   			  		 			     			  	 
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    daily_ret = (portvals/portvals.shift(1)) - 1
    daily_ret = daily_ret.tail(daily_ret.shape[0] - 1)
    cum_ret = (portvals[-1]/portvals[0]) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    drfr = (1 ** (1 / 252)) - 1
    sharpe_ratio = (avg_daily_ret - drfr) / std_daily_ret

    #plot
    # Plot the daily returns
"""    df = portvals.to_frame(name = "portfolio")
    df.index.rename("Date", inplace=True)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df, marker='o', linestyle='-', color='b')
    plt.title('Portfolio Daily Returns')
    plt.xlabel('Date')
    plt.ylabel('Daily Return')
    plt.grid(True)
    plt.show()"""

    #for my reference. Delete later
    SPX = pd.read_csv("../data/$SPX.csv",
            index_col="Date",
            parse_dates=True,
            usecols=["Date", 'Adj Close'])

    cum_ret_SPX = (SPX['Adj Close'][-1]/SPX['Adj Close'][0]) - 1
    daily_ret_SPX = (SPX/SPX.shift(1)) - 1
    daily_ret_SPX = daily_ret_SPX.tail(daily_ret_SPX.shape[0] - 1)
    avg_daily_ret_SPX = daily_ret_SPX.mean()
    std_daily_ret_SPX = daily_ret_SPX.std()
    sharpe_ratio_SPX = (avg_daily_ret_SPX - drfr) / std_daily_ret_SPX
  		  	   		 	   			  		 			     			  	 
    # Compare portfolio against $SPX  		  	   		 	   			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		 	   			  		 			     			  	 
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		 	   			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPX}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		 	   			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPX}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		 	   			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPX}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		 	   			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPX}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
if __name__ == "__main__":  		  	   		 	   			  		 			     			  	 
    test_code()  		  	   		 	   			  		 			     			  	 
