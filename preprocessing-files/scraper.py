import requests
from bs4 import BeautifulSoup
import json

# # URL for Analytics Vidhya Free Courses
# url = "https://courses.analyticsvidhya.com/courses/building-smarter-llms-with-mamba-and-state-space-model"



def scrap_url(url):
    # Send a GET request to fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # # Extract the c
    # ourse title
    title = soup.find("meta", property="og:title")["content"] if soup.find("meta", property="og:title") else "Title not found"
    small_description = soup.find("meta", property="og:description")["content"] if soup.find("meta", property="og:description") else "Small description not found"
    course_url = soup.find("meta", property="og:url")["content"] if soup.find("meta", property="og:url") else "url not found"

    # Extract the course description (fixed here)
    description = soup.find("div", class_="custom-theme").get_text(strip=True) if soup.find("div", class_="custom-theme") else "Course Description not found"


    course_curriculum = {}

    # Find all chapters
    chapters = soup.find_all("li", class_="course-curriculum__chapter")

    # Loop through each chapter and extract its title and lessons
    for chapter in chapters:
        # Extract chapter title
        chapter_title = chapter.find("h5", class_="course-curriculum__chapter-title").get_text(strip=True)
        
        # Find all lessons within the chapter
        lessons = chapter.find_all("span", class_="course-curriculum__chapter-lesson")
        
        # Extract lesson titles
        lesson_titles = [lesson.get_text(strip=True) for lesson in lessons]
        
        # Add the chapter and its lessons to the dictionary
        course_curriculum[chapter_title] = lesson_titles

    # print(course_curriculum)
    # Store data in a dictionary
    course_data = {
        "title": title,
        "small_description" : small_description,
        "url" : course_url,
        "description": description,
        "curriculum": course_curriculum
    }
    return course_data



# Load the course links from the JSON file
with open("free_course_links.json", "r") as f:
    course_links = json.load(f)



free_courses_contents = []
# Loop over each course link
for link in course_links:
    # print(link)

    # print("#######################\n\n\n")
    free_courses_contents.append(scrap_url(link))


    # print("\n\n\n***************************")
# print(course_data)

# Save the course links to a JSON file
with open("free_courses_content.json", "w") as f:
    json.dump(free_courses_contents, f, indent=4)


