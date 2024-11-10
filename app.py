import streamlit as st
import pandas as pd
import requests
import re
from config import GROQ_API_KEY, SERPAPI_KEY

# Title for the web app
st.title("AI Data Retrieval Agent")

# File upload section
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(data.head())

    # Get the number of rows in the uploaded data
    num_rows = len(data)

    # Set max_rows based on the length of the data (dynamic max_value)
    max_rows = st.number_input(
        "Enter number of rows to process",
        min_value=1,
        max_value=num_rows,
        value=min(50, num_rows)  # Ensure the default value does not exceed the number of rows
    )

    # Limit the data to the number of rows selected by the user
    data = data.head(max_rows)
    st.write(f"Processing {len(data)} rows")

    # Select the main column for entities
    column = st.selectbox("Select the main column for entities", data.columns)

    # Prompt template input for dynamic query generation
    prompt_template = st.text_input("Enter a custom prompt (e.g., 'Find official contact information for {entity}')")

    # Function to fetch data from GroqAPI
    def fetch_groqapi_data(query):
        api_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        try:
            data = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": query}]
            }
            response = requests.post(api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"GroqAPI returned {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error fetching data from GroqAPI: {e}")
            return None

    # Function to fetch data from SerpAPI
    def fetch_serpapi_data(query):
        serpapi_url = "https://serpapi.com/search"
        params = {
            'q': query,
            'api_key': SERPAPI_KEY
        }
        try:
            response = requests.get(serpapi_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"SerpAPI returned {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error fetching data from SerpAPI: {e}")
            return None

    # Function to extract relevant contact information using regex
    def extract_relevant_info(response_dict, entity):
        contact_info = {}
        try:
            content = ""
            # Check if response is from GroqAPI
            if 'choices' in response_dict:
                content = response_dict.get('choices', [{}])[0].get('message', {}).get('content', '')
            # Check if response is from SerpAPI
            elif 'organic_results' in response_dict:
                content = response_dict.get('organic_results', [{}])[0].get('snippet', '')

            # Only search for contact information specific to the entity
            if entity.lower() in content.lower():
                # Extract emails and phone numbers with improved regex patterns
                email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}', content)
                phone_matches = re.findall(r'(\+?\d{1,2}[-\s]?)?(\d{3})[-\s]?(\d{3})[-\s]?(\d{4})', content)

                # Deduplicate emails and phone numbers
                if email_matches:
                    contact_info['Emails'] = list(set(email_matches))
                if phone_matches:
                    contact_info['Phone Numbers'] = list(set([''.join(match) for match in phone_matches]))

                # Return extracted contact info or a message if nothing found
                if contact_info:
                    return contact_info
                else:
                    return {"Error": f"No contact info found for {entity}"}
            else:
                return {"Error": f"Content is irrelevant to {entity}"}
        except Exception as e:
            st.error(f"Error processing the response: {e}")
            return {"Error": "Could not extract relevant information"}

    # Button to trigger the search
    if st.button("Run Search"):
        if prompt_template and column:
            results = []

            # Show progress spinner while fetching results
            with st.spinner('Fetching data from GroqAPI and SerpAPI...'):
                for idx, entity in enumerate(data[column].dropna().unique()):
                    # Format query based on user template (e.g., "Find official contact information for {entity}")
                    query = prompt_template.replace("{entity}", entity)

                    # Try GroqAPI first
                    response = fetch_groqapi_data(query)

                    # If no response from GroqAPI, fallback to SerpAPI
                    if not response:
                        response = fetch_serpapi_data(query)

                    # If either response is valid, extract contact information
                    if response:
                        extracted_info = extract_relevant_info(response, entity)
                        if extracted_info and "Error" not in extracted_info:
                            results.append({"Entity": entity, **extracted_info})
                        else:
                            st.warning(f"No relevant info extracted for {entity}. Skipping...")
                    else:
                        st.warning(f"Failed to retrieve information for {entity}. Skipping...")
            
            # Display results in a table
            if results:
                results_df = pd.DataFrame(results)
                st.write("Results:")
                st.dataframe(results_df)

                # Option to download the results as CSV
                st.download_button("Download Results", data=results_df.to_csv(index=False), mime="text/csv")
            else:
                st.warning("No valid results to display.")
        else:
            st.warning("Please enter a prompt template and select a column before running the search.")
