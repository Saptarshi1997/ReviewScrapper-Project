import re
from urllib.request import urlopen as ureq
import pymongo
from pymongo import mongo_client
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify




app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template("index.html")


@app.route('/scrap', methods=['POST'])
def search_box():
    searchstring = request.form['content'].replace(' ', '')
    try:
        
        dbconn = pymongo.MongoClient("mongodb://localhost:27017/")
        db = dbconn["Scrapperdb"]
        mycollection = db[searchstring]
        # print(mycollection)
        # rev = dbconn.list_database_names() 
        
        rev2= mycollection.find({})
        # print(type(rev2))
        k = list(rev2)
        # print(k)

        if len(k) > 0 :
            
            # a= rev2.get('Product')
            # print(a)
        
            # if a==searchstring:
            reviews= mycollection.find({})
            # c = list(reviews)
            # print(c)
                
                
            # a_product = i["Product"]
            # a_rating = i["Rating"]
            # a_title = i["Title"]
            # a_description = i["Description"]
            # all_rev.append(i)
            # print(k)
                    

            # print(len(all_rev))

            # print(all_rev)
            return render_template("results.html", reviews=reviews)

        else:
            url = "https://www.flipkart.com/search?q=" + searchstring
            # print(url)

            uClient = ureq(url)
            all_product_page = uClient.read()
            uClient.close()



            soup = BeautifulSoup(all_product_page, 'html.parser')
                # print(soup.prettify())

            product = soup.find_all("div", {"class": "_2kHMtA"})
            reviews = []
            for item in product:
                product_page = "https://www.flipkart.com" + item.a["href"]
                # print(product_page)
                # print(reviews[0].text)

                review_req = requests.get(product_page)
                htmlcontent_review = review_req.content

                # print(type(htmlcontent_review))
                review_soup = BeautifulSoup(htmlcontent_review, 'html.parser')
                # print(review_soup)

                review_class = review_soup.find("div", {"class": "col JOpGWq"})
                # print(review_url)
                
                
                try:
                    review_attr = review_class.find_all('a', attrs={'href': re.compile('/product-reviews')})
                    review_href = review_attr[-1]['href']
                    review_url = "https://www.flipkart.com" + review_href

                    # for items in link:
                    #     print(items['href'] +'\n')
                    # # reviews = soup.div.div.find_all("div")

                    # print(review_url)
                    
                    for page in range(1,4):
                        # print(review_url+str(page))
                        review_page_link = review_url + '&page=' + str(page)
                        # print(review_page_link)


                        page_req = requests.get(review_page_link)
                        page_htmlcontent = page_req.content
                        # print(type(htmlcontent))
                        page_soup = BeautifulSoup(page_htmlcontent, 'html.parser')
                        # print(soup.prettify())

                        page_product_review = page_soup.find_all(
                            "div", {"class": "col _2wzgFH K0kLPL"})

                        # for star in reviews:
                        # print(star.text)

                        # print(reviews.text)
                        # star= reviews[0].find('div', {'class':''})
                        # print(star)
                        
                        
                        for review in page_product_review:
                            # find('div', {"class": "_3LWZlK _1BLPMq"})
                            try:
                                stars = review.div.div.text
                            except:
                                print("No Rating")
                            # find('p', {"class": "_2-N8zT"})
                            try:
                                commentheads = review.div.p.text
                            except:
                                print("No Commentheads")
                            try:
                                commentbodies = review.find('div', {"class": 't-ZTKy'}).text
                            except:
                                print("No commentbodies")
                            # for star, commenthead, commentbody in zip(stars, commentheads, commentbodies):
                            # print(stars, commentheads, commentbodies + "\n")
                            
                            dictionary = {"Product": searchstring, "Rating": stars, "Title": commentheads,
                                            "Description": commentbodies}
                            mycollection.insert_one(dictionary)
                            reviews.append(dictionary)
                        # return render_template('results.html', reviews=reviews)
                        
            
                except:
                    print('no reviews')
        
            print(len(reviews))
            return render_template('results.html', reviews=reviews)
        
    except:
        return 'something went wrong'
    







if __name__ == "__main__":
    app.run(debug=True)
