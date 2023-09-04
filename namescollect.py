import requests
import tools

from bs4 import BeautifulSoup

from lxml import html

def cpu(url):

    response = tools.grab(url)

    # Parse the content using lxml
    tree = html.fromstring(response.content)

    # Extract the table using the provided XPath
    table = tree.xpath('//*[@id="cputable"]')

    # Print the table
    s = html.tostring(table[0]).decode()
    return s 

def parse_cpu_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the table with the id 'cputable'
    table = soup.find('table', {'id': 'cputable'})
    
    # Extract the rows from the table body
    rows = table.tbody.find_all('tr')
    
    data = []
    for row in rows:
        columns = row.find_all('td')
        
        # Extract the data from each column
        cpu_name = columns[0].a.text
        cpu_mark = columns[1].text
        rank = columns[2].text
        cpu_value = columns[3].text
        price = columns[4].text
        
        # Append the data to the list
        data.append({
            'CPU Name': cpu_name,
            'CPU Mark': cpu_mark,
            'Rank': rank,
            'CPU Value': cpu_value,
            'Price': price
        })
    
    return data

savename = 'CPU Names'
html = tools.grab('https://www.cpubenchmark.net/cpu_list.php', savename)
parsed_data = parse_cpu_table(html)
print(parsed_data[:10])
