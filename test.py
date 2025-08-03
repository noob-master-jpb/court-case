from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
data = ""
def submit_case_search(case_type: str, case_number: str, year: str):
    """
    Navigates to the court website, fills the search form with user data,
    and submits it.
    """
    driver = webdriver.Firefox()  # You can also use Chrome or any other browser driver
    
    # 1. Navigate to the specific court website URL
    # Replace with the actual URL you are targeting
    court_url = "https://delhihighcourt.nic.in/app/get-case-type-status" 
    driver.get(court_url)

    try:
        # 2. Find the form elements using the IDs you found
        # NOTE: Replace these placeholder IDs with the real ones from the website.
        case_type_element = driver.find_element(By.ID, 'case_type')
        case_number_element = driver.find_element(By.ID, 'case_number')
        case_year_element = driver.find_element(By.ID, 'case_year')
        submit_button_element = driver.find_element(By.ID, 'search')
        
        captcha_code_element = driver.find_element(By.ID, 'captcha-code')
        captcha_input_element = driver.find_element(By.ID, 'captchaInput')
        
        captcha_text = captcha_code_element.text
        # global data
        # data = captcha_text
        case_type_element.send_keys(case_type)
        case_number_element.send_keys(case_number)
        case_year_element.send_keys(year)
        captcha_input_element.send_keys(captcha_text)  # Replace with actual CAPTCHA handling logic

        
        # Handle any CAPTCHA here if necessary (e.g., by pausing)
        # time.sleep(20) 

        # 4. Click the submit button to "send the request"
        print("Submitting form with the provided data...")
        submit_button_element.click()

        # 5. Wait for the results page to load
        print("Waiting for results to load...")
        time.sleep(2) # A simple pause to allow the next page to load

        # At this point, the browser controlled by Selenium is on the results page.
        # You can now get the page's HTML for parsing.
        page_html = driver.page_source
        print("Results page loaded successfully.")
        return page_html

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the browser window
        driver.quit()


if __name__ == '__main__':
    user_case_type = "W.P.(C)"
    user_case_number = "4352"
    user_case_year = "2025"
    data = {
        "case_type": user_case_type,
        "case_number": user_case_number,
        "case_year": user_case_year,
        
    }
    result_html = submit_case_search(user_case_type, user_case_number, user_case_year)

    if result_html:
        print("Next step: Parse the returned HTML.")
        
    # Parse the HTML and extract data column-wise
    soup = BeautifulSoup(result_html, 'html.parser')
    target_elements = soup.find_all(class_="dt-layout-row dt-layout-table")

    if target_elements:
        for element in target_elements:
            tbody = element.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    columns = row.find_all(['td', 'th'])
                    column_data = []
                    for column in columns:
                        column_data.append(column)
                    
    column_data = column_data[1::]
    col1 = column_data[0]
    col1 = str(col1).split("<br/>")[1::]
    

    if len(col1) > 0:
        text = col1[0]
        match = re.search(r'\[([^\]]+)\]', text)
        if match:
            extracted_data = match.group(1)
            print(f"Extracted status: {extracted_data}")
        else:
            print("No bracketed text found")
    
    # Extract link from col1[1]
    if len(col1) > 1:
        link_text = col1[1]

        
        # Try to extract href using regex
        link_match = re.search(r'href="([^"]*)"', link_text)
        if link_match:
            extracted_link = link_match.group(1)
            print(f"Extracted link: {extracted_link}")
        else:
            # Try alternative patterns
            link_match = re.search(r'href=["\']([^"\']*)["\']', link_text)
            if link_match:
                extracted_link = link_match.group(1)
                print(f"Extracted link (alt pattern): {extracted_link}")
            else:
                print("No link found in col1[1]")
                print(f"Full content: {link_text}")
    else:
        print("col1[1] not available")
    

