---
title: Analytics-Vidhya Free-Courses
emoji: 👁
colorFrom: pink
colorTo: green
sdk: gradio
sdk_version: 5.5.0
app_file: app.py
pinned: false
short_description: This is assignment for Analytics Vidhya Gen AI Intern
---

# Analytics Vidhya: Free Course Search

This project is a Gradio-based web application that allows users to search for relevant courses on Analytics Vidhya. It uses a pre-trained sentence-transformer model to calculate the similarity between a user query and course titles, descriptions, and lesson content, presenting the most relevant courses based on the query.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [License](#license)

## Features
- **Course Search**: Enter a query to find relevant courses from the dataset based on title, description, and lesson content.
- **Similarity-Based Ranking**: Courses are ranked by their similarity score, determined using cosine similarity.
- **Interactive UI**: Built with Gradio, making it easy to interact and retrieve search results.
  
## Installation

### Prerequisites
- [Python 3.7+](https://www.python.org/downloads/)
- [Git LFS](https://git-lfs.github.com/) for handling large files if the dataset file (`courses_with_granular_embeddings.json`) is over 10 MB.

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://huggingface.co/spaces/<username>/Analytics-Vidhya_Free-Courses.git
    cd Analytics-Vidhya_Free-Courses
    ```

2. **Install Dependencies**
    Install the necessary packages specified in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Git LFS (if required)**
   ```bash
   git lfs install
   git lfs pull
   ```

4. **Run the Application**
    ```bash
    python app.py
    ```

## Usage
1. Open the Gradio app on `localhost` or the designated Hugging Face Space link.
2. Enter a search query in the text box, and click "Submit" to find relevant courses.
3. Results will be displayed in a table format, showing course titles, descriptions, and links.

## Project Structure
```plaintext
Analytics-Vidhya_Free-Courses/
├── app.py                    # Main application code
├── requirements.txt          # Dependencies required to run the app
├── courses_with_granular_embeddings.json  # Dataset with course embeddings
├── .gitattributes            # File to specify Git LFS-tracked files
├── README.md                 # Project README
└── preprocessing-files       # Folder containing scripts and files used for preprocessing course data
    ├── get_url.py               # Script to scrape URLs of free courses from Analytics Vidhya
    ├── scraper.py               # Script to extract detailed course data from each URL
    ├── free_course_links.json   # JSON file containing URLs of all free courses
    ├── free_courses_content.json # JSON file containing scraped details of each free course (title, description, curriculum)
    ├── create_embedding.py      # Script to generate embeddings for course titles, descriptions, and lessons
    ├── find_matching.py         # Script to find relevant courses based on user queries using similarity matching
    └── README.md                # Detailed documentation explaining the preprocessing steps and scripts
```

## Technologies Used
- **Gradio**: For creating the interactive web interface.
- **Sentence Transformers**: For generating text embeddings to compare queries and course content.
- **Scikit-Learn**: For cosine similarity calculations.
- **Git LFS**: To manage large files like `courses_with_granular_embeddings.json`.

## License
This project is not at all licensed.
