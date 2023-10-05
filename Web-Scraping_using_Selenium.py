from selenium import webdriver
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

website = 'https://www.bema.co.uk/partners/'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(website)

while True:
    buttons = driver.find_elements(By.CLASS_NAME, "btn-swatpro.btn-red-outline.float-left.mr-3")
    csv_file_path = 'selenium.csv'
    data_list = []

    for button in buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()

            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "item.redactor-wrapper.relative"))
            # )

            # element = driver.find_element(By.CLASS_NAME, "item.redactor-wrapper.relative")

            company_name = driver.find_element(By.CLASS_NAME, "partners-feed_page-partner-logo").text

            img_element = driver.find_element(By.XPATH, "//div[@class='partners-feed_page-partner-logo']/img")

            logo = img_element.get_attribute("src")

            address_element = driver.find_element(By.XPATH,
                                                  "//div[@class='col-12 col-sm-6']/address")

            address_text = address_element.text

            a_elements = driver.find_elements(By.XPATH,
                                              "//div[@class='col-12 col-sm-6']/address/a")

            telephone = ""
            mail = ""
            cnt = 0
            for a_element in a_elements:
                if cnt == 0:
                    telephone = a_element.text
                elif cnt == 1:
                    mail = a_element.text
                cnt = cnt + 1

            element = driver.find_element(By.CLASS_NAME, "btn-swatpro")

            website = element.get_attribute("href")

            parent_element = driver.find_element(By.CLASS_NAME, "col-12.col-md-8")

            child_elements = parent_element.find_elements(By.XPATH, "./*")

            extracted_text = []
            description=""
            excluded_classes = ["partners-feed_page-partner-logo", "partners-feed_page-partner-meta",
                                "partners-feed_page-partner-contact"]
            for child_element in child_elements:
                class_attribute = child_element.get_attribute("class")
                if all(excluded_class not in class_attribute for excluded_class in excluded_classes):
                    extracted_text.append(child_element.text)

            description = "\n".join(extracted_text)

            if not extracted_text:
                # Locate the <h1> element by its class name
                h1_element = driver.find_element(By.CLASS_NAME, "partners-feed_page-partner-logo")

                # Use JavaScript to extract the text after the <h1> element
                script = "return arguments[0].nextSibling.textContent.trim();"
                text_after_h1 = driver.execute_script(script, h1_element)

                description=text_after_h1


            print(website)
            data_list.append({
                'company_name': company_name,
                'website': website,
                'address_text': address_text,
                'telephone': telephone,
                'mail': mail,
                'logo': logo,
                'description': description,

            })

        except StaleElementReferenceException:
            continue
        except ElementClickInterceptedException:
            continue
        driver.execute_script("window.history.go(-1)")

    with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        fieldnames = ['company_name', 'website', 'address_text', 'telephone', 'mail', 'logo',
                      'description']  # Column names
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write data rows
        for row in data_list:
            writer.writerow(row)

    print(f'CSV file "{csv_file_path}" has been created successfully.')
    driver.quit()
