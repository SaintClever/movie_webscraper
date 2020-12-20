from bs4 import BeautifulSoup
import requests, pandas



'''Request site'''
user_input = input('Movie request: ').replace(' ', '-')
url = requests.get('https://www2.musichq.net/search/' + user_input)
url_content = url.content
parse_content = BeautifulSoup(url_content, 'html.parser')
# print(parse_content)




'''Pages'''
# url = 'https://www2.musichq.net/search/' + user_input + '?page={}'
# print(url)

pages = parse_content.find_all('a', {'class': 'page-link'})
# print(pages)

page_list = []
for page in pages:
  pagination = {}
  pagination['Pages'] = page
  # print(page)

  page_list.append(pagination)
  
print(page_list[:int(len(page_list) / 2)])
pages_list = page_list[:int(len(page_list) / 2)]




'''Posters'''
posters = parse_content.find_all('div', {'class':'flw-item'})
# print(posters)

# quality, poster, title, year, length, tv/movie
movies_list = []
for poster in posters:
  data = {}

  data['Poster'] = '<img src="' + poster.find_all('img', {'class':'film-poster-img'})[0]['data-src'] + '" width="50%">'
  
  title = poster.find_all('h2', {'class':'film-name'})[0].text.strip()
  data['Title'] = '<a href="https://www2.musichq.net/' + poster.find_all('a')[0]['href'] + '" target="_blank">' + title + '</a>'
  # print(data)

  poster_type = poster.find_all('span', {'class':'fdi-type'})[0].text.strip()
  data['Movie / TV'] = poster_type

  year_and_duration = poster.find_all('span', {'class':'fdi-item'})
  data['Year'] = year_and_duration[0].text.strip()
  data['Duration'] = year_and_duration[1].text.strip()

  movies_list.append(data)




'''Create HTML and CSV'''
try:
  pages_df = pandas.Series(pages_list, index=['Poster', 'Title', 'Movie / TV', 'Year', 'Duration'])
  # print(pages_df)
  movies_df = pandas.DataFrame(movies_list)
  result = movies_df.append(pages_df, ignore_index=True)
  result.to_html('movies.html', escape=False)
except:
  # print(movies_list)
  movies_df = pandas.DataFrame(movies_list)
  movies_df.to_html('movies.html', escape=False)
  movies_df.to_csv('movies.csv')