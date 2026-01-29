import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from store.ml.export_dataset import export_interaction_dataset

def train_user_item_matrix():
    data = export_interaction_dataset()
    df = pd.DataFrame(data)

    if df.empty:
        return None, None

    user_item = df.pivot_table(
        index="user_id",
        columns="product_id",
        values="total_score",
        fill_value=0
    )

    similarity = cosine_similarity(user_item)
    similarity_df = pd.DataFrame(
        similarity,
        index=user_item.index,
        columns=user_item.index
    )

    return user_item, similarity_df
