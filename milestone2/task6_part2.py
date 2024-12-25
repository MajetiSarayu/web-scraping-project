from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st
import pandas as pd
import time
import random
import io

base_url = 'https://www.behance.net'

def sel_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def fetch_jobs(url, limit=10):
    driver = sel_driver()
    driver.get(url)
    time.sleep(3)
    
    scrolls, curr = 0, 0
    max_scroll_attempts = 10
    jobs = driver.find_elements(By.CSS_SELECTOR, "div.JobCard-jobCard-mzZ")
    curr = len(jobs)
    while curr < limit and scrolls < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))
        jobs = driver.find_elements(By.CSS_SELECTOR, "div.JobCard-jobCard-mzZ")
        prev = curr
        curr = len(jobs)
        if prev == curr:
            scrolls += 1
        else:
            scrolls = 0

    job_data = {"Job Role": [], "Company": [], "Location": [], "Description": [], "Job Link": []}
    for job in jobs[:limit]:
        role = job.find_element(By.CSS_SELECTOR, "h3.JobCard-jobTitle-LS4").text if job.find_element(By.CSS_SELECTOR, "h3.JobCard-jobTitle-LS4") else "Not Mentioned"
        company = job.find_element(By.CSS_SELECTOR, "p.JobCard-company-GQS").text if job.find_element(By.CSS_SELECTOR, "p.JobCard-company-GQS") else "Not Mentioned"
        location = job.find_element(By.CSS_SELECTOR, "p.JobCard-jobLocation-sjd").text if job.find_element(By.CSS_SELECTOR, "p.JobCard-jobLocation-sjd") else "Not Mentioned"
        description = job.find_element(By.CSS_SELECTOR, "p.JobCard-jobDescription-SYp").text if job.find_element(By.CSS_SELECTOR, "p.JobCard-jobDescription-SYp") else "Not Mentioned"
        link = job.find_element(By.CSS_SELECTOR, "a.JobCard-jobCardLink-Ywm").get_attribute("href") if job.find_element(By.CSS_SELECTOR, "a.JobCard-jobCardLink-Ywm") else "Not Mentioned"
        
        job_data["Job Role"].append(role)
        job_data["Company"].append(company)
        job_data["Location"].append(location)
        job_data["Description"].append(description)
        job_data["Job Link"].append(link)

    driver.quit()
    return job_data

def fetch_assets(url, limit=10):
    driver = sel_driver()
    driver.get(url)
    time.sleep(3)

    scrolls, curr = 0, 0
    max_scroll_attempts = 10
    assets = driver.find_elements(By.CSS_SELECTOR, "div.AssetsContent-container-wjB div.Layout-gridItem-OTU")
    curr = len(assets)
    while curr < limit and scrolls < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        assets = driver.find_elements(By.CSS_SELECTOR, "div.AssetsContent-container-wjB div.Layout-gridItem-OTU")
        prev = curr
        curr = len(assets)
        if prev == curr:
            scrolls += 1
        else:
            scrolls = 0

    asset_data = {"Title": [], "Owner": [], "Likes": [], "Views": [], "Price": [], "Link": [], "Image": []}
    for asset in assets[:limit]:
        try:
            title = asset.find_element(By.CSS_SELECTOR, "a.Title-title-lpJ").text
            owner = asset.find_element(By.CSS_SELECTOR, "a.Owners-owner-EEG").text
            likes = asset.find_element(By.CSS_SELECTOR, "div.ProjectCover-stats-QLg span").text
            views = asset.find_element(By.CSS_SELECTOR, "div.ProjectCover-stats-QLg span:last-child").text
            price = asset.find_element(By.CSS_SELECTOR, "span.PaidAssetsCountBadge-count-yPz").text
            link = asset.find_element(By.CSS_SELECTOR, "a.Title-title-lpJ").get_attribute("href")
            image = asset.find_element(By.CSS_SELECTOR, "img.js-cover-image").get_attribute("src")

            asset_data["Title"].append(title if title else "Not Mentioned")
            asset_data["Owner"].append(owner if owner else "Not Mentioned")
            asset_data["Likes"].append(likes if likes else "Not Mentioned")
            asset_data["Views"].append(views if views else "Not Mentioned")
            asset_data["Price"].append(price if price else "Not Mentioned")
            asset_data["Link"].append(link if link else "Not Mentioned")
            asset_data["Image"].append(image if image else "Not Mentioned")
        except Exception as e:
            print(e)

    driver.quit()
    return asset_data


def download_options(df):
    csv = df.to_csv(index=False).encode("utf-8")
    excel = io.BytesIO()
    df.to_excel(excel, index=False, engine="xlsxwriter")
    excel.seek(0)
    json_data = df.to_json(orient="records")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("Download as CSV", csv, "records.csv", "text/csv")
    with col2:
        st.download_button("Download as Excel", excel, "records.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with col3:
        st.download_button("Download as JSON", json_data, "records.json", "application/json")


def ui():
    st.header("Behance Scraper")
    scrape_type = st.selectbox("Select type of category records you want to fetch", ["Jobs", "Assets"])
    limit = st.text_input("Enter the number of records you want to scrape", "10")
    search_text = st.text_input("Enter the specific type of records you want to fetch")
    
    
    if st.button("Scrape Records"):
        try:
            limit = int(limit)
        except ValueError:
            st.error("Please enter a valid number for the limit.")
            return
        
        if scrape_type == "Jobs":
            search_url = f"{base_url}/joblist?search={search_text.strip()}" if search_text else f"{base_url}/joblist"
            records = fetch_jobs(search_url, limit)
        else:
            search_url = f"{base_url}/assets?search={search_text.strip()}" if search_text else f"{base_url}/assets"
            records = fetch_assets(search_url, limit)
        
        df = pd.DataFrame(records)
        if not df.empty:
            st.success(f"Found {len(df)} Records")
            st.dataframe(df)
            download_options(df)
        else:
            st.error("No records found")
            
# call the ui function
ui()




