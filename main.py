import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

 file you just created
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file.")
    print("Make sure you created a file named .env with: GEMINI_API_KEY=your_key_here")
    exit()


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def get_jumia_reviews(url):
    """
    Launches a Chrome instance, navigates to Jumia, and extracts review text.
    """
    chrome_options = Options()

    
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)
    reviews = []

    try:
        print(f"🚀 Connecting to Jumia: {url}")
        driver.get(url)

        
         driver.execute_script("window.scrollTo(0, 1500);")
        time.sleep(2)

      
        review_elements = driver.find_elements(
            By.CSS_SELECTOR, "article.-pvs, .rev")

        print(f"🔎 Scanning page for reviews...")

        for el in review_elements[:20]:  # Grab the top 20 reviews
            try:
                
                text = el.find_element(By.CSS_SELECTOR, ".cnt").text.strip()
                if len(text) > 5:
                    reviews.append(text)
            except:
               
                text = el.text.strip()
                if len(text) > 10:
                    reviews.append(text)

    except Exception as e:
        print(f"⚠️ Scraping Error: {e}")
    finally:
        driver.quit()

    return list(set(reviews))  # Remove any accidental duplicates


def analyze_reviews(reviews_list):
    """
    Sends the gathered reviews to Gemini for a professional summary.
    """
    if not reviews_list:
        return "❌ I couldn't find any reviews to analyze. Check if the product actually has ratings."

    
    formatted_reviews = "\n---\n".join(reviews_list)

    prompt = f"""
    You are an expert E-commerce Analyst in Kenya. Analyze these customer reviews from Jumia.
    Provide a clear, professional report covering:
    
    1. THE VIBE: 1-2 sentences on general customer satisfaction.
    2. THE GOOD: 3 bullet points on what users love most.
    3. THE BAD: 3 bullet points on common complaints or 'red flags'.
    4. AUTHENTICITY: Do these look like real Kenyan buyers or bot-generated fluff?
    5. FINAL VERDICT: Give me a clear 'BUY' or 'SKIP' recommendation.
    
    REVIEWS TO ANALYZE:
    {formatted_reviews}
    """

    print("🤖 Sending data to Gemini AI...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI Analysis Error: {e}"



if __name__ == "__main__":
    print("\n" + "="*40)
    print("🇰🇪 JUMIA AI REVIEW SUMMARIZER")
    print("="*40 + "\n")

    product_link = input("Paste the Jumia Product URL: ").strip()

    if "jumia.co.ke" in product_link:
        data = get_jumia_reviews(product_link)

        if data:
            print(f"✅ Extracted {len(data)} unique reviews.")
            print("\n" + "-"*40)
            print("AI ANALYSIS REPORT")
            print("-"*40)

            summary = analyze_reviews(data)
            print(summary)
        else:
            print("❌ No reviews were found on that page.")
    else:
        print("❌ Invalid Link. Please use a 'jumia.co.ke' URL.")
