import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_url_with_chatgpt(url: str) -> tuple:
    prompt = f"""
    You are an expert in analyzing SEO content. Go to the URL '{url}' and perform the following tasks:
    1. Extract the most prominent topics. Summarize your findings in 5-10 keywords (in English). Consider the keywords in the URL as well.
    2. Identify the single most frequently occurring word in the content of the URL (excluding common stop words).

    Format your response as follows:
    Topics: keyword1, keyword2, keyword3, ...
    Top word: most_frequent_word

    If the provided URL is thin in content, return the following output:
    Topics: * No topics found
    Top word: N/A
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing web pages."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    result = response.choices[0].message.content.strip()
    topics = result.split('\n')[0].split(': ', 1)[1]
    top_word = result.split('\n')[1].split(': ', 1)[1]

    return topics, top_word

def process_csv(input_path, output_path, num_rows=None):
    df = pd.read_csv(input_path)
    
    if num_rows:
        df = df.head(num_rows)
    
    for index, row in df.iterrows():
        url = row["Top pages"]
        topics, top_word = analyze_url_with_chatgpt(url)
        
        df.at[index, "Topics"] = topics
        df.at[index, "Top_word"] = top_word
        
        print(f"Processed {index + 1}/{len(df)} URLs")
    
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    input_file = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/Data_CSV/url_data.csv"
    output_file = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/Data_CSV/processed_url_data.csv"
    
    # Process only the first 5 rows for testing
    process_csv(input_file, output_file, num_rows=5)
    
    # Uncomment the following line to process the entire dataset
    # process_csv(input_file, output_file)