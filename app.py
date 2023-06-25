import streamlit as st
import pickle
import pandas as pd
import requests
import json

def video(movie_id) :
    url = "https://api.themoviedb.org/3/movie/{}/videos?api_key=090699765dc55e21896b2c4d21bffe5f&language=en-US".format(movie_id)

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    l=[]
    for i in json.loads(response.text)['results']:

        if i['name'] == 'Official Trailer':
            l.append(i['key'])
        elif i['type'] == 'Trailer':
            l.append(i['key'])
    return 'https://www.youtube.com/watch?v='+l[-1]

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=090699765dc55e21896b2c4d21bffe5f&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommanded_movies=[]
    recomanded_movies_poster=[]
    movies_video = []
    movie_rating=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommanded_movies.append(movies.iloc[i[0]].title)
        recomanded_movies_poster.append(fetch_poster(movie_id))
        movies_video.append(video(movie_id))
        movie_rating.append(rating.iloc[i[0]].vote_average)
    return recommanded_movies,recomanded_movies_poster,movies_video,movie_rating

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
ratings = pickle.load(open('rating.pkl','rb'))
rating= pd.DataFrame(ratings)


similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Movie Name',
movies['title'].values)

def redirect_button(url: str, text: str= None, color="#FD504D"):
    st.markdown(
    f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

try :
    if st.button(":red[Recommend]"):
        names,posters,videos,movie_ratings=recommend(selected_movie_name)

        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0],width=130)
            st.write('⭐', movie_ratings[0])
            redirect_button(videos[0],"Watch Trailer")
        with col2:
            st.text(names[1])
            st.image(posters[1],width=130)
            st.write('⭐', movie_ratings[1])
            redirect_button(videos[1], "Watch Trailer")
        with col3:
            st.text(names[2])
            st.image(posters[2],width=135)
            st.write('⭐', movie_ratings[2])
            redirect_button(videos[2], "Watch Trailer")
        with col4:
            st.text(names[3])
            st.image(posters[3],width=130)
            st.write('⭐', movie_ratings[3])
            redirect_button(videos[3], "Watch Trailer")
        with col5:
            st.text(names[4])
            st.image(posters[4],width=130)
            st.write('⭐', movie_ratings[4])
            redirect_button(videos[4], "Watch Trailer")

except Exception as e:
    print(e)



