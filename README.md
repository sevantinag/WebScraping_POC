# inf510_project
The project is set to scrape websites and retreive data from API to check for companies that were breached and the number of accounts that were exposed.

The main file NAG_SEVANTI_hw5.py is the file that is to be run. But before running the file, following environment setups are to be made:

This project requires the following packages:
1. Download Chromedriver from:
   - For Chrome Versions 78: “https://chromedriver.storage.googleapis.com/index.html?path=78.0.3904.105/“
   - For Chrome Versions 79: "https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/"
  and add the exe file as per the system's OS to the project folder (Replace if existing)
2. Change the absolute path of the 'chromedriver' in 'statista_data_breach.py' LINE NO: 31
3. Install requests
4. Install BeautifulSoup
5. Install Selenium
6. Install Tweepy for Twitter API usage
7. Install Matplotlib for plotting graph


On Windows to successfully run nag_sevanti.ipynb file, on Anaconda Prompt navigate to Anaconda folder ("C:/Users/usr_name/Anaconda") and install the following:

1. Install Selenium
2. Install requests
3. Install BeautifulSoup
4. Install Tweepy for Twitter API usage
5. Install Matplotlib for plotting graph

To run this project, make sure the above packages are installed, and then simply clone the repo at https://github.com/sevantinag/inf510_project.git

To run through command, navigate to project folder and type:
python NAG_SEVANTI_hw5.py -source=remote
(or)
python NAG_SEVANTI_hw5.py -source=local

This will generate a graph as breach_graph.png

Altenatetively, one can run the jupyter notebook nag_sevanti.ipynb and see the graph plotted on it
