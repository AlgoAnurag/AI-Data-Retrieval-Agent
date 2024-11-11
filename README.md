# AI Data Retrieval Agent

## Project Description

The AI Data Retrieval Agent is a Streamlit-based web application that leverages GroqAPI and SerpAPI to retrieve and extract contact information for companies listed in a CSV file. This tool is designed to facilitate the extraction of data such as emails and phone numbers for each entity by generating targeted queries.

## Features

- **Dynamic Prompting**: Customize search prompts to extract specific contact information.
- **API Integration**: Utilizes GroqAPI and SerpAPI to fetch data from multiple sources.
- **Data Extraction**: Extracts and displays emails and phone numbers using regex.
- **User-friendly Dashboard**: Allows for CSV file upload, preview, and selective row processing.
- **CSV Download**: Download extracted data in CSV format.

## Setup Instructions

### Prerequisites

- Python 3.7+
- Git
- An IDE or text editor like VS Code

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AlgoAnurag/AI-Data-Retrieval-Agent.git
   cd AI-Data-Retrieval-Agent

# Usage Guide

## Running the Application

1. **Start the Streamlit app:**
   - Open your terminal and run the following command:
     ```bash
     streamlit run app.py
     ```

2. **Upload a CSV file:**
   - Upload a CSV file containing company names. The app will preview the file and prompt you to select the main column that contains the entity names.

3. **Enter a custom prompt:**
   - Specify the information you need by entering a custom prompt template. For example:
     - "Find the official contact information for {entity}"

4. **Run the search:**
   - Click the "Run Search" button to start retrieving data. The app will first attempt to fetch data using **GroqAPI** and will fall back to **SerpAPI** if necessary.

5. **Download Results:**
   - Once the search completes, you can download the extracted contact information as a CSV file directly from the dashboard.

# API Keys and Environment Variables

To run the application successfully, you'll need to configure your API keys for data retrieval and web scraping. These keys should be added to the `.env` file.

1. **GROQ_API_KEY**  
   This key allows access to **GroqAPI** for data retrieval.

2. **SERPAPI_KEY**  
   This key enables access to **SerpAPI** for web scraping when a fallback is needed.

**Important:**
- Add these keys to the `.env` file (refer to the [Setup Instructions](#setup-instructions) above).
- For security reasons, **do not push the `.env` file** to GitHub. Ensure that it is added to `.gitignore` to keep your API keys safe.

---

# Optional Features

1. **Advanced Query Templates:**
   - You can use advanced prompts to retrieve multiple fields in a single query. For example, you could specify a template like:
     - "Find the official contact information, location, and website for {entity}"

2. **Error Handling:**
   - The application automatically handles errors from failed API calls or irrelevant responses and will notify users accordingly with helpful error messages.

## Project Screenshot
Example output from the app:

![Dashboard Screenshot](screenshots/)

---

**Note:**  
Ensure that you have the required API keys and the `.env` file set up properly before running the application.
