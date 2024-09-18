import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("API key not found. Please set it in the .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_topics_for_url(url: str) -> str:
    prompt = f"""
    You are an expert in analyzing SEO content. Analyze the URL '{url}' and perform the following task:
    Extract the most prominent topics. Summarize your findings in 5-10 keywords (in English). Consider the keywords in the URL as well.

    Format your response exactly as follows:
    keyword1, keyword2, keyword3, ...

    If the provided URL is thin in content, return the following output:
    * No topics found
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing web pages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )

        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        print(f"Error processing URL {url}: {str(e)}")
        return "* Error processing URL"

def process_url(url):
    time.sleep(20)  # Add a 20-second delay between API calls
    topics = get_topics_for_url(url)
    return {
        'Top pages': url,
        'Topics': topics
    }

def process_csv(input_path, output_path, num_rows=None):
    # Read the CSV file
    df = pd.read_csv(input_path, nrows=num_rows)

    # Process URLs in parallel
    with ThreadPoolExecutor(max_workers=1) as executor:  # Reduced to 1 worker to avoid rate limiting
        future_to_url = {executor.submit(process_url, url): url for url in df['Top pages']}
        results = []
        for future in tqdm(as_completed(future_to_url), total=len(df), desc="Processing URLs"):
            results.append(future.result())

    # Create a new DataFrame with the results
    result_df = pd.DataFrame(results)

    # Merge the results with the original DataFrame
    merged_df = pd.merge(df, result_df, on='Top pages', how='left')

    # Save the processed data to a new CSV file
    merged_df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    input_file = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/Data_CSV/url_data.csv"
    output_file = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/Data_CSV/processed_url_data.csv"

    # Process only the first 5 rows for testing
    #process_csv(input_file, output_file, num_rows=5)

    # Uncomment the following line to process the entire dataset
process_csv(input_file, output_file)