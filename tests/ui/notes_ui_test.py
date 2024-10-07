import json
import os
import time
import requests
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--headless')
from faker import Faker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from .support_ui import create_user_ui, delete_json_file, delete_user_ui, login_user_ui
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def test_create_note_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    # 1 = Home, 2 = Work , 3 = Personal
    note_category = Faker().random_element(elements=(1, 2, 3))
    # 1 = Checked, 2 = Unchecked
    note_completed = Faker().random_element(elements=(1,2))
    note_description = Faker().sentence(3)
    note_title = Faker().sentence(2)
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.XPATH,"//button[normalize-space()='+ Add Note']").click() 
    driver.find_element(By.CSS_SELECTOR,"#category").click()
    driver.find_element(By.CSS_SELECTOR,f"#category > option:nth-child({note_category})").click()
    for x in range(note_completed):
        driver.find_element(By.CSS_SELECTOR,f"#completed").click()
    driver.find_element(By.CSS_SELECTOR,"#title").send_keys(note_title)
    driver.find_element(By.CSS_SELECTOR,"#description").send_keys(note_description)
    driver.find_element(By.CSS_SELECTOR,"button[data-testid='note-submit']").click()
    for x in range(15):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    if note_completed == 1:  
        note_message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="progress-info" and text()="You have completed all notes"]')))
    else:
        note_message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="progress-info" and text()="You have 0/1 notes completed in the all categories"]')))
    note_title_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="note-card-title" and text()="{note_title}"]')))
    note_description_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//p[@class='card-text' and text()='{note_description}']")))
    note_updated_at_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="note-card-updated-at"]')))
    note_updated_at = note_updated_at_element.text.strip()
    note_style = note_title_element.get_attribute("style")
    if note_completed == 1:
        assert note_style == "background-color: rgba(40, 46, 41, 0.6); color: rgb(255, 255, 255);"
    elif note_category == 1:
        assert note_style == "background-color: rgb(255, 145, 0); color: rgb(255, 255, 255);"
    elif note_category == 2:
         assert note_style == "background-color: rgb(92, 107, 192); color: rgb(255, 255, 255);"
    else:
        assert note_style == "background-color: rgb(50, 140, 160); color: rgb(255, 255, 255);"        
    assert note_description_element.is_displayed()
    assert note_message_element.is_displayed()
    assert note_title_element.is_displayed()
    assert note_updated_at_element.is_displayed()
    combined_responses = {
        'note_category': note_category,
        'note_completed': note_completed,
        'note_description': note_description,
        'note_title': note_title,
        'note_updated_at': note_updated_at
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def test_check_note_ui():
    randomData = Faker().hexify(text='^^^^^^^^^^^^')
    create_user_ui(randomData)
    login_user_ui(randomData)
    create_note_ui(randomData)
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    note_category = data['note_category']   
    note_completed = data['note_completed']  
    note_description = data['note_description']
    note_title = data['note_title']
    note_updated_at = data['note_updated_at']
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.XPATH,"//a[normalize-space()='View']").click() 
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    note_description_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="note-card-description"]')
    note_title_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="note-card-title" and text()="{note_title}"]')))
    note_updated_at_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="note-card-updated-at"]')
    checkbox_status_element = driver.find_element(By.CSS_SELECTOR, '#switch')
    assert note_description_element.text.strip() == note_description
    assert note_title_element.text.strip() == note_title
    assert note_updated_at_element.text.strip() == note_updated_at
    note_style = note_title_element.get_attribute("style")
    if note_completed == 1:
        assert note_style == "background-color: rgba(40, 46, 41, 0.6); color: rgb(255, 255, 255);"
        assert checkbox_status_element.is_selected() == True
    elif note_category == 1:
        assert note_style == "background-color: rgb(255, 145, 0); color: rgb(255, 255, 255);"
        assert checkbox_status_element.is_selected() == False
    elif note_category == 2:
         assert note_style == "background-color: rgb(92, 107, 192); color: rgb(255, 255, 255);"
         assert checkbox_status_element.is_selected() == False
    else:
        assert note_style == "background-color: rgb(50, 140, 160); color: rgb(255, 255, 255);" 
        assert checkbox_status_element.is_selected() == False 
    delete_user_ui()
    delete_json_file(randomData)
    time.sleep(5)

def delete_json_file(randomData):
    os.remove(f"./tests/fixtures/file-{randomData}.json")

def create_user_ui(randomData):
    user_email = Faker().company_email()
    user_name = Faker().name()
    user_password = Faker().password()
    driver.get("https://practice.expandtesting.com/notes/app/register")
    driver.find_element(By.CSS_SELECTOR, "#root > div > div > div").click()
    assert driver.title == "Notes React Application for Automation Testing Practice"
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#confirmPassword").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#name").send_keys(user_name)
    for x in range(10):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    driver.implicitly_wait(2)
    user_created = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-success > b").is_displayed()
    assert user_created == True
    combined_responses = {
        'user_email': user_email,
        'user_name': user_name,
        'user_password': user_password
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def login_user_ui(randomData):
    with open(f"./tests/fixtures/file-{randomData}.json", 'r') as json_file:
        data = json.load(json_file)
    user_email = data['user_email']   
    user_password = data['user_password']  
    user_name = data['user_name']
    driver.get("https://practice.expandtesting.com/notes/app/login")
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    for x in range(8):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()
    user_logged = driver.find_element(By.CSS_SELECTOR,"#navbarSupportedContent > ul > li:nth-child(1) > a").is_displayed()
    assert user_logged == True
    user_token = driver.execute_script("return localStorage.getItem('token')")
    headers = {'accept': 'application/json', 'x-auth-token': user_token}
    resp = requests.get("https://practice.expandtesting.com/notes/api/users/profile", headers=headers)
    respJS = resp.json()
    user_id = respJS['data']['id']
    combined_responses = {
        'user_email': user_email,
        'user_id': user_id,
        'user_name': user_name,
        'user_password': user_password,
        'user_token': user_token
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)

def delete_user_ui():
    driver.get("https://practice.expandtesting.com/notes/app/profile")
    for x in range(12):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.CSS_SELECTOR, "div.row > div > button").click()
    driver.find_element(By.CSS_SELECTOR, "div.modal-footer > button.btn.btn-danger").click()
    driver.implicitly_wait(5)
    user_deleted = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div > div > div:nth-child(2) > div > div > div").is_displayed()
    assert user_deleted == True

def create_note_ui(randomData):
    # 1 = Home, 2 = Work , 3 = Personal
    note_category = Faker().random_element(elements=(1, 2, 3))
    # 1 = Checked, 2 = Unchecked
    note_completed = Faker().random_element(elements=(1,2))
    note_description = Faker().sentence(3)
    note_title = Faker().sentence(2)
    for x in range(5):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    driver.find_element(By.XPATH,"//button[normalize-space()='+ Add Note']").click() 
    driver.find_element(By.CSS_SELECTOR,"#category").click()
    driver.find_element(By.CSS_SELECTOR,f"#category > option:nth-child({note_category})").click()
    for x in range(note_completed):
        driver.find_element(By.CSS_SELECTOR,f"#completed").click()
    driver.find_element(By.CSS_SELECTOR,"#title").send_keys(note_title)
    driver.find_element(By.CSS_SELECTOR,"#description").send_keys(note_description)
    driver.find_element(By.CSS_SELECTOR,"button[data-testid='note-submit']").click()
    for x in range(15):
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.DOWN)
    if note_completed == 1:  
        note_message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="progress-info" and text()="You have completed all notes"]')))
    else:
        note_message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="progress-info" and text()="You have 0/1 notes completed in the all categories"]')))
    note_title_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//div[@data-testid="note-card-title" and text()="{note_title}"]')))
    note_description_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//p[@class='card-text' and text()='{note_description}']")))
    note_updated_at_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="note-card-updated-at"]')))
    note_updated_at = note_updated_at_element.text.strip()
    note_style = note_title_element.get_attribute("style")
    if note_completed == 1:
        assert note_style == "background-color: rgba(40, 46, 41, 0.6); color: rgb(255, 255, 255);"
    elif note_category == 1:
        assert note_style == "background-color: rgb(255, 145, 0); color: rgb(255, 255, 255);"
    elif note_category == 2:
         assert note_style == "background-color: rgb(92, 107, 192); color: rgb(255, 255, 255);"
    else:
        assert note_style == "background-color: rgb(50, 140, 160); color: rgb(255, 255, 255);"        
    assert note_description_element.is_displayed()
    assert note_message_element.is_displayed()
    assert note_title_element.is_displayed()
    assert note_updated_at_element.is_displayed()
    combined_responses = {
        'note_category': note_category,
        'note_completed': note_completed,
        'note_description': note_description,
        'note_title': note_title,
        'note_updated_at': note_updated_at
    }
    with open(f"./tests/fixtures/file-{randomData}.json", 'w') as json_file:
        json.dump(combined_responses, json_file, indent=4)