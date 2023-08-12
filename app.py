from flask import Flask,render_template,request
import os
import requests
from bs4 import BeautifulSoup
import csv
## create the flask app

app=Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")
@app.route("/review", methods=['POST','GET'])
def review():
    if request.method=='POST':
    
        try:
            query = request.form['content'].replace(" ","")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            response = requests.get(f"https://www.flipkart.com/{query}/product-reviews/itm77dc35f7779a4?pid=MOBGQQ9HGCXD47M7&lid=LSTMOBGQQ9HGCXD47M7ECDWS5&marketplace=FLIPKART")
            print(response)
            soup=BeautifulSoup(response.content, "html.parser")
            #print(soup)    
            reviews=[]
            for i in soup.find_all("div", class_="_27M-vq"):
                #print(i)
                review_title=i.find("p", class_= "_2-N8zT").get_text()
                review_comment=i.find("div", class_= "").get_text()
                review_rating=i.find("div", class_= "_3LWZlK _1BLPMq").get_text()
                review_author=i.find("p", class_= "_2sc7ZR _2V5EHH").get_text()
                reviews.append([review_title,review_author,review_rating,review_comment])
            print(reviews)
        
            save_directory= "review"
            csv_path = f"{save_directory}/reviews.csv"
        
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(['review_title','review_author','review_rating','review_comment'])
                writer.writerows(reviews)
                return render_template('result.html', output=reviews) 
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            return f"Error: {str(e)}"
    

    else:
        return render_template('index.html')
    

if __name__=='__main__':
    app.run(debug=True)

    