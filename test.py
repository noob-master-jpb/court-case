from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.firefox.options import Options


def submit_case_search(case_type: str, case_number: str, year: str):
    
    _options = Options()
    _options.add_argument("--headless")
    try:
        driver = webdriver.Firefox(options=_options)
    except Exception as e:
        try:
            driver = webdriver.Chrome(options=_options)
        except Exception as e:
            print(f"Error initializing the browser: {e}")
            return None
        
        
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

        case_type_element.send_keys(case_type)
        case_number_element.send_keys(case_number)
        case_year_element.send_keys(year)
        captcha_input_element.send_keys(captcha_text)  

        submit_button_element.click()


        print("Waiting for results to load...")
        time.sleep(2) 

        page_html = driver.page_source
        print("Results page loaded successfully.")
        return page_html

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the browser window
        driver.quit()

def submit_order_search(url: str):
    _options = Options()
    _options.add_argument("--headless")
    try:
        driver = webdriver.Firefox(options=_options)
    except Exception as e:
        try:
            driver = webdriver.Chrome(options=_options)
        except Exception as e:
            print(f"Error initializing the browser: {e}")
            return None
    driver.get(url)
    try:
        page_html = driver.page_source
        print("Results page loaded successfully.")
        
        return page_html
    except Exception as e:
        print(f"An error occurred while fetching order data: {e}")
        return None
    finally:
        driver.quit()
    
def order_extractor(user_case_type, user_case_number, user_case_year):
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

    col1 = column_data[0].find_all(['a','font'])[1::]
    if col1:
        data["status"] = col1[0].text.strip()[1:-1]  
        if len(col1) > 1:
            data["order_link"] = col1[1].get('href', '').strip()
        else:
            data["order_link"] = None
    else:
        data["status"] = None
        data["order_link"] = None

    
    col2 = column_data[1]
    data["petitioner"] = col2.text.split("VS.")[0].strip()
    data["respondent"] = col2.text.split("VS.")[1].strip()

    
    col3 = str(column_data[2])
    next_date = col3.split("<br/>")[0].strip("</td> \t \n").split(":")
    if next_date[1].strip() == "NA":
        data[next_date[0].strip()] = None
    else:
        data[next_date[0].strip()] = next_date[1].strip()
    try:
        temp1 = col3.split("<br/>")[1].strip("</td> \t \n").split(":")
        data[temp1[0].strip()] = temp1[1].strip()
    except:
        pass
    try:
        temp2 = col3.split("<br/>")[2].strip("</td> \t \n").split(":")
        data[temp2[0].strip()] = temp2[1].strip()
    except:
        pass
    
    order_data = []
    
    soup = BeautifulSoup(submit_order_search(data["order_link"]), 'html.parser')
    target_elements = soup.find_all(id="caseTable")
    if target_elements:
        tbody = target_elements[0].find('tbody')
    orders = tbody.find_all('tr')
    for i in orders:
        temp = {}
        cells = i.find_all('td')
        temp["link"] = cells[1].find_all('a')[0].get('href')
        temp["date"] = cells[2].text
        order_data.append(temp)
    data["orders"] = order_data
    return data

if __name__ == "__main__":
    user_case_type = "W.P.(C)"
    user_case_number = "4352"
    user_case_year = "2025"
    
    result = order_extractor(user_case_type, user_case_number, user_case_year)
    print(result)