# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     df["Combined_Research"] = df[["Research Interest 1", "Research Interest 2"]].fillna('').agg(' '.join, axis=1)
#     return df

# def recommend_professors(user_input, df, top_n=3):
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(df["Combined_Research"].values)
#     user_tfidf = vectorizer.transform([user_input])
    
#     similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
#     top_indices = similarities.argsort()[-top_n:][::-1]
    
#     return df.iloc[top_indices][["Name", "College/Company", "Citations", "h-index", "Research Interest 1", "Research Interest 2"]]

# # Load Data
# data_path = "C:\\Users\\krish\\OneDrive\\Desktop\\sem6\\llm\\project\\4_updated_professor_data.csv"
# df = load_data(data_path)

# # Example Usage
# # user_input = "Bridging the Gap: AI-Driven Fusion of Skin Tones in Skin Cancer"
# user_input = "Lightweight Generative AI on Edge Devices: Pruning Strategies for VGG-16 and MobileNet on CIFAR"

# recommendations = recommend_professors(user_input, df)

# # Display results properly
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)
# print(recommendations.to_string(index=False))
import pandas as pd
from sentence_transformers import SentenceTransformer, util

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["Combined_Research"] = df[["Research Interest 1", "Research Interest 2"]].fillna('').agg(' '.join, axis=1)
    return df

def recommend_professors(user_input, df, top_n=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Pretrained Transformer Model
    research_embeddings = model.encode(df["Combined_Research"].tolist(), convert_to_tensor=True)
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(user_embedding, research_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_n]
    
    recommended_df = df.iloc[top_indices.tolist()]
    
    # Convert 'Citations' to numeric and sort in descending order
    recommended_df["Citations"] = pd.to_numeric(recommended_df["Citations"], errors='coerce')
    recommended_df = recommended_df.sort_values(by="Citations", ascending=False)
    
    return recommended_df[["Name", "Affiliation", "Citations", "h-index", "Research Interest 1", "Research Interest 2"]]

# Load Data
data_path = "C:\\Users\\krish\\OneDrive\\Desktop\\sem6\\llm\\project\\4_updated_professor_data.csv"
df = load_data(data_path)

# Example Usage
user_input = "Analysis of COVID-19 from Lung CT Scan"
recommendations = recommend_professors(user_input, df)

# Display results properly
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(recommendations.to_string(index=False))
