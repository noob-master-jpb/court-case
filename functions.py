import time
import os
import tempfile
from fpdf import FPDF
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

def get_chrome_driver():
    """Get Chrome driver optimized for Railway and Docker deployment"""
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    
    # Set binary location based on environment
    if os.getenv('RAILWAY_ENVIRONMENT'):
        # Railway with nixpacks
        chrome_options.binary_location = "/nix/store/*/bin/chromium"
    elif os.getenv('CHROME_BIN'):
        # Docker environment
        chrome_options.binary_location = os.getenv('CHROME_BIN')
    
    try:
        # Try to create the driver
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Chrome driver failed: {e}")
        # Fallback: try without binary location
        chrome_options.binary_location = None
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e2:
            print(f"Chrome driver fallback failed: {e2}")
            return None

def submit_case_search(case_type: str, case_number: str, year: str):
    driver = get_chrome_driver()
    if not driver:
        print("Failed to initialize browser driver")
        return None
        
    court_url = "https://delhihighcourt.nic.in/app/get-case-type-status"
    driver.get(court_url)

    try:
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
        driver.quit()

def submit_order_search(url: str):
    driver = get_chrome_driver()
    if not driver:
        print("Failed to initialize browser driver")
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
    

def get_filing_date(case_type: str, case_number: str, year: str):
    driver = get_chrome_driver()
    if not driver:
        print("Failed to initialize browser driver")
        return None

    court_url = "https://dhcmisc.nic.in/pcase/guiCaseWise.php"
    driver.get(court_url)

    try:
        case_type_element = driver.find_element(By.ID, 'ctype')
        case_number_element = driver.find_element(By.ID, 'regno')
        case_year_element = driver.find_element(By.ID, 'regyr')
        submit_button_element = driver.find_element(By.NAME, 'Submit')
        captcha_code_element = driver.find_element(By.ID, 'cap')
        captcha_input_element = driver.find_element(By.NAME, 'captcha_code')
        
        captcha_text = captcha_code_element.text
        case_type_element.send_keys(case_type)
        case_number_element.send_keys(case_number)
        case_year_element.send_keys(year)
        captcha_input_element.send_keys(captcha_text)  
        submit_button_element.click()


        print("Waiting for results to load...")
        time.sleep(5) 

        page_html = driver.page_source
        

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        
    try:
        html = BeautifulSoup(page_html, 'html.parser')
        target_elements = html.find(id="form3")
        data = target_elements.find('table')
        filing_date = data.find('tbody').find('tr').find_all('td')[-1].text.strip().split("-")
        date_map={
            'jan': '01',
            'feb': '02',
            'mar': '03',
            'apr': '04',
            'may': '05',
            'jun': '06',
            'jul': '07',
            'aug': '08',
            'sep': '09',
            'oct': '10',
            'nov': '11',
            'dec': '12'
        }
        try:
            filing_date[1] = date_map[filing_date[1].strip().lower()]
        except KeyError:
            print("Invalid month in date")
        return f"{filing_date[2]}/{filing_date[1]}/{filing_date[0]}"
    except Exception as e:
        print(f"An error occurred while parsing the filing date: {e}")
        return None
    
def order_extractor(user_case_type, user_case_number, user_case_year):
    data = {
        "case_type": user_case_type,
        "case_number": user_case_number,
        "case_year": user_case_year,
        
    }
    result_html = submit_case_search(user_case_type, user_case_number, user_case_year)


    if result_html:
        print("Next step: Parse the returned HTML.")
        
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
        data[next_date[0].strip().lower().replace(" ", "_")] = None
    else:
        data[next_date[0].strip().lower().replace(" ", "_")] = next_date[1].strip()
    try:
        temp1 = col3.split("<br/>")[1].strip("</td> \t \n").split(":")
        data[temp1[0].strip().lower().replace(" ", "_")] = temp1[1].strip()
    except:
        pass
    try:
        temp2 = col3.split("<br/>")[2].strip("</td> \t \n").split(":")
        data[temp2[0].strip().lower().replace(" ", "_")] = temp2[1].strip()
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
    data["filing_date"] = get_filing_date(user_case_type, user_case_number, user_case_year)
    return data


def get_pdf_filename(pdf_data):
    """Generate a safe filename for the PDF"""
    safe_case_type = pdf_data['case_type'].replace("(", "").replace(")", "").replace("/", "_")
    return f"{safe_case_type}_{pdf_data['case_number']}_{pdf_data['case_year']}.pdf"


def pdf_generator(pdf_data, save_to_disk=True):
    if not pdf_data:
        print("No data available to generate PDF.")
        return None
    
    pdf = FPDF()
    pdf.add_page()
    

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 12, 'DELHI HIGH COURT', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"{pdf_data['case_type']} {pdf_data['case_number']}/{pdf_data['case_year']}", 0, 1, 'C')
    pdf.ln(10)
    

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'CASE INFORMATION', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    

    pdf.set_font('Arial', '', 10)
    case_info = [
        ("Case Type:", pdf_data['case_type']),
        ("Case Number:", pdf_data['case_number']),
        ("Year:", pdf_data['case_year']),
        ("Status:", pdf_data['status']),
        ("Filing Date:", pdf_data.get('filing_date', 'N/A')),
        ("Next Date:", pdf_data.get('next_date', 'N/A')),
        ("Hearing Date:", pdf_data.get('hearing_date', 'N/A'))
    ]
    
    for label, value in case_info:
        pdf.cell(50, 6, label, 0, 0, 'L')
        pdf.cell(0, 6, str(value), 0, 1, 'L')
    
    pdf.ln(8)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'PARTIES', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(50, 6, 'Petitioner:', 0, 0, 'L')
    pdf.multi_cell(0, 6, pdf_data['petitioner'])
    pdf.ln(2)
    
    pdf.cell(50, 6, 'Respondent:', 0, 0, 'L')
    pdf.multi_cell(0, 6, pdf_data['respondent'])
    pdf.ln(8)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'ORDERS & DOCUMENTS', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    if pdf_data['orders']:
        for idx, order in enumerate(pdf_data['orders'], 1):
            pdf.cell(15, 6, f"{idx}.", 0, 0, 'L')
            pdf.cell(30, 6, "Date:", 0, 0, 'L')
            pdf.cell(40, 6, order['date'], 0, 0, 'L')
            
            pdf.cell(20, 6, "Link:", 0, 0, 'L')
            
            link_text = "Click to view document"
            pdf.set_text_color(0, 0, 255)
            pdf.set_font('Arial', 'U', 10)
            pdf.cell(0, 6, link_text, 0, 1, 'L', link=order['link'])
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 10)
            
            pdf.set_font('Arial', '', 8)
            pdf.set_text_color(100, 100, 100)
            url_display = order['link'][:80] + ('...' if len(order['link']) > 80 else '')
            pdf.cell(65, 4, "", 0, 0, 'L')
            pdf.cell(0, 4, f"URL: {url_display}", 0, 1, 'L')
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.ln(3)
    else:
        pdf.cell(0, 6, 'No orders available', 0, 1, 'L')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 6, f'Generated on: {time.strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')

    if save_to_disk:
        temp_dir = os.path.join(tempfile.gettempdir(), 'court_case_pdfs')
        os.makedirs(temp_dir, exist_ok=True)
        
        filename = get_pdf_filename(pdf_data)
        file_path = os.path.join(temp_dir, filename)
        
        pdf.output(file_path)
        print(f"PDF saved to: {file_path}")
        return file_path
    else:
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        return pdf_bytes


if __name__ == "__main__":
    case_type = "W.P.(C)"
    case_number = "4352"
    year = "2025"
    pdf_data =  order_extractor(case_type, case_number, year)
    pdf_file = pdf_generator(pdf_data)
    if pdf_file:
        print(f"PDF generated successfully: {pdf_file}")