import streamlit as st
import pickle as pk
import pandas as pd
import requests

movies_dict=pk.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pk.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=91cebe56813be0ae28ce53932eb62b4b')
    data=response.json()
    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies,recommended_movies_poster

st.title('Movie Recommendation System')

selected_movie_name=st.selectbox('Select movie name:',movies['title'].values)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])