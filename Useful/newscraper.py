import pandas as pd
from bs4 import BeautifulSoup

# Load the HTML file
with open('used488s.htm', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Create lists to hold extracted data
years = []
prices = []
mileages = []
exterior_colors = []
interior_colors = []
locations = []

# Parse the listings
listings = soup.find_all('div', class_='VehicleCard__content__aWk634tv')

for listing in listings:
    # Extract year and mileage
    year_element = listing.find('div', class_='VehicleCard__year__31akchrt')
    year = year_element.get_text(strip=True) if year_element else 'N/A'
    
    mileage_element = listing.find('div', class_='VehicleCard__odometer__2Aa-D18j')
    mileage = mileage_element.get_text(strip=True) if mileage_element else 'N/A'
    
    # Clean and convert mileage to integer
    mileage = int(mileage.replace(',', '').replace(' mi', '')) if mileage != 'N/A' else 'N/A'
    
    # Extract price
    price_element = listing.find('div', class_='VehicleCard__specsHead__priceValue__13AM2QkL')
    price = price_element.get_text(strip=True) if price_element else 'N/A'
    if "Price on request" in price:
        continue  # Skip listings with "Price on request"
    
    # Clean and convert price to integer
    price = int(price.replace('$', '').replace(',', '')) if price != 'N/A' else 'N/A'
    
    # Extract exterior color
    exterior_color_element = listing.find('div', string='exterior color')
    exterior_color = exterior_color_element.find_next_sibling('div').get_text(strip=True) if exterior_color_element else 'N/A'
    
    # Extract interior color
    interior_color_element = listing.find('div', string='interior color')
    interior_color = interior_color_element.find_next_sibling('div').get_text(strip=True) if interior_color_element else 'N/A'
    
    # Extract location
    location_element = listing.find('div', string=' Available at')
    location = location_element.find_next_sibling('div').get_text(strip=True) if location_element else 'N/A'

    # Append the data to the lists
    years.append(year)
    prices.append(price)
    mileages.append(mileage)
    exterior_colors.append(exterior_color)
    interior_colors.append(interior_color)
    locations.append(location)

# Create a DataFrame
df = pd.DataFrame({
    'Year': years,
    'Price': prices,
    'Mileage': mileages,
    'Exterior Color': exterior_colors,
    'Interior Color': interior_colors,
    'Location': locations
})

# Save to CSV
df.to_csv('488data.csv', index=False)

print("Data scraping complete, CSV file saved.")
