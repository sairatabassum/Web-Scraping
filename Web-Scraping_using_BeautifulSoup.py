import re
import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.bema.co.uk/partners/"
r1 = requests.get(url)
soup1 = BeautifulSoup(r1.content, 'html.parser')
companies = soup1.find_all('div', {"class": "partners-feed__inner-buttons"})

companies_list = []
data_list = []
csv_file_path = 'output-3.csv'

for company in companies:
    a_element = company.find('a')
    url = a_element.get('href')
    r1 = requests.get(url)
    print(url)
    soup1 = BeautifulSoup(r1.content, 'html.parser')
    name = soup1.find("h1", {"class": "partners-feed_page-partner-logo"}).text.strip()
    website_logo = soup1.find('div', {"class": "partners-feed_page-partner-logo"})
    img_element = website_logo.find('img')
    img = "https://www.bema.co.uk" + img_element.get('src')

    website_logo = soup1.find('div', {"class": "partners-feed_page-partner-contact"})

    a_element = website_logo.find('a')
    website = a_element.get('href')
    address_telephone = soup1.find("div", {"class": "partners-feed_page-partner-meta"})
    addresses = address_telephone.find("address")
    address = addresses.text.strip()
    telephone = address_telephone.find('a').text.strip()
    # print(address_telephone)

    # Find the <a> element with the "mailto" href attribute
    specific_a_element = address_telephone.find('a', href=lambda x: x and x.startswith("mailto:"))
    email = ""

    # Extract and print the text of the specific <a> element
    if specific_a_element:
        email = specific_a_element.text.strip()
        print(email)

    soup = soup1.find("div", {"class": "col-md-8"})
    descriptions = soup.find_all(['h1', 'div', 'p'],
                                 class_=["partners-feed_page-partner-meta", "partners-feed_page-partner-contact"])

    for element in descriptions:
        element.extract()
        # print(element)

    description = soup.get_text(strip=True)

    # Print the extracted text
    # print(description)

    # print(descriptions)
    # description = ""
    # if descriptions.find('p'):
    #     description_all = descriptions.find_all("p")
    #     for d in description_all:
    #         description += d.text.strip()
    #
    # else:
    #     article = soup1.find('article', class_='partners-feed_page')
    #     h1_element = article.find('h1', class_='partners-feed_page-partner-logo')
    #
    #     if h1_element:
    #         text_after_h1 = h1_element.find_next_sibling(text=True)
    #
    #         if text_after_h1:
    #             description=text_after_h1.strip()
    #
    #         else:
    #             description=""
    # print(description)
    data_list.append({
        'name': name,
        'website': website,
        'address': address,
        'telephone': telephone,
        'email': email,
        'img': img,
        'description': description,

    })

with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
    fieldnames = ['name', 'website', 'address', 'telephone', 'email', 'img', 'description']  # Column names
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write data rows
    for row in data_list:
        writer.writerow(row)

print(f'CSV file "{csv_file_path}" has been created successfully.')
