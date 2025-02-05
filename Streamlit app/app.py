import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

st.set_page_config(page_title="Google Scraper", page_icon="🔍", layout="wide")


st.markdown(
    """
    <style>
    .big-title {
        font-size:36px !important;
        text-align: center;
        color: #ff4b4b;
        font-weight: bold;
    }
    .stTextInput > label {
        font-size:18px;
        font-weight: bold;
    }
    .stButton button {
        background-color: #ff4b4b !important;
        color: white !important;
        font-size: 16px;
        border-radius: 10px;
        padding: 8px 24px;
    }
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<p class="big-title">🔍 Google Search Scraper</p>', unsafe_allow_html=True)
st.write("Enter a search term and collect **all links** from the first **3 pages of Google**.")


query = st.text_input("🔎 Enter Search Query:")


if st.button("Search Google"):
    if query.strip():
       
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("🚀 Searching Google...")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(options=options)


      
        # search_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
        # driver.get(search_url)
        
        driver.get("https://www.google.com/search?q=" + query.replace(" ", "+"))

        all_links = set()
        page = 1

        while page <= 3:  
            time.sleep(2) 
            search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc a")

            for result in search_results:
                link = result.get_attribute("href")
                if link:
                    all_links.add(link)

            progress_bar.progress(page * 33)

            try:
           
                next_button = driver.find_element(By.LINK_TEXT, "Next")
                next_button.click()
                page += 1
            except NoSuchElementException:
                break  

        driver.quit()

      
        df = pd.DataFrame(list(all_links), columns=["🌍 Web Links"])

       
        status_text.text("✅ Scraping Completed!")
        progress_bar.empty()

       
        st.write("### 🔗 Extracted Links:")
        st.dataframe(df, use_container_width=True)

       
        copy_text = "\n".join(df["🌍 Web Links"])
        st.code(copy_text, language="text")
        st.success("✅ You can copy and save these links!")

    else:
        st.warning("⚠️ Please enter a search query.")
