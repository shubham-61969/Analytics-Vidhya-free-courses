from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Load the model
model = SentenceTransformer('all-mpnet-base-v2')

# Load the courses data with granular embeddings
with open("courses_with_granular_embeddings.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

# Function to find relevant courses based on a user query
def find_relevant_courses(user_query):
    # Encode the user query
    query_embedding = model.encode(user_query)

    # Store results with similarity scores
    results = []

    for course in courses:
        # 1. Calculate similarity with the title embedding
        title_similarity = cosine_similarity([query_embedding], [course['title_embedding']])[0][0]

        # 2. Calculate similarity with the sld_embedding (small description + description)
        sld_similarity = cosine_similarity([query_embedding], [course['sld_embedding']])[0][0]

        # 3. Calculate similarities with each lesson embedding and take the maximum
        lesson_similarities = [
            cosine_similarity([query_embedding], [lesson['embedding']])[0][0]
            for lesson in course['lesson_embeddings']
        ]
        max_lesson_similarity = max(lesson_similarities) if lesson_similarities else 0
        title_threshold=0.3
        sld_threshold=0.3
        lesson_threshold=0.3
        # Apply thresholds: if a score is below its threshold, set it to zero
        if(title_similarity >= title_threshold or sld_similarity >= sld_threshold or max_lesson_similarity >= lesson_threshold):
            # Create a sorted list of scores in descending order for ranking
            sorted_scores = sorted([title_similarity, sld_similarity, max_lesson_similarity], reverse=True)
            # Append course data with sorted scores for ranking
            results.append((course['title'], sorted_scores))

    # Sort courses by the sorted scores list
    # If two courses have the same 0th element, sort by 1st element, then by 2nd element
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    
    # Return the course titles in ranked order
    return [title for title, _ in sorted_results]

# Get user input and find relevant courses
user_query = "Automation"

# Find and display relevant course titles
relevant_courses = find_relevant_courses(user_query)
print("Courses matching your query:")
for course_title in relevant_courses:
    print(course_title)
