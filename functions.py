# In your Django app's scraping_function.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from .models import Scrape_Vogue, Scrape_Trends_Tagwalk, Scrape_M_W_Fashion_Acc_Tagwalk, URL_Vogue, URL_Trends_TagWalk, URL_Acc_TagWalk, URL_M_W_TagWalk
import requests
from django.db.models import Q
from django.utils import timezone
from urllib.parse import urlparse, parse_qs
import json
import time as time_module
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from django.conf import settings


# def extract_trends_urls_from_tagwalk():
#     types = ['woman', 'man']
#     base_url = "https://www.tag-walk.com/en/trends"
#     data_filtered_by_trend = []
#     for type in types:
#         url = str(base_url + '/' + type + '/fall-winter-2024')
#         print('url: ', url)
#         # Configure Selenium webdriver
#         options = webdriver.ChromeOptions()
#         # Run Chrome in headless mode (without opening browser window)
#         options.add_argument('--headless')
#         driver = webdriver.Chrome(options=options)
#         driver.get(url)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         seasons = []
#         season_slider_container = soup.find('div', class_="season-slider")
#         season_slider_links = season_slider_container.find_all('a')
#         season_names = season_slider_container.find_all('div')
#         for i in range(len(season_slider_links)):
#             d = {
#                 'name': season_names[i].text,
#                 'link': season_slider_links[i].get('href')
#             }
#             seasons.append(d)
#         # print(seasons)

#         trends = []
#         for season in seasons:
#             url = "https://www.tag-walk.com"+season['link']
#             print('season url: ', url)
#             response = requests.get(url)
#             soup = BeautifulSoup(response.text, "html.parser")
#             trends_list = soup.find('div', class_='trends-list')
#             trends_links = trends_list.find_all('a')
#             trend_cards = trends_list.find_all('div', class_='trend-card')
#             for i in range(len(trends_links)):
#                 d = {
#                     'trend_name': trend_cards[i].find('h3').text,
#                     'season_name': season['name'],
#                     'link': trends_links[i].get('href')
#                 }
#                 trends.append(d)

#             # print(len(trends))

#             for trend in trends:
#                 print(trend['link'])
#                 url = "https://www.tag-walk.com" + trend['link']
#                 print("url trends: ", url)
#                 driver.get(url)
#                 soup = BeautifulSoup(driver.page_source, 'html.parser')
#                 photo_list = soup.find('div', id="results")
#                 photo_links = photo_list.find_all('a')
#                 for photo_link in photo_links:
#                     designer = photo_link.find_all(
#                         'p', class_='photo-list-item-link-details-designer')[0].text
#                     d = {
#                         'type': 'Menswear' if type == 'man' else 'Womenswear',
#                         'season_name': trend['season_name'],
#                         'trend_name': trend['trend_name'],
#                         'designer_name': designer,
#                         'url': url
#                     }
#                 existing_event = URL_Trends_TagWalk.objects.filter(
#                     Q(type=d['type']) &
#                     Q(season=d['season_name']) &
#                     Q(trend=d['trend_name']) &
#                     Q(designer=d['designer_name'])
#                 ).exists()

#                 print("existing url: ", existing_event)

#                 if not existing_event:
#                     # Save the data into the Scrape_Vogue model
#                     URL_Trends_TagWalk.objects.create(
#                         type=d['type'],
#                         season=d['season_name'],
#                         designer=d['designer_name'],
#                         trend=d['trend_name'],
#                         url=d['url'],
#                     )

#     return data_filtered_by_trend


def extract_trends_urls_from_tagwalk():
    types = ['woman', 'man']
    base_url = "https://www.tag-walk.com/en/trends"
    data_filtered_by_trend = []

    for type in types:
        url = str(base_url + '/' + type + '/fall-winter-2024')
        print('url from new scrapper: ', url)

        # Configure Selenium webdriver options
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')

        service = Service(settings.CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        seasons = []
        season_slider_container = soup.find('div', class_="season-slider")
        season_slider_links = season_slider_container.find_all('a')
        season_names = season_slider_container.find_all('div')
        for i in range(len(season_slider_links)):
            d = {
                'name': season_names[i].text,
                'link': season_slider_links[i].get('href')
            }
            seasons.append(d)
        # print(seasons)

        trends = []
        for season in seasons:
            url = "https://www.tag-walk.com"+season['link']
            print('season url: ', url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            trends_list = soup.find('div', class_='trends-list')
            trends_links = trends_list.find_all('a')
            trend_cards = trends_list.find_all('div', class_='trend-card')
            for i in range(len(trends_links)):
                d = {
                    'trend_name': trend_cards[i].find('h3').text,
                    'season_name': season['name'],
                    'link': trends_links[i].get('href')
                }
                trends.append(d)

            # print(len(trends))

            for trend in trends:
                print(trend['link'])
                url = "https://www.tag-walk.com" + trend['link']
                print("url trends: ", url)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                photo_list = soup.find('div', id="results")
                photo_links = photo_list.find_all('a')
                for photo_link in photo_links:
                    designer = photo_link.find_all(
                        'p', class_='photo-list-item-link-details-designer')[0].text
                    d = {
                        'type': 'Menswear' if type == 'man' else 'Womenswear',
                        'season_name': trend['season_name'].strip(),
                        'trend_name': trend['trend_name'].strip(),
                        'designer_name': designer.strip(),
                        'url': url
                    }

                    print("data from rends tagwalk url scraper: ", d)

                existing_event = URL_Trends_TagWalk.objects.filter(
                    Q(type=d['type']) &
                    Q(season=d['season_name']) &
                    Q(trend=d['trend_name']) &
                    Q(designer=d['designer_name'])
                ).exists()

                print("existing url: ", existing_event)

                if not existing_event:
                    # Save the data into the Scrape_Vogue model
                    URL_Trends_TagWalk.objects.create(
                        type=d['type'],
                        season=d['season_name'],
                        designer=d['designer_name'],
                        trend=d['trend_name'],
                        url=d['url'],
                    )

    return data_filtered_by_trend


# def extract_trends_from_tagwalk():
#     types = ['woman', 'man']
#     base_url = "https://www.tag-walk.com/en/trends"
#     data_filtered_by_trend = []
#     for type in types:
#         url = str(base_url + '/' + type + '/fall-winter-2024')
#         # print('url: ', url)
#         # # Configure Selenium webdriver
#         # options = webdriver.ChromeOptions()
#         # # Run Chrome in headless mode (without opening browser window)
#         # options.add_argument('--headless')
#         # driver = webdriver.Chrome(options=options)
#         # driver.get(url)

#         # Configure Selenium webdriver options
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--disable-gpu')
#         options.add_argument('--window-size=1920x1080')

#         service = Service(settings.CHROMEDRIVER_PATH)
#         driver = webdriver.Chrome(service=service, options=options)
#         driver.get(url)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         seasons = []
#         season_slider_container = soup.find('div', class_="season-slider")
#         season_slider_links = season_slider_container.find_all('a')
#         season_names = season_slider_container.find_all('div')
#         for i in range(len(season_slider_links)):
#             d = {
#                 'name': season_names[i].text,
#                 'link': season_slider_links[i].get('href')
#             }
#             seasons.append(d)
#         # print(seasons)

#         trends = []
#         for season in seasons:
#             url = "https://www.tag-walk.com"+season['link']
#             print('season url: ', url)
#             response = requests.get(url)
#             soup = BeautifulSoup(response.text, "html.parser")
#             trends_list = soup.find('div', class_='trends-list')
#             trends_links = trends_list.find_all('a')
#             trend_cards = trends_list.find_all('div', class_='trend-card')
#             for i in range(len(trends_links)):
#                 d = {
#                     'trend_name': trend_cards[i].find('h3').text,
#                     'season_name': season['name'],
#                     'link': trends_links[i].get('href')
#                 }
#                 trends.append(d)

#             # print(len(trends))

#             for trend in trends:
#                 print(trend['link'])
#                 url = "https://www.tag-walk.com" + trend['link']
#                 print("url trends: ", url)

#                 driver.get(url)
#                 soup = BeautifulSoup(driver.page_source, 'html.parser')
#                 photo_list = soup.find('div', id="results")
#                 photo_links = photo_list.find_all('a')
#                 for photo_link in photo_links:
#                     designer = photo_link.find_all(
#                         'p', class_='photo-list-item-link-details-designer')[0].text
                    
#                     try:
#                         trend_status = URL_Trends_TagWalk.objects.get(
#                             type='Menswear' if type == 'man' else 'Womenswear',
#                             season=trend['season_name'],
#                             designer=designer
#                         )
#                         if (trend_status.status == "completed"):
#                             continue
#                     except URL_Trends_TagWalk.DoesNotExist:
#                         print("scrape urls first")
#                         continue
#                     except Exception as e:
#                         print("an error occured: ", str(e))
#                         continue

#                     sources = photo_link.find_all('source')
#                     images = []
#                     for source in sources:
#                         srcset = source.get('srcset')
#                         if srcset:
#                             images.append(srcset)
#                     d = {
#                         'type': 'Menswear' if type == 'man' else 'Womenswear',
#                         'season_name': trend['season_name'].strip(),
#                         'trend_name': trend['trend_name'].strip(),
#                         'designer_name': designer.strip(),
#                         'images': images
#                     }
#                     data_filtered_by_trend.append(d)
#                     print(d)
#                     existing_event = Scrape_Trends_Tagwalk.objects.filter(
#                         Q(type=d['type']) &
#                         Q(season=d['season_name']) &
#                         Q(designer=d['designer_name']) & Q(trend=d['trend_name']) 
#                     ).exists()

#                 print("existing event: ", existing_event)

#                 if not existing_event:
#                     # Save the data into the Scrape_Vogue model
#                     Scrape_Trends_Tagwalk.objects.create(
#                         type=d['type'],
#                         season=d['season_name'],
#                         trend=d['trend_name'],
#                         designer=d['designer_name'],
#                         collections=d['images'],
#                     )
                
#                 # Update the accessoriesStatus entry
#                     try:
#                         trends_status = URL_Trends_TagWalk.objects.get(
#                             type=d['type'],
#                             season=d['season_name'],
#                             trend=d['trend_name']
#                         )
#                         trends_status.status = 'completed'
#                         trends_status.scraped_at = timezone.now()
#                         trends_status.error_message = ''
#                         trends_status.attempts = 1
#                         trends_status.save()
#                     except URL_Trends_TagWalk.DoesNotExist:
#                         print(
#                             f'trends entry not found for season: , designer: ')


#     return data_filtered_by_trend


def extract_trends_from_tagwalk():
    types = ['woman', 'man']
    base_url = "https://www.tag-walk.com/en/trends"
    data_filtered_by_trend = []

    # Configure Selenium webdriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    service = Service(settings.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for type in types:
            url = f"{base_url}/{type}/fall-winter-2024"
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            seasons = []
            season_slider_container = soup.find('div', class_="season-slider")
            if season_slider_container:
                season_slider_links = season_slider_container.find_all('a')
                season_names = season_slider_container.find_all('div')
                for i in range(len(season_slider_links)):
                    season_name = season_names[i].text.strip()
                    season_link = season_slider_links[i].get('href')
                    seasons.append({'name': season_name, 'link': season_link})

            trends = []
            for season in seasons:
                url = f"https://www.tag-walk.com{season['link']}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                trends_list = soup.find('div', class_='trends-list')
                if trends_list:
                    trends_links = trends_list.find_all('a')
                    trend_cards = trends_list.find_all(
                        'div', class_='trend-card')
                    for i in range(len(trends_links)):
                        trend_name = trend_cards[i].find('h3').text.strip()
                        trend_link = trends_links[i].get('href')
                        trends.append(
                            {'trend_name': trend_name, 'season_name': season['name'], 'link': trend_link})

            for trend in trends:
                url = f"https://www.tag-walk.com{trend['link']}"
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                photo_list = soup.find('div', id="results")
                if photo_list:
                    photo_links = photo_list.find_all('a')
                    for photo_link in photo_links:
                        designer = photo_link.find(
                            'p', class_='photo-list-item-link-details-designer').text.strip()
                        images = [source.get('srcset') for source in photo_link.find_all(
                            'source') if source.get('srcset')]

                        trend_statuses = URL_Trends_TagWalk.objects.filter(
                            type='Menswear' if type == 'man' else 'Womenswear',
                            season=trend['season_name'],
                            designer=designer
                        )

                        for trend_status in trend_statuses:
                            if trend_status.status == "completed":
                                continue
                            # Process each matching trend_status object
                            data = {
                                'type': 'Menswear' if type == 'man' else 'Womenswear',
                                'season_name': trend['season_name'],
                                'trend_name': trend['trend_name'],
                                'designer_name': designer,
                                'images': images
                            }
                            data_filtered_by_trend.append(data)

                            existing_event = Scrape_Trends_Tagwalk.objects.filter(
                                Q(type=data['type']) &
                                Q(season=data['season_name']) &
                                Q(designer=data['designer_name']) &
                                Q(trend=data['trend_name'])
                            ).exists()

                            if not existing_event:
                                Scrape_Trends_Tagwalk.objects.create(
                                    type=data['type'],
                                    season=data['season_name'],
                                    trend=data['trend_name'],
                                    designer=data['designer_name'],
                                    collections=data['images'],
                                )

                            try:
                                trend_status.status = 'completed'
                                trend_status.scraped_at = timezone.now()
                                trend_status.error_message = ''
                                trend_status.attempts = 1
                                trend_status.save()
                            except Exception as e:
                                print(
                                    f"An error occurred while updating URL_Trends_TagWalk: {str(e)}")

    except Exception as e:
        print(f"An error occurred during data extraction: {str(e)}")
    finally:
        driver.quit()

    return data_filtered_by_trend

def scrape_accessories_urls_from_tagwalk():
    types = ['accessory-man', 'couture','accessory']
    base_url = "https://www.tag-walk.com"
    for type in types:
        url = str(base_url + '/en/collection/search?type=' + type)
        # to tackle pagination
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                photo_cards = soup.find_all('div', class_='photo-card')
                for photo_card in photo_cards:
                    photo_card_link = photo_card.find(
                        'a', class_='photo-card-link')
                    temp_url = str(base_url + photo_card_link['href'])
                    # Parse the URL
                    parsed_url = urlparse(temp_url)
                    # Extract type, season, designer, and city parameters
                    query_params = parse_qs(parsed_url.query)
                    type_value = query_params['type'][0]
                    season_value = query_params['season'][0]
                    designer_value = query_params['designer'][0]
                    data = {
                        'type': 'accessory-women' if type_value == 'accessory' else type_value,
                        'season': season_value.replace('-', ' '),
                        'url': temp_url,
                        'designer': designer_value.replace('-', ' '),
                    }
                    existing_event = URL_Acc_TagWalk.objects.filter(
                        Q(type=data['type']) &
                        Q(season=data['season']) &
                        Q(designer=data['designer'])
                    ).exists()

                    print("existing url: ", existing_event)

                    if not existing_event:
                        # Save the data into the Scrape_Vogue model
                        URL_Acc_TagWalk.objects.create(
                            type=data['type'],
                            season=data['season'],
                            designer=data['designer'],
                            url=data['url'],
                        )
                
                next_links = soup.find_all(
                    'a', class_='pagination-list-item-link')
                next_links.reverse()
                # print(next_links)
                endpoint = None
                for link in next_links:
                    if link.text.strip() == 'Next':
                        print("text: ", link.text)
                        endpoint = link['href']
                        break
                if endpoint:
                    url = str(base_url + endpoint)
                    print("url: ", url)
                else:
                    print("no more endpoints")
                    break

            else:
                print("not 200")
        print('type from accessories urls: ', type)
    return {response: "Accessories urls scraped!!!"}

                    
def scrape_accessories_from_tagwalk():
    types = ['accessory-man', 'couture','accessory']
    base_url = "https://www.tag-walk.com"
    for type in types:
        url = str(base_url + '/en/collection/search?type=' + type)
        # to tackle pagination
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                photo_cards = soup.find_all('div', class_ = 'photo-card')
                for photo_card in photo_cards:
                    photo_card_link = photo_card.find('a', class_ = 'photo-card-link')
                    temp_url = str(base_url + photo_card_link['href'])
                    print("temp url: ", temp_url)
                    # Parse the URL
                    parsed_url = urlparse(temp_url)
                    # Extract type, season, designer, and city parameters
                    query_params = parse_qs(parsed_url.query)
                    type_value = query_params['type'][0] if 'type' in query_params and query_params['type'][0] else ''
                    season_value = query_params['season'][0] if 'season' in query_params and query_params['season'][0] else ''
                    designer_value = query_params['designer'][0] if 'designer' in query_params and query_params['designer'][0] else ''
                    city_value = query_params['city'][0] if 'city' in query_params and query_params['city'][0] else ''
                    data = {
                        'type': 'accessory-women' if type_value == 'accessory' else type_value,
                        'season': season_value.replace('-', ' '),
                        'city': city_value.replace('-', ' '),
                        'designer': designer_value.replace('-', ' '),
                    }
                    try: 
                        accessories_status = URL_Acc_TagWalk.objects.get(
                            type=data['type'],
                            season=data['season'],
                            designer=data['designer']
                        )
                        if (accessories_status.status == "completed"):
                            continue
                    
                    except URL_Acc_TagWalk.DoesNotExist:
                        print( f'URL_Acc_TagWalk entry not found for season: {data["season"]}, designer: {data["designer"]}')
                        continue
                    except Exception as e:
                        print(f'An error occurred while updating URL_Acc_TagWalk: {str(e)}')
                    
                    photo_response = requests.get(temp_url)
                    if photo_response.status_code == 200:
                        photo_soup = BeautifulSoup(photo_response.text, 'html.parser')
                        photo_list = photo_soup.find('div', class_ = 'photo-list', id = 'results')
                        print("photo list: " , photo_list)
                        images = photo_list.find_all('img', class_='photo-list-item-link-img')
                        print("images: ", images)
                        photos = []
                        for image in images:
                            image_url = image['src']
                            print("url: ", image_url)
                            photos.append(image_url)
                        data['collections'] = photos[1:]
                    
                    # Check if a FashionShow object with the same characteristics exists
                    existing_show = Scrape_M_W_Fashion_Acc_Tagwalk.objects.filter(
                        type=data['type'],
                        season=data['season'],
                        city=data['city'],
                        designer=data['designer']
                    ).exists()

                    print("existing_show: ", existing_show)
                    if not existing_show:
                        # Save the fashion show data into the database
                        Scrape_M_W_Fashion_Acc_Tagwalk.objects.create(**data)

                    # Update the accessoriesStatus entry
                    try:
                        accessories_status = URL_Acc_TagWalk.objects.get(
                            type=data['type'],
                            season=data['season'],
                            designer=data['designer']
                        )
                        accessories_status.status = 'completed'
                        accessories_status.scraped_at = timezone.now()
                        accessories_status.error_message = ''
                        accessories_status.attempts = 1
                        accessories_status.save()
                    except URL_Acc_TagWalk.DoesNotExist:
                        print(
                            f'accessory entry not found for season: , designer: ')

                next_links = soup.find_all(
                    'a', class_='pagination-list-item-link')
                next_links.reverse()
                # print(next_links)
                endpoint = None
                for link in next_links:
                    if link.text.strip() == 'Next':
                        print("text: ", link.text)
                        endpoint = link['href']
                        break
                if endpoint:
                    url = str(base_url + endpoint)
                    print("url: ", url)
                else:
                    print("no more endpoints")
                    break
            
            else: 
                print("not 200")
                # if next_link:
            #     url = url + next_link['href']  # Update URL for the next page
            # else:
            #     url = None  # No more pages

        print('typefrom accesories data: ', type)
    print("function executed !!!!")
    return {}


def scrape_men_women_tagwalk():
    types = ['man', 'woman']
    last_season_scrap = "pre-fall-2023"
    top_season = ""
    for type in types:
        url = f"https://www.tag-walk.com/en/live/{type}/fall-winter-2023?city=paris"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        s = soup.find(id='season')
        if s is None:
            continue
        else:
            seasons = soup.find(id='season').find_all('option')
            for season in seasons:
                current_season = season['value']
                print("Season: ", season)
                if current_season == "":
                    continue
                if current_season != last_season_scrap:
                    if top_season == "":
                        top_season = current_season
                    fashion_shows = extract_data_from_tagwalk(
                        current_season, type)
                else:
                    break
            last_season_scrap = top_season
            print(last_season_scrap, top_season, current_season)
    print("function executed !!!!")

    
def extract_data_from_tagwalk(season_temp, type):
    fashion_shows = []
    url = f"https://www.tag-walk.com/en/live/{type}/{season_temp}?city=paris"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        cities = soup.find(id='city').find_all('option')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return json.dumps(fashion_shows)
    except Exception as e:
        print(f"Error parsing HTML for city options: {e}")
        return json.dumps(fashion_shows)

    for cityy in cities:
        city_temp = cityy['value']
        if city_temp != "":
            city_url = f"https://www.tag-walk.com/en/live/{type}/{season_temp}?city={city_temp}"

            try:
                response = requests.get(city_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                designers = soup.find(id='designer').find_all('option')
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL {city_url}: {e}")
                continue
            except Exception as e:
                print(f"Error parsing HTML for designer options: {e}")
                continue

            for designer in designers:
                designer_temp = designer['value']
                if designer_temp != "":
                    designer_url = f"https://www.tag-walk.com/en/collection/{type}/{designer_temp}/{season_temp}"

                    designer_name = designer.text.strip()

                    try:
                        # Use filter instead of get for URL_M_W_TagWalk
                        tagwalk_statuses = URL_M_W_TagWalk.objects.filter(
                            type='Menswear' if type == 'man' else 'Womenswear',
                            season=season_temp,
                            designer=designer_name
                        )

                        for tagwalk_status in tagwalk_statuses:
                            if tagwalk_status.status == "completed":
                                continue

                            try:
                                response = requests.get(designer_url)
                                response.raise_for_status()
                                soup = BeautifulSoup(
                                    response.content, "html.parser")
                                images = []
                                for show in soup.find_all('div', {'class': 'photo-list-item'}):
                                    image = show.find('img')['src']
                                    if image == "/images/loader.gif":
                                        continue
                                    images.append(image)

                                collection = season_temp
                                city = cityy.text.strip()

                                show_data = {
                                    'type': 'Menswear' if type == 'man' else 'Womenswear',
                                    'season': collection,
                                    'city': city,
                                    'designer': designer_name,
                                    'collections': images
                                }

                                fashion_shows.append(show_data)

                                # Check and create Scrape_M_W_Fashion_Acc_Tagwalk
                                existing_show = Scrape_M_W_Fashion_Acc_Tagwalk.objects.filter(
                                    type=show_data['type'],
                                    season=show_data['season'],
                                    city=show_data['city'],
                                    designer=show_data['designer']
                                ).exists()

                                if not existing_show:
                                    Scrape_M_W_Fashion_Acc_Tagwalk.objects.create(
                                        **show_data)

                                # Update tagwalk_status
                                try:
                                    tagwalk_status.status = 'completed'
                                    tagwalk_status.scraped_at = timezone.now()
                                    tagwalk_status.error_message = ''
                                    tagwalk_status.attempts = 1
                                    tagwalk_status.save()
                                except Exception as e:
                                    print(
                                        f"An error occurred while updating URL_M_W_TagWalk: {str(e)}")

                            except requests.exceptions.RequestException as e:
                                print(
                                    f"Error fetching URL {designer_url}: {e}")
                            except Exception as e:
                                print(f"Error parsing HTML for images: {e}")

                    except Exception as e:
                        print(
                            f"Error fetching or updating URL_M_W_TagWalk: {str(e)}")

    return json.dumps(fashion_shows)

def scrape_complete_data_from_vogue():
    seasons = seasonScrapperVogue()
    print("seasons: ", seasons)
    dataBase = []
    for season in seasons:
        for obj in seasons[season]:
            url = str('https://www.vogue.com' + obj['link'])
            designersResponse = requests.get(url)
            soup = BeautifulSoup(designersResponse.text, 'html.parser')
            designers = soup.find_all('h3', class_='iMnJyD')
            d = []
            for designer in designers:
                d.append((designer.text).lower().replace(" ", "-"))
            print(d)
            for i in range(len(d)):
                try:
                    vogue_status = URL_Vogue.objects.get(
                        season=obj['name'],
                        designer=d[i]
                    )
                    if(vogue_status.status == "completed"):
                        continue
                except vogue_status.DoesNotExist:
                    print("scrape url for to scrape this page coming from vogue")
                    continue
                except Exception as e:
                    print("error occured while scraping: ", str(e))
                    continue

                data = scrape_images_from_website(obj['link'], d[i])

                # if 'error' in data:
                #     return data
                print("data: ", data)
                print('season : ', season)
                data['year'] = season
                data['season'] = obj['name']
                data['designer'] = d[i]

                print("data from scrape_complete_data: ", data)
                existing_event = Scrape_Vogue.objects.filter(
                    Q(year=data['year']) &
                    Q(season=data['season']) &
                    Q(designer=data['designer'])
                ).exists()

                print("existing event: ", existing_event)

                if not existing_event:
                    # Save the data into the Scrape_Vogue model
                    Scrape_Vogue.objects.create(
                        year=data['year'],
                        date=data['date'],
                        season=data['season'],
                        designer=data['designer'],
                        collections=data['images'],
                        details=data['details_images'],
                        beauty=data['beauty_images'],
                        write_up=data['experience'],
                        author=data['author']
                    )

                    # Update the URL_Vogue entry
                    try:
                        vogue_status = URL_Vogue.objects.get(
                            season=data['season'],
                            designer=data['designer']
                        )
                        vogue_status.status = 'completed'
                        vogue_status.scraped_at = timezone.now()
                        vogue_status.error_message = ''
                        vogue_status.attempts = 1
                        vogue_status.save()
                    except URL_Vogue.DoesNotExist:
                        print(
                            f'URL_Vogue entry not found for season: {data["season"]}, designer: {data["designer"]}')
                dataBase.append(data)

    return dataBase    # print(seasons)


def scrape_urls_from_vogue():
    seasons = seasonScrapperVogue()
    # print("seasons: ", seasons)
    print("alpha beta gamma updated in the server !!!!")
    dataBase = []
    for season in seasons:
        for obj in seasons[season]:
            url = str('https://www.vogue.com' + obj['link'])
            designersResponse = requests.get(url)
            soup = BeautifulSoup(designersResponse.text, 'html.parser')
            designers = soup.find_all('h3', class_='iMnJyD')
            d = []
            for designer in designers:
                d.append((designer.text).lower().replace(" ", "-"))
            print(d)
            for i in range(len(d)):
                url = str("https://www.vogue.com" +
                          obj['link'] + '/' + d[i])
                data = {
                    'season': obj['name'],
                    'designer': d[i],
                    'url': url,
                }
                existing_event = URL_Vogue.objects.filter(
                    Q(season=data['season']) &
                    Q(designer=data['designer'])
                ).exists()

                print("existing url: ", existing_event)

                if not existing_event:
                    # Save the data into the Scrape_Vogue model
                    URL_Vogue.objects.create(
                        season=data['season'],
                        designer=data['designer'],
                        url=data['url']
                    )

                    dataBase.append(data)

    return dataBase



# def scrape_images_from_website(season, designer):
#     # Replace with the URL of the website you want to scrape
#     # url = "https://www.vogue.com/fashion-shows/tokyo-fall-2024/shinyakozuka"
#     url = str("https://www.vogue.com" + season + '/' + designer)
#     # url = "https://www.vogue.com/fashion-shows/pre-fall-2024/bottega-veneta"
#     # url = "https://www.vogue.com/fashion-shows/spring-2012-ready-to-wear/d-g"  # gallery-beauty
#     print('url: ', url)
#     # Configure Selenium webdriver
#     options = webdriver.ChromeOptions()
#     # Run Chrome in headless mode (without opening browser window)
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)

#     # Click the "Load More" button 
#     selectors = ['.fkjdoS', '.oTJkH']
#     for selector in selectors:
#         try:
#             load_more_button = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, selector))
#             )
#             load_more_button.click()
#         except Exception as e:
#             print("Error clicking Load More button:", e)

    
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # Extract IMAGE COLLECTION
#     image_collection = []
#     collection_section = soup.find('section', id='gallery-collection')
#     id = 1
#     try: 
#         for img in collection_section.find_all('img'):
#             image_collection.append({
#                 'url': img.get('src'),
#                 'title': id
#             })
#             id += 1
#     except Exception as e:
#         print("Collections not present")


#     # EXTRACT IMAGE UNDER DETAILS SECTION
#     image_details = []
#     details_section = soup.find('section', id='gallery-detail')
#     if details_section:
#         id = 1
#         for img in details_section.find_all('img'):
#             image_details.append({
#                 'url': img.get('src'),
#                 'title': id
#             })
#             id += 1
#     else:
#         print("Details section not found or empty")

#     # EXTRACT IMAGE UNDER beauty SECTION
#     image_beauty = []
#     beauty_section = soup.find('section', id='gallery-beauty')
#     if beauty_section:
#         id = 1
#         for img in beauty_section.find_all('img'):
#             image_beauty.append({
#                 'url': img.get('src'),
#                 'title': id
#             })
#             id += 1
#     else:
#         print("beauty section not found or empty")


#     # THE FOLLOWING IS FOR THE WRITE UP
#     target_div = soup.find('div', class_='jtraPi')
#     experience = []
#     if target_div:
#         experience = target_div.find_all('p')
#     complete_experience = [p.text for p in experience]
#     time = soup.find('time')
#     by = (soup.find('a', class_='byline__name-link')).text if (soup.find('a', class_='byline__name-link')) else ' '
#     # data = {
#     #     'experience': complete_experience,
#     #     'images': image_collection,
#     #     'date': time.text if time else '',
#     #     'author': by
#     # }
#     data = {
#         'experience': complete_experience,
#         'images': image_collection,
#         'details_images': image_details,
#         'beauty_images': image_beauty,
#         'date': time.text if time else '',
#         'author': by
#     }
#     # Close the webdriver
#     driver.quit()

#     return data


def scrape_images_from_website(season, designer):
    url = f"https://www.vogue.com{season}/{designer}"
    print('url: ', url)

    # Configure Selenium webdriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    

    service = Service(settings.CHROMEDRIVER_PATH)

    temp_data = {
        'name': 'vogue', 
    }

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        temp_data['driver'] = 'entered try block'

        # Wait and click the "Load More" button if it exists
        selectors = ['.fkjdoS', '.oTJkH']
        for selector in selectors:
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                load_more_button.click()
                # Allow time for the page to load more content
                time_module.sleep(2)
            except Exception as e:
                print("Error clicking Load More button:", e)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract IMAGE COLLECTION
        image_collection = []
        collection_section = soup.find('section', id='gallery-collection')
        if collection_section:
            for id, img in enumerate(collection_section.find_all('img'), start=1):
                image_collection.append({
                    'url': img.get('src'),
                    'title': id
                })
        else:
            print("Collection section not found or empty")

        # Extract IMAGE UNDER DETAILS SECTION
        image_details = []
        details_section = soup.find('section', id='gallery-detail')
        if details_section:
            for id, img in enumerate(details_section.find_all('img'), start=1):
                image_details.append({
                    'url': img.get('src'),
                    'title': id
                })
        else:
            print("Details section not found or empty")

        # Extract IMAGE UNDER BEAUTY SECTION
        image_beauty = []
        beauty_section = soup.find('section', id='gallery-beauty')
        if beauty_section:
            for id, img in enumerate(beauty_section.find_all('img'), start=1):
                image_beauty.append({
                    'url': img.get('src'),
                    'title': id
                })
        else:
            print("Beauty section not found or empty")

        # Extract the write-up
        target_div = soup.find('div', class_='jtraPi')
        complete_experience = [
            p.text for p in target_div.find_all('p')] if target_div else []
        time = soup.find('time')
        by = soup.find('a', class_='byline__name-link')
        author = by.text if by else ''
        data = {
            'experience': complete_experience,
            'images': image_collection,
            'details_images': image_details,
            'beauty_images': image_beauty,
            'date': time.text if time else '',
            'author': author
        }

        #close the driver
        driver.quit()

        return data

        # for item in data:
        #     temp_data[item + '1'] = item

    except Exception as e:
        print("An error occurred:", e)

        

def seasonScrapperVogue():
    response = requests.get(
        'https://www.vogue.com/fashion-shows/seasons')
    soup = BeautifulSoup(response.text, 'html.parser')
    years = soup.find_all('p', class_='navigation__heading')
    temp = []
    for year in years:
        temp.append(year.text)
    shows = soup.find_all('a', class_='knabMb')
    showsDict = {}
    for i in range(len(temp)):
        showsDict[temp[i]] = []
        for show in shows:
            if str(temp[i]) in show.text:
                d = {}
                d['name'] = show.text
                d['link'] = show.get('href')
                showsDict[temp[i]].append(d)
    return showsDict
