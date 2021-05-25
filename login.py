# #!/usr/bin/env python
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging
logging.basicConfig(filename='/home/adminuser/logs/loginapp.log', filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)-25s,%(name)-8s,%(levelname)-8s,%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


# Run through testing steps
def startrun():
    logger.info('Starting the browser...')
    print(getcurrenttimestamp(), ' :: Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    logger.info('Browser started successfully. Navigating to the demo page to login.')
    print(getcurrenttimestamp(), ' :: Browser started successfully. Navigating to the demo page to login.')
    # driver = webdriver.Chrome()
    login('standard_user', 'secret_sauce', driver)
    addallinventorytocart(driver)
    displayshoppingcart(driver)
    emptyshoppingcart(driver)


# Start the browser and login with standard_user
def login(user, password, driver):
    driver.get('https://www.saucedemo.com/')
    # Wait for page to load
    print(getcurrenttimestamp(), ' :: Waiting for page https://www.saucedemo.com/ to load')
    driver.implicitly_wait(10)
    logger.info('Logging into the website with username: %s', user)
    stamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(getcurrenttimestamp(), ' :: Logging into the website with username:', user)
    driver.find_element_by_id("user-name").send_keys(user)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("login-button").click()
    actualurl = "https://www.saucedemo.com/inventory.html"
    expectedurl = driver.current_url
    assert actualurl == expectedurl
    logger.info('Successfully logged into site. Now at page %s', expectedurl)
    print(getcurrenttimestamp(), ' :: Successfully logged into site. Now at page', expectedurl)


def addallinventorytocart(driver):
    inventorylist = driver.find_elements_by_class_name("inventory_item")
    inventoryListCount = len(inventorylist)
    if inventoryListCount > 6:
        logger.warning("%d Inventory Items found. Only six will be placed in Shopping Cart", inventoryListCount)
        print(getcurrenttimestamp(), ' :: ', inventoryListCount,
              'Inventory Items found. Only six will be placed in Shopping Cart')
    print(getcurrenttimestamp(), ' :: ', inventoryListCount, 'Inventory Items found')
    itemCount = 0
    while itemCount < 6:
        inventorylist[itemCount].find_element_by_tag_name('button').click()
        driver.implicitly_wait(5)
        shoppingcartbadge = driver.find_element_by_class_name('shopping_cart_badge')
        itemdescelement = inventorylist[itemCount].find_element_by_class_name('inventory_item_name')
        logger.info('Item %s added to cart successfully. Number of items in cart: %s',
                    itemdescelement.text,
                    shoppingcartbadge.text)
        print(getcurrenttimestamp(), ' :: Item', itemdescelement.text,
              'added to cart successfully. Number of items in cart:',
              shoppingcartbadge.text)
        itemCount = itemCount + 1



def displayshoppingcart(driver):
    driver.find_element_by_class_name('shopping_cart_link').click()
    logger.info('Clicked on shopping cart')
    print(getcurrenttimestamp(), ' :: Clicked on shopping cart')
    driver.implicitly_wait(10)


def emptyshoppingcart(driver):
    inventoryElements = driver.find_elements_by_class_name('cart_item')
    shoppingcartbadge = driver.find_element_by_class_name('shopping_cart_badge')
    for inventoryElement in inventoryElements:
        logger.info('Number of items in shopping cart: %s before removing item: %s',
                    shoppingcartbadge.text,
                    inventoryElement.find_element_by_class_name('inventory_item_name').text)
        print(getcurrenttimestamp(), ' :: Number of items in shopping cart:',
              shoppingcartbadge.text,
              'before removing item:',
              inventoryElement.find_element_by_class_name('inventory_item_name').text)
        inventoryElement.find_element_by_tag_name('button').click()
    driver.quit()


def getcurrenttimestamp():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


startrun()
