from sentence_transformers import SentenceTransformer
import json

# Load the pretrained model
model = SentenceTransformer('all-mpnet-base-v2')

# Load the course content JSON file
with open("free_courses_content.json", "r", encoding="utf-8") as file:
    courses = json.load(file)

# Process each course
for course in courses:
    # 1. Generate individual embeddings for title, small_description, and description
    title_embedding = model.encode(course['title'])
    summary_text = f"{course['small_description']} {course['description']}"
    summary_embedding = model.encode(summary_text)
    
    

    # Add these embeddings to the course data
    course['title_embedding'] = title_embedding.tolist()  # Convert to list for JSON compatibility
    # Add the summary embedding to the course data
    course['sld_embedding'] = summary_embedding.tolist()  # Convert to list for JSON compatibility

    # 2. Generate lesson-wise embeddings for each lesson within each chapter
    lesson_embeddings = []
    for chapter, lessons in course['curriculum'].items():
        for lesson in lessons:
            lesson_text = f"{chapter} : {lesson}"
            lesson_embedding = model.encode(lesson_text)
            lesson_embeddings.append({
                "lesson": lesson,
                "chapter": chapter,
                "embedding": lesson_embedding.tolist()
            })
    
    # Add the lesson embeddings to the course data
    course['lesson_embeddings'] = lesson_embeddings

# Save the updated course data with embeddings
with open("courses_with_granular_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, indent=4)

print("Granular embeddings created and saved to courses_with_granular_embeddings.json")
