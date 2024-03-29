from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

@pytest.fixture
def login():
    driver = webdriver.Chrome()
    expected_title = "Google"
    expected_title_2 = "Swag Labs"

    driver.get('https://www.google.com/')
    time.sleep(5)
    assert driver.title==expected_title, "Wrong page as title not matching"

    driver.get("https://www.saucedemo.com/")
    assert driver.title == expected_title_2, "Result did not match"

    action = ActionChains(driver)
    action.click(on_element = driver.find_element(By.ID, "user-name")).send_keys("standard_user").perform()
    action.click(on_element = driver.find_element(By.ID, "password")).send_keys("secret_sauce").perform()
    action.click(on_element = driver.find_element(By.ID, "login-button")).perform()
    time.sleep(5)
    return driver, action

def test_sort_price_high_to_low(login):
    driver, action = login
    action.click(on_element = driver.find_element(By.CLASS_NAME, "product_sort_container")).perform()
    action.click(on_element = driver.find_element(By.VALUE, "hilo")).perform()
    time.sleep(2)

    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    product_prices = [float(item.text[1:]) for item in product_elements]
    reverse_sorted_product_prices = sorted(product_prices, reverse = True)

    assert product_prices == reverse_sorted_product_prices, "Sorting elements on prices from high to low not working"


def test_element_selected_display_cart(login):
    driver, action = login
    inventory_item_names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    list1 = [1,2,4]
    selected_item_names = []
    for i in list1:
        action.click(onelement = add_to_cart_buttons[i-1]).perform()
        selected_item_names.append(inventory_item_names[i-1])
            
    action.click(onelement = driver.find_element(By.CLASS_NAME, "shopping_cart_link")).perform()
    cart_item_names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]

    assert cart_item_names.sort() == selected_item_names.sort(), "The selected items are not viewing in the cart"


def test_number_of_items_selected_display_cart_symbol(login):
    driver, action = login
    
    def add_or_remove_item(item="add"):
        if item == "add":
            add_to_cart_buttons = driver.find_elements(By.LINK_TEXT, "Add to cart")
            if add_to_cart_button != None:
                action.click(onelement = add_to_cart_button[0]).perform()
                counter+=1
            else:
                print("All elements are already added to cart")
        else:
            remove_from_cart_buttons = driver.find_elements(By.LINK_TEXT, "Remove")
            if remove_from_cart_buttons != None:
                action.click(onelement = remove_from_cart_buttons[-1]).perform()
                counter-=1
            else:
                print("No elements present in cart")
                
    counter = int(driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text)
    list_of_commands = ["add","add","add","remove","add","remove","remove"]
    for com in list_of_commands:
        add_or_remove_item(com)
        assert int(driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text) == counter, "The display of number of items in cart is not working properly"

        
    #n=0
    #while(n<10):
        #position = int(input("Enter the position:"))
        #action.click(on_element = add_to_cart_buttons[position-1]).perform()
        #n+=1
        #value_of_buttons = [item.text for item in add_to_cart_buttons]
        #number_of_items_selected = value_of_buttons.count("Remove")
        #number_of_items_in_cart = int(driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text)
        #if(number_of_items_selected == 0):
            #assert number_of_items_in_cart == None, "Number of items present in cart not matching"
        #else:
            #assert number_of_items_in_cart == number_of_items_selected, "Number of items present in cart not matching"


def test_sauce_insights(login):
    driver, action = login
    action.click(on_element = driver.find_element(By.ID, "react-burger-menu-btn")).perform()
    action.click(on_element = driver.find_element(By.ID, "about_sidebar_link")).perform()

    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
 
    action.click(onelement = driver.find_element(By.LINK_TEXT, "Sauce Insights")).perform()
    time.sleep(5)
    expected_title_3 = "Testing Insights With Sauce Insights | Sauce Labs"
    assert driver.title == expected_title_3, "Sauce Insights page is not opening"


def test_automation_tab_open(login):
    driver, action = login
    action.click(on_element = driver.find_element(By.ID, "react-burger-menu-btn")).perform()
    action.click(on_element = driver.find_element(By.ID, "about_sidebar_link")).perform()

    action.move_to_element(driver.find_element(By.LINK_TEXT, "Solutions").click().perform()
    action.click(onelement = driver.find_element(By.LINK_TEXT, "Test automation")).perform()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])
    expected_title_3 = "Getting Started with Sauce Labs Integrations | Sauce Labs Documentation"
    assert driver.title == expected_title_3, "Test Automation page is not opening
