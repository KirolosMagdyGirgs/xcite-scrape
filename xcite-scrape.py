from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import json
from bs4 import BeautifulSoup
import time




def find_products():
    # Create a playwright instance
    with sync_playwright() as play_wright:
        browser = play_wright.chromium.launch()
        agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'
        )

        # Create a new context and page
        context = browser.new_context(user_agent=agent)
        page = context.new_page()

        # Apply the stealth settings
        stealth_sync(page)

        # Navigate to the website
        word=input('Enter Product')
        base_url = f"https://www.xcite.com.sa/search?q={word}"
        page.goto(base_url)



        # Calculate results_count only once before entering the loop
        page.wait_for_load_state("load")
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')
        results_count_text = soup.find('p', class_='typography-small text-gray-600').text.split(" ")[0]
        results_count = int(results_count_text)

        products = soup.find_all('li',class_='col-span-2 sm:col-span-4 sp:col-span-3 md:col-span-4 lg:col-span-3 xl:col-span-2 relative flex')
        product_list = []
        index=1
        while True:

            for product in products:
                product_dict = {}
                product_brand = product.find('h5', class_='mb-2 text-lg')
                product_name = product.p.text
                original_price = product.find('span', class_='text-base line-through')
                discount_price = product.find('span', class_='text-2xl text-functional-red-800 block mb-2')
                non_discount = product.h4
                link = product.div.a['href']


                product_dict['Product Number:'] = index
                print('Product Number:',index)
                index+=1
                if product_brand is None:
                    product_dict['Product Brand'] = '-'
                else:
                    product_dict['Product Brand'] = product_brand.text

                product_dict['Product Name'] = product_name

                if discount_price is None:
                    product_dict['Price'] = non_discount.text.split('I')[0]
                else:
                    product_dict['Discount Price'] = discount_price.text.split('I')[0]
                    product_dict['Original price'] = original_price.text

                product_dict['Link'] = link
                product_list.append(product_dict)

            #print(len(product_list))
            #print(results_count)

            # Find the "Next" button to navigate to the next page, if available
            show_more_button = page.locator('button.button.secondaryOnLight')
            if show_more_button.is_visible():
                show_more_button.click()
            else:
                break  # Exit the loop when there are no more pages



            # Break the loop when the total number of scraped products is equal to or greater than the results count
            if len(product_list)>results_count:
                break



        # Save the data to 'products.json'
        with open('products.json', 'w') as json_file:
            json.dump(product_list, json_file, indent=4)

        print("Data saved to 'products.json")

# Call the function to start scraping
find_products()



# if __name__ == '__main__':
#     while True :
#         find_products()
#         time_wait = 20     # every 20 minutes
#         time.sleep(60 * time_wait)