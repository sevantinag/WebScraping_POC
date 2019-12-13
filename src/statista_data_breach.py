#This file is to scrape data from Statista. This URL contains a graph that gives all the data exposed numbers
#against each year from 2005 - 2018

#To get the number of data exposed number
#get_statista_exposed_data()

#To get the years from the x-axis
#get_statista_year()
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#import for web scraping using BeautifulSoup and selenium to extract data from Graph
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class statista_data_class():
    
    #initialinzing statista_data class
    def __init__(self):
        try:
            self.statista_data_exposed_list = []
            self.statista_year_list = []
            
            #initialising chrome driver, which will be used to open url and scrape graph data
            self.chrome_options = Options()  
            self.chrome_options.add_argument('headless')
            self.chrome_options.add_argument('window-size=1920x1080')
            self.chrome_options.add_argument("disable-gpu")
            
            #path to Chrome Driver. This is required to be Absolute Path
            self.driver = webdriver.Chrome(executable_path='/Users/sevantinag/Downloads/inf510_project/inf510_project/src/chromedriver',options=self.chrome_options)
            
            #running thr URL in the chrome driver
            self.driver.get("https://www.statista.com/statistics/273550/data-breaches-recorded-in-the-united-states-by-number-of-breaches-and-records-exposed/")
            
            #setting the page as html and scraping the html
            self.html = self.driver.page_source
            self.statista_soup = BeautifulSoup(self.html, "html.parser")
            
            #selecting the element in the graph that contains all the breach data numbers 
            self.statista_data_exposed_chart = self.statista_soup.find("g", {"class" : "highcharts-data-labels highcharts-series-1 highcharts-line-series highcharts-color-1"})
            for tag in self.statista_data_exposed_chart:
                self.statista_data_exposed = tag.find('tspan').text.replace(' ', '')
                
                #adding the values to the list
                self.statista_data_exposed_list.append(float(self.statista_data_exposed))
            
            #selecting the element in the graph that contains all the years
            self.statista_year_chart = self.statista_soup.find("g", {"class" : "highcharts-xaxis-labels"})
            for tag in self.statista_year_chart:
                self.statista_year = tag.find('tspan').text
                
                #adding the values to the list
                self.statista_year_list.append(int(self.statista_year))

        except Exception as e:
            print(f"Something went wrong! {e}")
            
    #function to get the number of data exposed number
    def get_statista_exposed_data(self):
        return self.statista_data_exposed_list
    
    #function to get the years from the x-axis
    def get_statista_year(self):
        return self.statista_year_list
    
    
