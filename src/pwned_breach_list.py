#This file is to scrape data from Have I Been Pwned website. This site lists all the company portals that were
#breached and their breach date and the number of data records that were exposed in the breach

#To obtain the list of all the exposed data records
#get_pwned_breach_info()
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#imports for web scraping using BeautifulSoup
import requests
from bs4 import BeautifulSoup

class pwned_breach():
    
    #setting global variable to be used in other files
    pwned_breach_info_list = []
 
    #initialinzing pwned_breach class
    def __init__(self):
        try:
            self.url = 'https://haveibeenpwned.com/PwnedWebsites'
            self.r = requests.get(self.url)
            self.pwned_soup = BeautifulSoup(self.r.content, 'html.parser')
            
            #finding the closest element to the target element, with unique ID
            self.pwned_sibling_element= self.pwned_soup.find('div', {"id" : "notifyMeModal"})
            
            #selecting the target element as the Sibling of the element with unique ID
            self.pwned_breaches_container = self.pwned_sibling_element.find_previous_sibling('div', {"class":"container"})
            
            #using lambda to select element with class "row" and no other additional class name
            self.pwned_breaches_items = self.pwned_breaches_container.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['row'])
            
            for pwned_breaches_item in self.pwned_breaches_items:
                self.pwned_breaches_subitems = pwned_breaches_item.findAll('p')[-1].findAll("strong")[0].next_sibling
                
                #selecting the blocks only with breach date of 2019
                if int(self.pwned_breaches_subitems.split()[-1]) == 2019:
                    
                    #getting the number of breached data of each organization
                    self.pwned_breach_count = float((pwned_breaches_item.findAll('p')[-1].findAll("strong")[2].next_sibling).replace(',', ''))                  
                    self.pwned_breach_info_list.append(self.pwned_breach_count)
       
        #on failed connection, print the error
        except Exception as e:
            print(f"Something went wrong! {e}")
        
        
    #function to obtain the list of exposed data
    def get_pwned_breach_info(self):
        return self.pwned_breach_info_list

