

import pickle
import streamlit as st # type: ignore
import numpy as np
import io 
import requests

st.header('Book Recommender System')
model = pickle.load(open('artifacts/model.pkl','rb'))
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))



# url = 'https://emmubucket.s3.ap-south-1.amazonaws.com/artifacts/model.pkl'
# response = requests.get(url)
# model = pickle.load(io.BytesIO(response.content))

# url = 'https://emmubucket.s3.ap-south-1.amazonaws.com/artifacts/book_names.pkl'
# response = requests.get(url)
# book_names = pickle.load(io.BytesIO(response.content))

# url = 'https://emmubucket.s3.ap-south-1.amazonaws.com/artifacts/final_rating.pkl'
# response = requests.get(url)
# final_rating = pickle.load(io.BytesIO(response.content))

# url = 'https://emmubucket.s3.ap-south-1.amazonaws.com/artifacts/book_pivot.pkl'
# response = requests.get(url)
# book_pivot = pickle.load(io.BytesIO(response.content))

import requests

# Set page to full width

# Define the API URL
# api_url = "https://by5ldea1kd.execute-api.ap-south-1.amazonaws.com/default/get_data"
api_url = 'https://by5ldea1kd.execute-api.ap-south-1.amazonaws.com/default/fetchBookData'


# Fetch data from the API
response = requests.get(api_url)
data = response.json()

# Display the data using Streamlit
st.title("Books Data")

# Define the number of books per page
books_per_page = 20

# Calculate number of pages
num_pages = (len(data) + books_per_page - 1) // books_per_page

# Display books based on pagination
page_number = st.number_input("Enter page number:", min_value=1, max_value=num_pages, value=1)

start_index = (page_number - 1) * books_per_page
end_index = min(page_number * books_per_page, len(data))
paged_data = data[start_index:end_index]

# Display books in a grid layout
num_rows = 5
num_columns = 4

for i in range(num_rows):
    row_data = paged_data[i * num_columns: (i + 1) * num_columns]
    col = st.columns(num_columns)
    for book, col_item in zip(row_data, col):
        with col_item:
            st.markdown(f"## {book['Book-Title']}")
            st.write(f"Author: {book['Book-Author']}")
            st.image(book['Image-URL'], caption='Book Cover', use_column_width=True)
            st.write("---")


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url



def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url       



selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

if st.button('Show Recommendation'):
    recommended_books,poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])