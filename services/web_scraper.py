import web_services.webdriver_setup as setup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

def get_brand_names(urls: list, wait_sec: int = 10):
    driver = setup.get_driver()

    brand_list = []

    try:
        for url in urls:
            # Open the webpage
            driver.get(url)

            # The target website has a dropdown menu which contains all the brand names in our tax invoice
            # Wait for the dropdown to be clickable
            wait = WebDriverWait(driver, wait_sec)
            dropdown = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".category-results-select-all__arrow")))
            dropdown.click()

            # Wait for the dropdown content to be loaded
            # Retrieve all brand names that are under a specific class
            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".category-results-top-category__name")))
            
            # Extract brand names
            brand_elements = driver.find_elements(By.CSS_SELECTOR, ".category-results-top-category__name")
            brands = [element.text for element in brand_elements]
            brand_list.extend(brands)

    finally:
        driver.quit()

    return brand_list


