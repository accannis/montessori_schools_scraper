import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

class MontessoriScraper:
    def __init__(self):
        self.base_url = "https://operanazionalemontessori.it"
        self.ajax_url = f"{self.base_url}/wp-admin/admin-ajax.php"
        self.schools_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f"{self.base_url}/trova-scuola-montessori/"
        }

    def get_nonce(self):
        """Extract ASL nonce from the page"""
        try:
            response = requests.get(f"{self.base_url}/trova-scuola-montessori/", headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup.find_all('script'):
                if script.string and 'ASL_REMOTE' in str(script.string):
                    match = re.search(r'"nonce":"([^"]+)"', script.string)
                    if match:
                        return match.group(1)
            return None
        except Exception as e:
            print(f"Error getting nonce: {e}")
            return None

    def fetch_schools(self):
        """Fetch schools data through ASL AJAX request"""
        print("Fetching schools data...")
        
        nonce = self.get_nonce()
        if not nonce:
            print("Could not find ASL nonce")
            return None
            
        print(f"Found nonce: {nonce}")
        
        # ASL plugin parameters
        payload = {
            'action': 'asl_load_stores',
            'nonce': nonce,
            'load_all': '1',
            'layout': '1',
            'lang': 'it_IT'
        }
        
        try:
            response = requests.post(self.ajax_url, headers=self.headers, data=payload)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except json.JSONDecodeError:
                    print("Response is not JSON")
                    if len(response.text) < 200:
                        print("Response preview:", response.text)
                    else:
                        print("Response too long to preview")
        except Exception as e:
            print(f"Error fetching schools: {e}")
        
        return None

    def process_schools(self, schools_data):
        """Process the schools data into a structured format"""
        processed_schools = []
        
        if not isinstance(schools_data, list):
            print("Unexpected data format")
            return processed_schools
            
        for school in schools_data:
            try:
                processed_school = {
                    'name': school.get('title', ''),
                    'address': school.get('street', ''),
                    'city': school.get('city', ''),
                    'state': school.get('state', ''),
                    'postal_code': school.get('postal_code', ''),
                    'phone': school.get('phone', ''),
                    'email': school.get('email', ''),
                    'website': school.get('website', ''),
                    'description': school.get('description', ''),
                    'latitude': school.get('lat', ''),
                    'longitude': school.get('lng', '')
                }
                processed_schools.append(processed_school)
            except Exception as e:
                print(f"Error processing school: {e}")
                continue
                
        return processed_schools

    def scrape(self):
        """Main scraping function"""
        print("Starting scraper...")
        schools_data = self.fetch_schools()
        
        if schools_data:
            print("\nSuccessfully retrieved schools data!")
            processed_schools = self.process_schools(schools_data)
            
            if processed_schools:
                print(f"Processed {len(processed_schools)} schools")
                df = pd.DataFrame(processed_schools)
                df.to_csv('schools.csv', index=False, encoding='utf-8-sig')
                print("Results saved to schools.csv")
            else:
                print("No schools could be processed from the data")
        else:
            print("\nNo schools data found.")

if __name__ == "__main__":
    scraper = MontessoriScraper()
    scraper.scrape()
