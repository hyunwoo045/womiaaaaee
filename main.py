import random
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Firefox()
driver.implicitly_wait(time_to_wait=10)  # 요소 로딩까지 최대 10초까지만 기다려줌
driver.maximize_window()

# CONSTANT
EMAIL = 'answjd311@naver.com'
PASSWORD = 'af!546852'
NAME = '이담'
GENDER = '남아'
ADD_PERSON = '10인분'
ADDRESS_REGION = '동백죽전대로 507'
ADDRESS_DETAIL = '101동 703호'

MOM_PHONE = '01095156292'
MOM_NAME = '엄마'
PAPA_PHONE = '01047268401'
PAPA_NAME = '아빠'

# 3월 18일
# TABLE_POS = '/html/body/section[2]/div/div/div[1]/div[2]/table/tbody/tr[5]/td[2]'
# TABLE_TEXT = "평일돌잔치"
# TABLE_TIME = "15:30 ~ 19:00"

# 3월 8일
# TABLE_POS = '/html/body/section[2]/div/div/div[1]/div[2]/table/tbody/tr[3]/td[6]'
# TABLE_TEXT = "하람관"
# TABLE_TIME = "10:00 ~ 13:30"

# 3월 15일
# TABLE_POS = '/html/body/section[2]/div/div/div[1]/div[2]/table/tbody/tr[4]/td[6]'
# TABLE_TEXT = "영빈관"
# TABLE_TIME = "10:00 ~ 13:30"

# 3월 25일
# TABLE_POS = '/html/body/section[2]/div/div/div[1]/div[2]/table/tbody/tr[6]/td[2]'
# TABLE_TEXT = "평일돌잔치"
# TABLE_TIME = "10:00 ~ 13:30"

# 4월 6일
TABLE_POS = '/html/body/section[2]/div/div/div[1]/div[2]/table/tbody/tr[2]/td[7]'
TABLE_TEXT = '하람관'
TABLE_TIME = '10:00 ~ 13:30'


# TODO: https://thewoomije.co.kr/reservation-step1.php?year=2024&month=5&type=party  로 바꿔야함
def run_macro():
    # driver.get('https://thewoomije.co.kr/reservation-step1.php?year=2024&month=3&type=party')  # 3월
    driver.get('https://thewoomije.co.kr/reservation-step1.php?year=2024&month=4&type=party')  # 4월
    # driver.get('https://thewoomije.co.kr/reservation-step1.php?year=2024&month=5&type=party')  # 5월

    retry_flag = True
    while True:
        march_8 = driver.find_element(By.XPATH, TABLE_POS)
        march_8.click()

        select_box_table = driver.find_element(By.XPATH, '/html/body/section[2]/div/div/div[2]/form/table')
        select_box_table_tbody = select_box_table.find_element(By.ID, 'listbody')
        for tr_child in select_box_table_tbody.find_elements(By.TAG_NAME, 'tr'):
            fit_row = 0
            for td_child in tr_child.find_elements(By.TAG_NAME, 'td'):
                if td_child.text == TABLE_TEXT:
                    fit_row += 1
                if TABLE_TIME in td_child.text:
                    fit_row += 1

            if fit_row == 2:
                target_select_box = tr_child.find_elements(By.TAG_NAME, 'td')
                target_select_box[2].find_element(By.TAG_NAME, 'input').click()
                retry_flag = False
                break

        if not retry_flag:
            break
        else:
            # time.sleep(random.uniform(0.1, 0.11))
            driver.refresh()

    wait = WebDriverWait(driver, 10)
    submit_btn = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'submitBtn')))
    submit_btn.click()

    ######## 여기서부터는 사소함
    # 5분 어쩌고 하는거 확인 누르기
    # alert = Alert(driver)
    alert = wait.until(expected_conditions.alert_is_present())
    alert.accept()

    # 현재 창의 handle을 잡아두기
    submit_page_handle = driver.current_window_handle

    # form 입력 페이지
    # 이메일
    email_input = driver.find_element(By.ID, 'id')
    email_input.send_keys(EMAIL)

    # 패스워드
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(PASSWORD)

    # 패스워드 재입력
    repassword_input = driver.find_element(By.ID, 'repassword')
    repassword_input.send_keys(PASSWORD)

    # 애기 이름
    name_input = driver.find_element(By.ID, 'name')
    name_input.send_keys(NAME)

    # 애기 성별
    gender_select_element = driver.find_element(By.ID, 'gender')
    gender_select = Select(gender_select_element)
    gender_select.select_by_visible_text(GENDER)

    # 애기 생년월일
    birthday_input = driver.find_element(By.ID, 'birth')
    birthday_input.send_keys("2023-05-17")

    # 형제 추가 없음

    # 식사 주문
    add_person_select_element = driver.find_element(By.ID, 'addperson')
    driver.execute_script('arguments[0].scrollIntoView();', add_person_select_element)
    add_person_select = Select(add_person_select_element)
    for option in add_person_select.options:
        if ADD_PERSON in option.text:
            print('ADD_PERSON OPTION FOUND')
            wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="addperson"]/option[2]')))
            add_person_select.select_by_visible_text(option.text)
            break

    # 셀프 메이크업
    makeup_select_element = driver.find_element(By.ID, 'makeup')
    driver.execute_script('arguments[0].scrollIntoView();', makeup_select_element)
    makeup_select = Select(makeup_select_element)
    for option in makeup_select.options:
        if "더우미제" in option.text:
            print('MAKEUP OPTION FOUND')
            wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="makeup"]/option[2]')))
            makeup_select.select_by_visible_text(option.text)
            break

    # 엄마 연락처
    mom_phone_input = driver.find_element(By.ID, 'momphone')
    mom_phone_input.send_keys(MOM_PHONE)
    mom_name_input = driver.find_element(By.ID, 'momname')
    mom_name_input.send_keys(MOM_NAME)

    # 아빠 연락처
    papa_phone_input = driver.find_element(By.ID, 'papaphone')
    papa_phone_input.send_keys(PAPA_PHONE)
    papa_name_input = driver.find_element(By.ID, 'papaname')
    papa_name_input.send_keys(PAPA_NAME)

    # 우편번호 입력 창으로 이동
    address_input = driver.find_element(By.ID, 'address')
    address_input.click()
    all_window_handles = driver.window_handles
    address_window_handle = [handle for handle in all_window_handles if handle != submit_page_handle][0]
    driver.switch_to.window(address_window_handle)

    time.sleep(2)
    driver.switch_to.frame(0)

    # 도로명주소 입력
    region_input = wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="region_name"]')))
    region_input.send_keys(ADDRESS_REGION)
    region_input.send_keys(Keys.ENTER)

    time.sleep(2)
    # /html/body/div[1]/div/div[2]/ul/li/dl/dd[1]/span/button
    # /html/body/div[1]/div/div[2]/ul/li/dl/dd[2]/span/button[1]
    btn_link_post = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/ul/li/dl/dd[1]/span/button')
    btn_link_post.click()

    # 입력창으로 다시 이동
    driver.switch_to.window(submit_page_handle)

    # 상세주소 입력
    address_detail_input = driver.find_element(By.ID, 'addrdtaile')
    address_detail_input.send_keys(ADDRESS_DETAIL)

    # 끝
    final_submit_btn = driver.find_element(By.XPATH, '/html/body/section[2]/div/div/div[2]/form/div[15]/button')
    final_submit_btn.click()


if __name__ == '__main__':
    print("LETS GO!")
    run_macro()
