import requests
from bs4 import BeautifulSoup
import json

# Base URL of the courses page with pagination parameter
base_url = "https://courses.analyticsvidhya.com/collections/courses?page="

# Empty list to store all course links
course_links = []

# Loop through the pages until no more courses are found
page = 1
while True:
    # Generate the URL for the current page
    url = base_url + str(page)
    response = requests.get(url)
    
    # Check if the page was successfully loaded
    if response.status_code != 200:
        print("Failed to retrieve page:", page)
        break

    # Parse the page content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all course cards on the page and extract the href attribute for each
    courses = soup.find_all("li", class_="products__list-item")  # Adjust selector as per actual structure
    
    # Check if there are no more courses found, which means we've reached the last page
    if not courses:
        print("No more courses found on page", page)
        break
    
    # Extract href links for each course
    for course in courses:
        price_type = course.find("span", class_="course-card__price").get_text(strip=True)
        # print(course.find("a", class_="course-card course-card__public published").get("href"))
        # break
        link = course.find("a", class_="course-card course-card__public published").get("href")

        if link and price_type=="Free":
            # Add the base URL if the link is relative
            if link.startswith("/"):
                link = "https://courses.analyticsvidhya.com" + link
            course_links.append(link)
    # break
    print(f"Page {page} processed, found {len(courses)} courses.")
    page += 1

# Save the course links to a JSON file
with open("free_course_links.json", "w") as f:
    json.dump(course_links, f, indent=4)

print("Course links extracted and saved to course_links.json")
