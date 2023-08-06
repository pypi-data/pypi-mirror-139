# auntminnnie-update
this package for retirve auntminnie recent news, webinars and radiology conference

# how it work?
his package will scarape in [auntminnnie](https://www.auntminnie.com/) to get latest news, webinars and radiology conference.
this package use BeautifulSoup4 and requests.
and then produce output of excel & csv file or JSON thats ready to use in your web or mobile apps.
- .info() for info how to use
- .test() for testing the web 
- .data() for take all data from web 
- .createjson() for show data & create file json 
- .excelcsv() for show data & create file excel & csv 
- .run() for run .test, .data, .createjson, and .excelcsv
all exctract file in folder resultfile

the .data feature in .News and .Webinars can access certain pages as we want. 
Enter which page you want to access when defining .News or .Webinars.

default is scraping page number one.

i.e .News(2) for access page two in news.

# other package that need to be instaled
- BeautifulSoup4
- requests
- pandas(openpyxl)
