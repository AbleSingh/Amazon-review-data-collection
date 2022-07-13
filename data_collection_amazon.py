import requests
import pandas as pd
from bs4 import BeautifulSoup


reviewList = []

def totalPages(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'})
    return int(reviews.text.strip().split(", ")[1].split(" ")[0])
    

def extract_review(product_url, pageNumber):
    review_url = product_url.replace("dp", "product-reviews") + "?pageNumber=" + str(pageNumber)
    response = requests.get(review_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = soup.findAll('div', {'data-hook': 'review'})
    for item in reviews:
        review = {
            'product_title' : soup.title.text.replace("Amazon.in:Customer reviews:", "").strip(),
            'review_title' : item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'review_date' : item.find('span', {'data-hook': 'review-date'}).text.strip().split("on ")[1],
            'review_month' : item.find('span', {'data-hook': 'review-date'}).text.strip().split("on ")[1].split(" ")[1],
            'review_year' : int(item.find('span', {'data-hook': 'review-date'}).text.strip().split("on ")[1].split(" ")[2]),
            'rating' : int(item.find('i', {'data-hook': 'review-star-rating'}).text.strip().split(" ")[0].split(".")[0]),
            'review_text' : item.find('span', {'data-hook': 'review-body'}).text.strip(),
        }
        reviewList.append(review)

def main():
    product_url = "https://www.amazon.in/Samsung-Emerald-Processor-Purchased-Separately/dp/B0B14PKNS5/ref=sr_1_1_sspa?crid=2867AL7LEYSL4&keywords=phone&qid=1657632443&sprefix=pho%2Caps%2C349&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyRTMyN0JWTVZWNTYmZW5jcnlwdGVkSWQ9QTA1MzUxMDYxQ1BPTlU4R1pIQ0lZJmVuY3J5cHRlZEFkSWQ9QTA2OTIyOTUzRUVJTTBJWThTNkRWJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
    product_url = product_url.split("?")[0]
    review_url = product_url.replace("dp", "product-reviews") + "?pageNumber=" +  str(0)
    totalPg = totalPages(review_url)//10 + 1
    
    for i in range(totalPg):
        print("Collecting for Page: ", i)
        extract_review(product_url, i)
    
    df = pd.DataFrame(reviewList)
    df.to_excel("reviews.xlsx")

    # rating = 0
    # for i in range(len(reviewList)):
    #     rating += reviewList[i]['rating']
    # print("Average Rating: ", rating/len(reviewList))
    
main()