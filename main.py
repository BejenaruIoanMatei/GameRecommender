# Command to run this
#   uvicorn main:app --reload

from fastapi import FastAPI, Query
import pandas as pd
import joblib
import ast
from models.recommender_cosine import recommend_game
from models.recommender_nn import recommend_game_nn

app = FastAPI()

data = pd.read_pickle("classifier-model/steam_data.pkl")

data['Tags_str'] = data['Tags'].apply(lambda x: ' '.join(ast.literal_eval(x)) if isinstance(x, str) else '')
data['Genres_str'] = data['Genres'].apply(lambda x: ' '.join(ast.literal_eval(x)) if isinstance(x, str) else '')

data['combined'] = (
    data['Name'].fillna('') + ' ' +
    data['Categories'].fillna('') + ' ' +
    data['About the game'].fillna('') + ' ' +
    data['Tags_str'].fillna('') + ' ' +
    data['Genres_str'].fillna('')
)

vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
games_vector = joblib.load("models/games_vector.pkl")
nn_model = joblib.load("models/nn_model.pkl")

@app.get("/recommend/cosine")
def recommend_cosine(title: str = Query(..., description="Game title")):
    return recommend_game(title, data, games_vector)

@app.get("/recommend/nn")
def recommend_nearest_neighbors(title: str = Query(..., description="Game title")):
    return recommend_game_nn(title, data, games_vector, nn_model)

@app.get("/recommend/")
def recommend_both(title: str = Query(..., description="Game title")):
    nn_result = recommend_game_nn(title, data, games_vector, nn_model)
    cosine_result = recommend_game(title, data, games_vector)

    return {
        "nn": nn_result,
        "cosine": cosine_result
    }
