import gradio as gr
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load the model and course data with error handling
try:
    model = SentenceTransformer('all-mpnet-base-v2')  # Load a pre-trained model for embedding text queries and course data
except Exception as e:
    print(f"Error loading model: {e}")

try:
    with open("courses_with_granular_embeddings.json", "r", encoding="utf-8") as f:
        courses = json.load(f)  # Load the course data with precomputed embeddings for titles, descriptions, and lessons
except FileNotFoundError:
    print("Course data file not found.")
    courses = []
except json.JSONDecodeError as e:
    print(f"Error decoding JSON file: {e}")
    courses = []
except Exception as e:
    print(f"Unexpected error loading courses: {e}")
    courses = []

# Define the function to find relevant courses based on query
def find_relevant_courses(query):
    # Encode the query with error handling
    try:
        query_embedding = model.encode(query)  # Generate an embedding for the input query
    except Exception as e:
        print(f"Error encoding query: {e}")
        return [["Error", "Unable to encode query."]]

    # List to store results
    results = []

    # Loop through each course to compute similarity scores
    for course in courses:
        try:
            # 1. Calculate similarity with the title embedding
            title_similarity = cosine_similarity([query_embedding], [course['title_embedding']])[0][0]

            # 2. Calculate similarity with the sld_embedding (small description + description)
            sld_similarity = cosine_similarity([query_embedding], [course['sld_embedding']])[0][0]

            # 3. Calculate similarities with each lesson embedding and take the maximum
            lesson_similarities = [
                cosine_similarity([query_embedding], [lesson['embedding']])[0][0]
                for lesson in course['lesson_embeddings']
            ]
            max_lesson_similarity = max(lesson_similarities) if lesson_similarities else 0  # Get maximum lesson similarity

            # Set thresholds for filtering low-similarity results
            title_threshold = 0.4
            sld_threshold = 0.4
            lesson_threshold = 0.4

            # Apply thresholds: if a score is below its threshold, set it to zero
            if title_similarity >= title_threshold or sld_similarity >= sld_threshold or max_lesson_similarity >= lesson_threshold:
                # Create a sorted list of scores in descending order for ranking
                sorted_scores = sorted([title_similarity, sld_similarity, max_lesson_similarity], reverse=True)

                # Add the course details to the results list if it meets the threshold criteria
                results.append({
                    "title": course['title'],
                    "description": course['small_description'][:60] + '...' if len(course['small_description']) > 60 else course['small_description'],
                    "url": course['url'],
                    "score": sorted_scores  # Include sorted scores to rank results
                })

        except KeyError as e:
            print(f"Missing key in course data: {e}")
        except Exception as e:
            print(f"Unexpected error processing course: {e}")

    # Sort results by similarity score in descending order
    try:
        top_results = sorted(results, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        print(f"Error sorting results: {e}")
        return [["Error", "Unable to sort results."]]

    # Format the results as a list of lists for Gradio's dataframe output
    display_data = [[index + 1, result['title'], result['description'], result['url']] for index, result in enumerate(top_results)]
    
    return display_data  # Return formatted results for display

# Gradio interface function to handle search
def search(query):
    try:
        return find_relevant_courses(query)  # Call find_relevant_courses with the query and return the results
    except Exception as e:
        print(f"Error in search function: {e}")
        return [["Error", "An error occurred during the search."]]

# Customize the layout with Gradio components
with gr.Blocks(css=".submit-button { background-color: orange; color: white; }") as demo:
    gr.Markdown("<h1 style='text-align: center;'>Analytics Vidhya: Free Course Search</h1>")  # Title for the app
    
    with gr.Row():
        query_input = gr.Textbox(
            placeholder="Type a query to search for relevant courses.", 
            label="Search Query", 
            lines=1
        )
    
    # Provide examples to guide user input
    gr.Examples(
        examples=[["Self Driving Car"], ["Activation Functions"], ["Z-Score"]], 
        inputs=query_input,
        label="Examples"
    )
    
    # Submit button styled in orange
    submit_btn = gr.Button("Submit", elem_classes="submit-button")
    
    # Output section for displaying the search results
    output_table = gr.Dataframe(headers=["Sr.No","Title", "Description", "URL"], label="Results")

    # Connect the search function to the submit button
    submit_btn.click(fn=search, inputs=query_input, outputs=output_table)

# Launch the app
if __name__ == "__main__":
    try:
        demo.launch()  # Run the Gradio app
    except Exception as e:
        print(f"Error launching Gradio app: {e}")
