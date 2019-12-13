#This is the main python file that gets the scraped data from the data sources and adds them to Database.
#The data from database is to plot graph.
#The plotted graph shows the trend in the data breaches in the previous and current years. The trend shows
#with more people having data online, the data breaches are more and the number of exposed data is more
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#importing argparse for command line parameters. Importing the classes from python files that scrape data.
#Importing sqlite for adding DB. Importing matplotlib to plot bar graph
import argparse
from pwned_breach_list import pwned_breach
from statista_data_breach import statista_data_class
from twitter_word_search import tweet_word_search
import sqlite3
import matplotlib.pyplot as plt

#global variable to be used across functions
stored_data = tuple()

#function to run when the -source runs on remote
def grab_data_by_scraping_and_api_requests():
    #creating DB connection with data_breach.db
    conn = sqlite3.connect('../data/data_breach.db')
    cur = conn.cursor()

    #setting variables from the returned values from classes from python files
    pwned_data = pwned_breach().get_pwned_breach_info()
    twitter_data = tweet_word_search().twitter_search()
    statista_exposed_data = statista_data_class().get_statista_exposed_data()
    statista_year = statista_data_class().get_statista_year()
    
    #creating DB and inserting to store exposed data numbers from Have I Been Pwned website
    cur.execute('DROP TABLE IF EXISTS DataBreaches')
    cur.execute('CREATE TABLE DataBreaches (BREACH_ID INTEGER PRIMARY KEY AUTOINCREMENT, BREACH_EXPOSED_DATA REAL)')  
    for pwned_data_item in pwned_data:
        cur.execute('INSERT INTO DataBreaches (BREACH_EXPOSED_DATA) VALUES (?)', (pwned_data_item,))
    
    #creating DB and inserting to store exposed data numbers and year from Statista website
    cur.execute('DROP TABLE IF EXISTS OldDataBreaches')
    cur.execute('CREATE TABLE OldDataBreaches (OLD_BREACH_ID INTEGER PRIMARY KEY AUTOINCREMENT, OLD_BREACH_EXPOSED_DATA REAL, OLD_BREACH_EXPOSED_YEAR INTEGER)')
    cur.executemany('INSERT INTO OldDataBreaches (OLD_BREACH_EXPOSED_DATA, OLD_BREACH_EXPOSED_YEAR) VALUES (?,?)', zip(statista_exposed_data, statista_year))
     
    #creating DB and inserting to store exposed data numbers and URLS from Twitter
    cur.execute('DROP TABLE IF EXISTS TwitterDataBreaches')
    cur.execute('CREATE TABLE TwitterDataBreaches (TWITTER_BREACH_ID INTEGER PRIMARY KEY AUTOINCREMENT, TWITTER_BREACH_EXPOSED_DATA REAL, TWITTER_BREACH_URL TEXT)')
    
    for twitter_data_item in twitter_data:
        
        #checking if the URL from list exists in the DB
        cur.execute('SELECT * FROM TwitterDataBreaches WHERE (TWITTER_BREACH_URL=?)', (twitter_data_item[1],))
        url_entry = cur.fetchone()
        
        #if URL is unique
        if url_entry is None:
            #checking if the exposed data number exists in DB
            cur.execute('SELECT * FROM TwitterDataBreaches WHERE (TWITTER_BREACH_EXPOSED_DATA=?)', (twitter_data_item[0],))
            count_entry = cur.fetchone()
            
            #if exposed data number is unique insert values in DB
            if count_entry is None:
                cur.execute('INSERT INTO TwitterDataBreaches (TWITTER_BREACH_EXPOSED_DATA,TWITTER_BREACH_URL) VALUES (?,?)', (twitter_data_item[0],twitter_data_item[1],))
            else:
                continue
        else:
            continue
        
    #commit the changes to DB     
    conn.commit()

    #close DB connection
    conn.close()

    
#function to extract data from DB
def grab_data_from_downloaded_raw_files():
    #creating DB connection with data_breach.db
    conn = sqlite3.connect('../data/data_breach.db')
    cur = conn.cursor()

    #getting sum of all the exposed data from Have I Been Pwned DB and converting it to millions
    cur.execute('SELECT sum(BREACH_EXPOSED_DATA) as sum FROM DataBreaches')
    exposed_data_sum = cur.fetchall()
    exposed_data_sum_in_million = exposed_data_sum[0][0]/(10**6)
    
    #getting sum of all the exposed data which is in millions from Twitter DB
    cur.execute('SELECT sum(TWITTER_BREACH_EXPOSED_DATA) as sum FROM TwitterDataBreaches')
    exposed_twitter_data_sum = cur.fetchall()
    
    #Adding the sums from Have I Been Pwned DB and Twitter DB
    current_year_breach = exposed_data_sum_in_million + (exposed_twitter_data_sum[0][0])
    
    #fetching the values of exposed data from Statista and appending items to a list.
    #adding the previous sum to this list
    cur.execute("SELECT OLD_BREACH_EXPOSED_DATA FROM OldDataBreaches")
    old_breach_result_set = cur.fetchall()
    old_breach_list = []
    for item in old_breach_result_set:
        old_breach_list.append(item[0])
    old_breach_list.append(current_year_breach)
     
    #fetching the values of exposed data years from Statista and appending items to a list.
    #adding the year 2019 to this list
    cur.execute("SELECT OLD_BREACH_EXPOSED_YEAR FROM OldDataBreaches")
    old_year_result_set = cur.fetchall()
    old_year_list = []
    for item in old_year_result_set:
        old_year_list.append(item[0])
    old_year_list.append(2019)
    
    #close the DB connection
    conn.close()

    #returning tuple of list
    return old_year_list, old_breach_list
    
#function to take returned value from previous function to plot graph
def plot_graph(storage_data):

    old_year_list = storage_data[0]
    old_breach_list = storage_data[1]
    #Setting the size of the graph plot
    plt.figure(figsize=(10,10))
    
    #setting x and y axis of the graph
    x = old_year_list
    y = old_breach_list
    
    #setting the label of coordinates of the x axis
    tick_label = old_year_list
    
    #plotting the bar graph and setting the bar design
    plt.bar(x, y, tick_label = tick_label, width = 0.8, color = ['red', 'green'])
    
    #setting the labels for x and y axis. Storing the plotted graph as an image
    plt.xlabel('Year')
    plt.ylabel('Data Breaches')

    #show the plotted graph
    plt.show()

#function to decide whether the code should run on remote or local   
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", choices=["local", "remote"], nargs=1, help="where data should be gotten from")
    args = parser.parse_args()
    
    location = args.source

    if location == ['local']:
        stored_data = grab_data_from_downloaded_raw_files()
    else:
        grab_data_by_scraping_and_api_requests()
        stored_data = grab_data_from_downloaded_raw_files()

    plot_graph(stored_data)

    #when run on command, show graph as image
    plt.savefig("breach_graph.png")

    
    
#function to run py file in command prompt/terminal
if __name__ == "__main__":
    main()
