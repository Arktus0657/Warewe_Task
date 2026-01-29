# store/ml/model_store.py
from .train_recommender import train_user_item_matrix

_user_item = None
_similarity = None

def load_model():
    global _user_item, _similarity
    if _user_item is None or _similarity is None:
        _user_item, _similarity = train_user_item_matrix()
    return _user_item, _similarity
