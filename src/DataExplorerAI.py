import pandas as pd
from openai.embeddings_utils import get_embedding, cosine_similarity

# Load the Excel data
data = pd.read_excel("../sample-code/fileName.xlsx")
data['description_embedding'] = data['description'].apply(lambda x: get_embedding(x, engine="your_embedding_model"))

def find_similar_ids(input_id):
    input_description = data[data['id'] == input_id]['description'].values[0]
    input_embedding = get_embedding(input_description, engine="embedding_test_ada_model")

    data['similarity'] = data['description_embedding'].apply(lambda x: cosine_similarity(input_embedding, x))
    similar_ids = data.sort_values(by='similarity', ascending=False).head(5)['id'].tolist()  # top 5 similar IDs
    return similar_ids

# Example usage
similar_ids = find_similar_ids("your_input_id")
print("Similar IDs:", similar_ids)
