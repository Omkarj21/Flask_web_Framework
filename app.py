# This project made with Flask Web Framework,
# This project is to see reviews of Mobile brands with Flipkart website
# This project used Heroku Cloud for deployment

from flask import Flask, render_template, request
# flask-request => The data from a client’s web page gets sent to the server as a global "request" object. In order to process the request data, it should be imported from the Flask module.
# flask-render_template => Instead of returning hardcode HTML from the function, a HTML file can be rendered by the render_template() function. Flask will try to find the HTML file in the templates folder, in the same folder in which this script is present.
from flask_cors import cross_origin # This is nothing but CORS = Cross-Origin Resource Sharing to work with Web
import requests # used to get web data
from bs4 import BeautifulSoup as bs
# Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML, which is useful for web scraping
from urllib.request import urlopen as uReq
# urllib is a package that collects several modules for working with URLs:
# urllib.request for opening and reading URLs
# urllib.error containing the exceptions raised by urllib.request
# urllib.parse for parsing URLs
# urllib.robotparser for parsing robots.txt files


app = Flask(__name__)
# This is abstractly setting the name of the Flask instance to app And we want this for our secret key and decorators.
# Then the Flask instance's name is actually set to __main__ once we run it interactively.

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage(): # This will be 1st page
    # When you click on http://127.0.0.1:5000/ Control comes in this function
    return render_template("index.html")  #Call index.html

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index(): # when Click on http://127.0.0.1:5000/review SEARCH Button
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","") # input entered in text field, remove spaces
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # Contacatinate input with URL
            uClient = uReq(flipkart_url) # Open and Parse URL
            print(uClient)
            flipkartPage = uClient.read() # Read HTML File
            print(flipkartPage)
            uClient.close() # Close connection
            flipkart_html = bs(flipkartPage, "html.parser") # Collect HTML Data
            print(flipkart_html)
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
            print(bigboxes)
            del bigboxes[0:3] # Delete 1st three
            box = bigboxes[0] # Take 1st model
            print(box)
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink) #*******
            print(prodRes)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            print(commentboxes)

            # Below code is to create CSV and add reviews into it
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                print(reviews)
                reviews.append(mydict)
                print(mydict)
                # Below line is to transfer control to results.html with parameter reviews
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)]) # This shows reviews on page http://127.0.0.1:5000/review
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)