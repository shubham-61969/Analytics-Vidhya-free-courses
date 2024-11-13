
# Analytics Vidhya Course Search - Preprocessing Documentation

This project involves scraping, extracting, and embedding free courses from Analytics Vidhya. We process the data to create granular embeddings that enhance search functionality, allowing users to find relevant courses based on their search queries. This document explains each step, including scraping, data extraction, embedding creation, and final search implementation.

## Table of Contents
1. [Overview](#overview)
2. [Intuition](#intuition)
3. [Step 1: Scraping Course URLs (`get_url.py`)](#step-1-scraping-course-urls-get_urlpy)
4. [Step 2: Extracting Course Details (`scraper.py`)](#step-2-extracting-course-details-scraperpy)
5. [Step 3: Embedding Creation (`create_embedding.py`)](#step-3-embedding-creation-create_embeddingpy)
6. [Step 4: Finding Relevant Courses (`find_matching.py`)](#step-4-finding-relevant-courses-find_matchingpy)

---

## Overview

We aim to create an efficient search system for free courses by:
1. Scraping all available free course URLs from Analytics Vidhya.
2. Extracting course details such as titles, descriptions, and curriculums.
3. Generating embeddings for each course component.
4. Matching a user’s search query to course components using cosine similarity, providing the most relevant courses.

---

## Intuition

This project is designed to provide users with relevant courses based on natural language queries. The motivation behind each preprocessing step is to maximize search relevance, ensuring users find courses that meet their needs. The following sections explain the intuition behind each step of our approach:

1. **Comprehensive Data Collection**:
   - To build an effective search tool, it’s essential to have a complete dataset of free courses. By scraping all free course URLs, we ensure our dataset includes the full range of content available on Analytics Vidhya, maximizing the search tool’s utility and completeness.
   
2. **Layered Information Extraction**:
   - Courses on Analytics Vidhya contain multiple content layers, including titles, descriptions, and detailed curriculums. Each layer holds unique information that could match user queries in different contexts. Extracting this layered content allows for a more nuanced search experience:
     - **Titles** often capture the course’s general focus (e.g., "Machine Learning for Beginners").
     - **Descriptions** provide additional details about what the course covers.
     - **Curriculums** list specific topics and lessons, enabling highly granular search results when users search for specific terms (e.g., "Backpropagation in Neural Networks").
   - By breaking down each course into these components, we allow the search system to respond flexibly to both broad and specific queries.

3. **Embeddings for Semantic Matching**:
   - User queries can vary widely in wording, but often have similar meanings (e.g., "data science basics" vs. "introduction to data science"). Embeddings encode the semantic meaning of text, making it possible to match user queries to courses based on intent rather than exact wording.
   - Using pre-trained language models for embedding creation allows us to capture deep semantic relationships in the data, ensuring the system recognizes similar content across different phrasing. This makes the search experience more intuitive and effective, as users don’t need to guess the exact wording used in course titles or descriptions.

4. **Multi-Layered Matching**:
   - By creating embeddings at multiple levels (title, summary, lessons), we achieve a search mechanism that can respond to user queries at varying degrees of specificity. This approach allows users to search for courses based on:
     - **Broad Topics**: A query like "machine learning" can match titles and descriptions across multiple courses.
     - **Detailed Topics**: A more detailed query like "gradient descent optimization" can match specific lessons within a course curriculum.
   - By matching each level (title, summary, curriculum) separately, we can rank courses based on the relevance of each component, providing a more comprehensive search experience.

---

## Step 1: Scraping Course URLs (`get_url.py`)

The script `get_url.py` scrapes the URLs of all free courses on Analytics Vidhya.

- **URL Construction**: A base URL for the courses page is defined with pagination. The code loops through pages to gather course URLs.
- **Scraping Logic**:
  - Each page is fetched using the `requests` library.
  - If a page loads successfully, BeautifulSoup parses it.
  - All course links are collected from HTML elements matching course cards.
- **Filtering**:
  - Only free courses are selected by checking the course price.
- **Output**:
  - The URLs of all free courses are saved in a JSON file (`free_course_links.json`) for further processing.

### Code Snippet:
```python
url = base_url + str(page)
response = requests.get(url)
# Parse the page and filter free courses
```

## Step 2: Extracting Course Details (`scraper.py`)

In `scraper.py`, we fetch detailed information for each course using the URLs obtained in the previous step.

- **Data Extraction**:
  - For each URL, a request is made to retrieve course data.
  - The script extracts the following:
    - **Title**: Retrieved from the `meta` property.
    - **Small Description**: Also retrieved from metadata.
    - **Full Description**: Scraped from the course content area.
    - **Curriculum**: Each chapter and lesson are parsed and stored in a dictionary structure.
- **Output**:
  - All course information is saved to a JSON file (`free_courses_content.json`), providing structured data for embedding creation.

### Code Snippet:
```python
chapters = soup.find_all("li", class_="course-curriculum__chapter")
# Loop through chapters and extract lessons
course_curriculum[chapter_title] = lesson_titles
```

## Step 3: Embedding Creation (`create_embedding.py`)

The file `create_embedding.py` generates embeddings for each course using the `sentence-transformers` library.

- **Embedding Model**: The model `all-mpnet-base-v2` is loaded to encode textual data.
- **Embedding Generation**:
  - **Title Embedding**: Encodes the course title.
  - **Summary Embedding**: Combines the small description and full description, creating an embedding for a more comprehensive course summary.
  - **Lesson Embeddings**: Each lesson within the curriculum is embedded to allow granular matching at the chapter/lesson level.
- **Data Structure**:
  - The embeddings are added to the course data, structured for compatibility with JSON.
- **Output**:
  - The course data with embeddings is saved to `courses_with_granular_embeddings.json`.

### Code Snippet:
```python
title_embedding = model.encode(course['title'])
summary_embedding = model.encode(f"{course['small_description']} {course['description']}")
# Generate embeddings for each lesson
```

## Step 4: Finding Relevant Courses (`find_matching.py`)

The script `find_matching.py` implements a search function that compares user queries with course embeddings to find the best matches.

- **Search Mechanism**:
  - The user’s query is encoded to create a query embedding.
  - For each course:
    - **Title Similarity**: Calculates cosine similarity with the title embedding.
    - **Summary Similarity**: Calculates cosine similarity with the summary embedding.
    - **Lesson Similarity**: Computes the maximum similarity score among all lesson embeddings.
- **Threshold Filtering**:
  - Thresholds are applied to filter out courses with low similarity scores.
- **Ranking and Sorting**:
  - Courses are ranked based on their similarity scores.
- **Output**:
  - The sorted list of courses is displayed as the best matches for the user’s query.

### Code Snippet:
```python
title_similarity = cosine_similarity([query_embedding], [course['title_embedding']])[0][0]
sld_similarity = cosine_similarity([query_embedding], [course['sld_embedding']])[0][0]
```

---

This comprehensive documentation explains the approach and intuition, detailing the purpose of each step and its impact on improving the search functionality. Let me know if you need further enhancements!
