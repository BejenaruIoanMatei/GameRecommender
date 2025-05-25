from sklearn.neighbors import NearestNeighbors

def build_nn_model(games_vector):
    nn_model = NearestNeighbors(n_neighbors=6, metric='cosine')
    nn_model.fit(games_vector)
    return nn_model

def recommend_game_nn(title, data, games_vector, nn_model, n_recommendation=6):
    title = title.lower().strip()

    if 'name_norm' not in data.columns:
        data['name_norm'] = data['Name'].str.lower().str.strip()

    if title not in data['name_norm'].values:
        return {"error": "Game not found."}

    g_idx = data[data['name_norm'] == title].index[0]
    game_vector = games_vector[g_idx]

    distances, indices = nn_model.kneighbors(game_vector, n_neighbors=n_recommendation + 1)
    recommended_indices = indices.flatten()[1:]

    recommendations = []
    for idx in recommended_indices:
        recommendations.append({
            "name": data.iloc[idx]['Name'],
            "image": data.iloc[idx].get('Header image', '')
        })

    return {
        "input": title,
        "recommendations": recommendations
    }
