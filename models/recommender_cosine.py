import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def recommend_game(title, data, games_vector, n_recommendation=5, alpha=0.3):
    title = title.lower().strip()

    if 'name_norm' not in data.columns:
        data['name_norm'] = data['Name'].str.lower().str.strip()

    if title not in data['name_norm'].values:
        return {"error": "Game not found."}

    g_idx = data[data['name_norm'] == title].index[0]

    jaccard_scores = [
        0 if idx == g_idx else jaccard_similarity(
            data.loc[g_idx, 'Tags'], data.loc[idx, 'Tags']
        )
        for idx in range(len(data))
    ]
    jaccard_scores = np.array(jaccard_scores)
    if np.max(jaccard_scores) > 0:
        jaccard_scores /= np.max(jaccard_scores)

    cosine_scores = cosine_similarity(games_vector[g_idx], games_vector).flatten()
    if np.max(cosine_scores) > 0:
        cosine_scores /= np.max(cosine_scores)

    final_score = alpha * cosine_scores + (1 - alpha) * jaccard_scores
    recomm_idx = final_score.argsort()[::-1][1:n_recommendation + 1]

    recommendations = []
    for idx in recomm_idx:
        recommendations.append({
            "name": data.iloc[idx]['Name'],
            "image": data.iloc[idx].get('Header image', '')
        })

    return {
        "input": title,
        "recommendations": recommendations
    }
