from bs4 import BeautifulSoup
import requests
import pandas as pd

#create dataframe for book data with columns for data analysis
df = pd.DataFrame(columns =['Book Name', 'Category', 'Number of Reviews', 'Rating out of 5', 'Book Price', 'Stock on Hand'])

pages = range(1,51)

for page in pages:
    #create a variable request where the URL is for all books on the TOSCRAPE website
    URL = "http://books.toscrape.com/catalogue/category/books_1/page-" + str(page) + ".html"
    r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #get a list of books on the page under the <ol> tag
    BooksOnPage = soup.find("ol", class_='row').find_all("li", 
                                                 class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    
    #1st FOR LOOP: iterate through each <li> tag to find the name of the book
    
    for bts in BooksOnPage:
        tagstring = bts.find("h3").find("a", href=True)
        s = str(tagstring)
        sub1 = 'href="../../'
        sub2 = '/index.html"'
        pos1 = s.index(sub1)
        pos2 = s.index(sub2)
        bnts = s[pos1 + len(sub1): pos2]
        
        #create a new URL and go to the page for the current book being iterated through
        book_url = "http://books.toscrape.com/catalogue/"+ bnts +"/index.html"
        p = requests.get(book_url)
        page_soup = BeautifulSoup(p.content, 'html.parser')
        
        #get a list of items on the page under the <div> class="row" tag
        metrics = page_soup.find("div", class_="col-sm-6 product_main")
        
        #get the values for the metric for price
        fprice = str(metrics.find("p", class_="price_color").text)
        price = float(fprice[1:])
        
        #manipulate stock string to get the available books attached to the book
        stock_string = metrics.find("p", class_="instock availability").text
        stock_split = stock_string.split()
        stock_num = int(stock_split[2][1:])
    
        
        #manipulate star-rating string to get the rating attached to the book
        star_attr = metrics.find("p", class_="star-rating")
        s_star_attr = str(star_attr)
        star_split = s_star_attr.split()
        rating = star_split[2][:-2]
        
        #get the number of reviews
        bmetrics = str(page_soup.find("table", class_="table table-striped"))
        start_pos = bmetrics.find('<th>Number of reviews</th>')
        new_s = bmetrics[start_pos:]
        review_start = new_s.find('<td>')
        review_end = new_s.find('</td>')
        review_num = int(new_s[review_start + 4:review_end])
        
        #get the category for the book
        breadcrumb = page_soup.find("ul", class_="breadcrumb")
        catfinds = breadcrumb.find_all("a", href=True)
        cat = catfinds[2].text
        
        #get the name of the book
        bookname = str(breadcrumb.find("li", class_="active"))
        bn_start = bookname.find('">')
        bn_end = bookname.find('</l')
        booktitle = bookname[bn_start + 2 : bn_end]
        
        #assign metrics found to df
        lst = [booktitle, cat , review_num , rating , price , stock_num]
        df.loc[len(df)] = lst
    
    if page == 50:
        print('All books on pages have been processed!')
    else:
        print('All books for page ',page,' have been processed. Moving on to page',page + 1,'...')    
    
            
print('There are ', len(df),' rows in the dataframe')