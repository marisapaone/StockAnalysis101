# -*- coding: utf-8 -*-
"""
@author: Marisa Paone
Class: CS677

this scripts reads your ticker file (e.g. PG.csv and SPY.csv) and
constructs a list of lines
"""
import os

# Importing and reading two .csv files
ticker='PG'
here = os.path.abspath(__file__)
input_dir = os.path.abspath(os.path.join(here, os.pardir))
ticker_file = os.path.join(input_dir, ticker + '.csv')

ticker2='SPY'
here2 = os.path.abspath(__file__)
input_dir2 = os.path.abspath(os.path.join(here, os.pardir))
ticker_file2 = os.path.join(input_dir2, ticker2 + '.csv')

try:
    # Opening the files and reading each line into a list of lines
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)

    print("------------Question 1------------")
    print()
    print("Table data for ticker:", ticker)
    print()

    # Getting a list of the names of the columns for viewing purposes
    cols = lines[0].split(",")

    # For the list of lines, I am seperating all elements and appending them to a new list called rows. I am doing this for every line (list item)
    rows = []
    for e in lines:
        rows.append(e.split(","))

    # Creating lists of all of the years I want to calculate data on, and the days of the week.

    years = ['2016', '2017', '2018', '2019', '2020']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # For each of the 5 years compute the mean and standard deviation for all returns, all pos returns and all neg returns

    # sets of R, Rneg and Rpos

    def R_set(year, day):
        R = []
        # For every element in rows, (every line), if the year and day matches, append it to the R list.
        for i in range (1, len(rows)):
            if rows[i][1] == year:
                if rows[i][4] == day:
                    R.append(rows[i][13])
        return R

    def Rneg_set(year, day):
        Rneg = []
        # For every element in rows, (every line), if the year and day matches, append it to the Rneg list if its a negative number.
        for i in range (1, len(rows)):
            if rows[i][1] == year:
                if rows[i][4] == day:
                    if float(rows[i][13]) < 0.0:
                        Rneg.append(rows[i][13])
        return Rneg

    def Rpos_set(year, day):
        Rpos = []
        # For every element in rows, (every line), if the year and day matches, append it to the Rpos list if its a positive number.
        for i in range(1, len(rows)):
            if rows[i][1] == year:
                if rows[i][4] == day:
                    if float(rows[i][13]) >= 0.0:
                        Rpos.append(rows[i][13])
        return Rpos

    # Counts the number of values in the Rneg list, and for each year and day of the week, it will print the values out.
    def count_Rneg():
        print("Printing |R-|")
        for i in years:
            print()
            print("R- set")
            for j in days:
                count = len(Rneg_set(i, j))
                print(j, "count: ", count," in", i)


    # Counts the number of values in the Rpos list, and for each year and day of the week, it will print the values out.
    def count_Rpos():
        print()
        print("Printing |R+|")
        for i in years:
            print()
            print("R+ set")
            for j in days:
                count = len(Rpos_set(i, j))
                print(j, "count: ", count," in", i)


    # Printing the |R-| and |R+| values
    count_Rneg()
    count_Rpos()

    # ----------- Calculation functions -----------------
    # Calculating the mean of a particular set (list of floats)
    def calc_mean(set):
        count = 0
        total = 0.0
        for i in range(len(set)):
            total = total + float(set[i])
            count = count + 1
        mean = total/count
        return mean

    # Calculating the standard deviation of a particular set (list of floats)
    def calc_stand_dev(set):
        mean = calc_mean(set)
        count = 0
        total = 0.0
        # For the entire length of the set
        for i in range(len(set)):
            total = total + (float(set[i]))**2
            count = count + 1
        sd = ((total / count) - (mean**2))**0.5
        return sd

    # Printing the data to copy into excel

    # Printing the mean for the R set
    def print_mean_data_R():
        print()
        print("Printing Mean Data For the R set")
        for i in years:
            print()
            print("R set")
            for j in days:
                mean = calc_mean(R_set(i, j))
                print(j,"'s in", i, "mean μ(R): ", mean)

    # Printing the mean for the R- set
    def print_mean_data_Rneg():
        print()
        print("Printing Mean Data For the R- set")
        for i in years:
            print()
            print("R- set")
            for j in days:
                mean = calc_mean(Rneg_set(i, j))
                print(j,"'s in", i, "mean μ(R-): ", mean)

    # Printing the mean for the R+ set
    def print_mean_data_Rpos():
        print()
        print("Printing Mean Data For the R+ set")
        for i in years:
            print()
            print("R+ set")
            for j in days:
                mean = calc_mean(Rpos_set(i, j))
                print(j,"'s in", i, "mean μ(R+): ", mean)

    # Prints the standard deviation for the R set
    def print_sd_data_R():
        print()
        print("Printing Standard Deviation Data For the R set")
        for i in years:
            print()
            print("R set")
            for j in days:
                sd = calc_stand_dev(R_set(i, j))
                print(j,"'s in", i, "Standard Deviation σ(R): ", sd)

    # Prints the standard deviation for the R- set
    def print_sd_data_Rneg():
        print()
        print("Printing Standard Deviation Data For the R- set")
        for i in years:
            print()
            print("R- set")
            for j in days:
                sd = calc_stand_dev(Rneg_set(i, j))
                print(j,"'s in", i, "Standard Deviation σ(R-): ", sd)

    # Prints the standard deviation for the R+ set
    def print_sd_data_Rpos():
        print()
        print("Printing Standard Deviation Data For the R+ set")
        for i in years:
            print()
            print("R+ set")
            for j in days:
                sd = calc_stand_dev(Rpos_set(i, j))
                print(j,"'s in", i, "Standard Deviation σ(R+): ", sd)

    # Calculates the mean for all of the years
    def mean_all_years():
        count = 0
        total = 0.0
        for i in range(1, len(rows)):
            num = float(rows[i][13])
            count = count + 1
            total = total + num
        print("Average of all years daily returns: ")
        print(total / count)

    # Printing mean data
    print_mean_data_R()
    print_mean_data_Rneg()
    print_mean_data_Rpos()

    # Printing Standard Deviation Data
    print_sd_data_R()
    print_sd_data_Rneg()
    print_sd_data_Rpos()

    # Printing the mean for all the years
    print()
    mean_all_years()

    # ----------Question 3 Aggregate Table for 5 years---------------

    print()
    print("------------Question 3------------")
    print()

    # Opening the second ticker S&P (SPY)

    with open(ticker_file2) as g:
        lines2 = g.read().splitlines()
    print('opened file for ticker: ', ticker2)
    print()

    # Creating a new list of rows for the S&P (SPY)
    rows2 = []
    for e in lines2:
        rows2.append(e.split(","))

    # Forms the R set for all 5 years
    def R_set_5_years(day, ticker_rows):
        R = []
        for i in range (1, len(ticker_rows)):
            if ticker_rows[i][4] == day:
                R.append(ticker_rows[i][13])
        return R

    # Forms the R- set for all 5 years
    def Rneg_set_5_years(day,ticker_rows):
        Rneg = []
        for i in range (1, len(ticker_rows)):
            if ticker_rows[i][4] == day:
                if float(ticker_rows[i][13]) < 0.0:
                    Rneg.append(ticker_rows[i][13])
        return Rneg

    # Forms the R+ set for all 5 years
    def Rpos_set_5_years(day,ticker_rows):
        Rpos = []
        for i in range(1, len(ticker_rows)):
            if ticker_rows[i][4] == day:
                if float(ticker_rows[i][13]) >= 0.0:
                    Rpos.append(ticker_rows[i][13])
        return Rpos

    # Counts the R- set for all 5 years
    def count_Rneg_5_years(ticker_rows):
        print("Printing |R-|")
        for j in days:
            count = len(Rneg_set_5_years(j, ticker_rows))
            print(j, "count: ", count)

    # Counts the R+ set for all 5 years
    def count_Rpos_5_years(ticker_rows):
        print("Printing |R+|")
        for j in days:
            count = len(Rpos_set_5_years(j, ticker_rows))
            print(j, "count: ", count)


    # Printing the |R-| and |R+| values for SPY and PG
    print("Ticker:", ticker)
    count_Rneg_5_years(rows) #PG
    count_Rpos_5_years(rows) #PG
    print()

    print("Ticker:", ticker2)
    count_Rneg_5_years(rows2) #SPY
    count_Rpos_5_years(rows2) #SPY
    print()

    # Prints the mean data for the R set over 5 years
    def print_mean_data_R_5years(ticker_type):
        print()
        print("Printing Mean Data For the R set")
        for j in days:
            mean = calc_mean(R_set_5_years(j, ticker_type))
            print(j, "'s mean μ(R): ", mean)

    # Prints the mean data for the R- set over 5 years
    def print_mean_data_Rneg_5years(ticker_type):
        print()
        print("Printing Mean Data For the R- set")
        for j in days:
            mean = calc_mean(Rneg_set_5_years(j, ticker_type))
            print(j,"'s mean μ(R-): ", mean)

    # Prints the mean data for the R+ set over 5 years
    def print_mean_data_Rpos_5years(ticker_type):
        print()
        print("Printing Mean Data For the R+ set")
        for j in days:
            mean = calc_mean(Rpos_set_5_years(j, ticker_type))
            print(j, "'s mean μ(R+): ", mean)

    # Prints the standard deviation data for the R set over 5 years
    def print_sd_data_R_5years(ticker_type):
        print()
        print("Printing Standard Deviation Data For the R set")
        for j in days:
            sd = calc_stand_dev(R_set_5_years(j,ticker_type))
            print(j, "'s standard deviation σ(R): ", sd)

    # Prints the standard deviation data for the R- set over 5 years
    def print_sd_data_Rneg_5years(ticker_type):
        print()
        print("Printing Standard Deviation Data For the R- set")
        for j in days:
            sd = calc_stand_dev(Rneg_set_5_years(j,ticker_type))
            print(j, "'s standard deviation σ(R-): ", sd)

    # Prints the standard deviation data for the R+ set over 5 years
    def print_sd_data_Rpos_5years(ticker_type):
        print()
        print("Printing Standard Deviation Data For the R+ set")
        for j in days:
            sd = calc_stand_dev(Rpos_set_5_years(j,ticker_type))
            print(j, "'s standard deviation σ(R+): ", sd)

    #Printing data for 'PG' ticker
    print("Aggregate Table Data for ", ticker)

    # Printing the mean and standard deviation data values for all 5 years for PG
    print_mean_data_R_5years(rows) #PG
    print_mean_data_Rneg_5years(rows) #PG
    print_mean_data_Rpos_5years(rows) #PG

    print_sd_data_R_5years(rows) #PG
    print_sd_data_Rneg_5years(rows) #PG
    print_sd_data_Rpos_5years(rows) #PG
    print()

    #Running the same methods for 'SPY' ticker
    print("Aggregate Table Data for ", ticker2)

    # Printing the mean and standard deviation data values for all 5 years for SPY
    print_mean_data_R_5years(rows2) #SPY
    print_mean_data_Rneg_5years(rows2) #SPY
    print_mean_data_Rpos_5years(rows2) #SPY

    print_sd_data_R_5years(rows2) #SPY
    print_sd_data_Rneg_5years(rows2) #SPY
    print_sd_data_Rpos_5years(rows2) #SPY

    #-------------Question 4-------------

    print()
    print("------------Question 4------------")
    print()

    # Creates an oracle that knows each positive return day for a ticker.
    def oracle_prediction(money_total, ticker_rows):
        oracle = []
        for i in range(1, len(ticker_rows)):
            oracle.append(float(ticker_rows[i][13]))
        # For the positive values in the oracle it will tell you to sell.
        for i in oracle:
            if i>0: #if the rate of return is positive, we want to sell
                money_total = (money_total*i)+money_total #so we sell and then add that money to our pot
        return round(money_total, 2)

    print("Using an oracle that only trades on positive days...")
    print("The oracle made you $", oracle_prediction(100, rows), "with ticker:", ticker) #PG
    print("The oracle made you $", oracle_prediction(100, rows2), "with ticker:", ticker2) #SPY

    #------------Question 5-------------

    print()
    print("------------Question 5------------")
    print()

    # The Buy and Hold strategy function
    def buy_and_hold(money_total, ticker_rows):
        buyhold = []
        # For every day, you will be holding.
        for i in range(1, len(ticker_rows)):
            buyhold.append(float(ticker_rows[i][13]))
        for i in buyhold:
            money_total = (money_total*i)+money_total
        return round(money_total, 2)
    print("Buying and holding only...")
    print("Buying and holding you now have $", buy_and_hold(100, rows), "with ticker:", ticker)
    print("Buying and holding you now have $", buy_and_hold(100, rows2), "with ticker:", ticker2)


    #--------Question 6 -----------
    # Part A

    # Oracle removes the best 10 returns
    def oracle_best_ten(money_total, ticker_rows):
        oracle = []
        for i in range(1, len(ticker_rows)):
            oracle.append(float(ticker_rows[i][13]))
        print("Removing the 10 best returns from the oracle...")
        print()
        # Looping through 10 times, and removing the maximum value from oracle 10 times.
        for i in range(1,11):
            best_value = max(oracle)
            print(best_value)
            oracle.remove(best_value)
        for i in oracle:
            if i > 0: # If the rate of return is positive, we want to sell
                money_total = (money_total*i)+money_total # So we sell and then add that money to our pot
        return round(money_total, 2)

    print()
    print("------------Question 6, part a------------")
    print()
    print("Ticker:", ticker)
    print("The oracle made you $", oracle_best_ten(100, rows), "with ticker:", ticker)
    print()
    print("Ticker:", ticker2)
    print("The oracle made you $", oracle_best_ten(100, rows2), "with ticker:", ticker2)

    # Question 6 Part B
    # Oracle adds in the 10 worst return days
    def oracle_worst_ten(money_total, ticker_rows):
        oracle_dummy = [] # oracle_dummy is used to remove the worst values and add to oracle_lying list
        oracle = [] # oracle is used as the full list of daily returns
        oracle_lying = [] # The values to include in the oracle that its lying about
        for i in range(1, len(ticker_rows)):
            oracle_dummy.append(float(ticker_rows[i][13]))
            oracle.append(float(ticker_rows[i][13]))
        print("Adding the 10 worst returns to the oracle...")
        print()

        #looping through 10 times, and adding the minimum values to oracle_lying list 10 times.
        for i in range(1, 11):
            worst_value = min(oracle_dummy)
            print(worst_value)
            oracle_dummy.remove(worst_value) # Removing the worst value from oracle_dummy so we get new minimums (this happens 10 times)
            oracle_lying.append(worst_value) # adds the worst values from oracle to oracle_lying

        # for every daily return in oracle (contains worst values)
        for i in oracle:
            if i > 0: # If the rate of return is positive, we want to sell
                money_total = (money_total*i)+money_total # So we sell and then add that money to our pot
            elif i in oracle_lying: # If i is found in the oracle_lying list (the oracle will lie about it so we include it in the money_total)
                money_total = (money_total * i) + money_total
                oracle_lying.remove(i)

        return round(money_total, 2)

    print()
    print("------------Question 6, part b------------")
    print()
    print("Ticker:", ticker)
    print("The oracle made you $", oracle_worst_ten(100, rows), "with ticker:", ticker)
    print()
    print("Ticker:", ticker2)
    print("The oracle made you $", oracle_worst_ten(100, rows2), "with ticker:", ticker2)



    # Question 6 Part C

    # Oracle adds in the 5 worst return days and removes the best 5 days
    def oracle_best_five_worst_five(money_total, ticker_rows):
        oracle_dummy = []
        oracle = []
        oracle_lying = []
        for i in range(1, len(ticker_rows)):
            oracle_dummy.append(float(ticker_rows[i][13]))
            oracle.append(float(ticker_rows[i][13]))
        print("Adding the 5 worst return days to the oracle, and removing the best 5 return days")
        print()

        # looping through 5 times, and adding the minimum values to oracle_lying.
        print("Min 5:")
        for i in range(1, 6):
            worst_value = min(oracle_dummy)
            print(worst_value)
            # We must remove the worst value from the dummy oracle list so that it can tell us other minimum values for the next iteration of this loop
            oracle_dummy.remove(worst_value)
            # Add the worst values to oracle_lying
            oracle_lying.append(worst_value)

        # looping through 5 times, and removing the maximum values to the oracle.
        print("Max 5:")
        for i in range(1,6):
            best_value = max(oracle)
            print(best_value)
            # removing the best value of the oracle list
            oracle.remove(best_value)

        for i in oracle:
            if i > 0: # if the rate of return is positive, we want to sell
                money_total = (money_total*i)+money_total # so we sell and then add that money to our pot
            elif i in oracle_lying: # accounting for the 5 worst values that we wanted to add to the oracle
                money_total = (money_total * i) + money_total
                oracle_lying.remove(i) # removing i from the oracle_lying list in case there are two values of the same amount (we don't want to double count them)

        return round(money_total, 2)

    print()
    print("------------Question 6, part c------------")
    print()
    print("Ticker:", ticker)
    print("The oracle made you $", oracle_best_five_worst_five(100, rows), "with ticker:", ticker)
    print()
    print("Ticker:", ticker2)
    print("The oracle made you $", oracle_best_five_worst_five(100, rows2), "with ticker:", ticker2)

except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)
















