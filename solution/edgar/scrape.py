import json
import collections
import requests
from bs4 import BeautifulSoup


def fetch_url(url):
    """Retrieve supplied URL and return response object."""
    r = requests.get(url)
    return r


def main():
    """Scrapes company information from a demo Flask application."""

    # Set base URL.
    BASE_URL = 'http://127.0.0.1:5000'

    # Initialize a list. It will hold tuples of company_id, company_page_url
    # parsed from each of the site's 10 listing pages.
    id_url_list = []

    # Retrieve all 10 listing pages and compile a list of company id's and
    # detail page URLs.
    for page_number in range(1, 11):  # We know the number of pages.
        page_html = fetch_url(BASE_URL +
                              '/companies/?page=' + str(page_number))
        page_html_soup = BeautifulSoup(page_html.text, 'html.parser')
        page_table = page_html_soup.find('table')

        # From each row in the listing table, retrieve the company ID and
        # detail page URL. Append these to id_url_list as a tuple.
        for row in page_table.find_all('tr')[1:]:
            col = row.find_all('td')
            company_id = col[0].string
            company_page_url = col[1].find('a').get('href')

            id_url_list.append((company_id, company_page_url))

    # Initialize a list to hold one dictionary per company.
    output_list = []

    # Iterate through the list of company ID's and detail page URLs. For each,
    # fetch the detail page and find the table.
    for company in id_url_list:
        company_html = fetch_url(BASE_URL + company[1])
        company_html_soup = BeautifulSoup(company_html.text, 'html.parser')
        company_table = company_html_soup.find('table')

        # Build an ordered dictionary and make the first element the
        # company ID.
        d = collections.OrderedDict()
        d['id'] = company[0]

        # Iterate through the company detail table and turn each <td> element
        # pair into a key/value pair in the ordered dictionary.
        for row in company_table.find_all('tr'):
            col = row.find_all('td')
            key = col[1].get('id')
            value = col[1].contents[0]
            d[key] = value

        # Append the ordered dictionary to the output list.
        output_list.append(d)

    # Convert the output_list to json and write it to a file.
    j = json.dumps(output_list)
    with open('edgar.json', 'w') as file:
        file.write(j)


if __name__ == '__main__':
    main()
