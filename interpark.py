import datetime
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_diff_servertime_to_now(target_time):
    interpark_r = requests.get("https://ticket.interpark.com/")
    interpark_time = interpark_r.headers['Date']
    dt = datetime.datetime.strptime(interpark_time, '%a, %d %b %Y %H:%M:%S %Z')
    dt_utc = dt.replace(tzinfo=datetime.timezone.utc)
    dt_epoch = int(dt_utc.timestamp())

    input_dt = datetime.datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S %Z")
    input_dt_utc = input_dt.replace(tzinfo=datetime.timezone.utc)
    input_epoch = int(input_dt_utc.timestamp())

    return input_epoch - dt_epoch


def run(t):
    driver = webdriver.Chrome()
    driver.implicitly_wait(time_to_wait=10)  # 요소 로딩까지 최대 10초까지만 기다려줌
    driver.maximize_window()
    driver.get("https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE015")

    login_button = driver.find_element(By.XPATH, '//*[@id="ent-ticket__header"]/div[2]/div[1]/div/div[2]/a[1]')
    login_button.click()

    time.sleep(1)
    driver.switch_to.frame(0)

    # id_input = driver.find_element(By.ID, 'userId')
    id_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'userId'))
    )
    id_input.send_keys("hyunwoo045")

    password_input = driver.find_element(By.ID, 'userPwd')
    password_input.send_keys("@Hwoo045#rla")

    login_btn = driver.find_element(By.ID, 'btn_login')
    login_btn.click()
    time.sleep(1)

    # 티켓팅 시간까지 남은 시간
    wait_for = get_diff_servertime_to_now(t)
    print('{} 초 남았습니다'.format(wait_for))

    while wait_for > 0:
        #  10초 남을때 까지 대기
        if wait_for > 2:
            time.sleep(wait_for / 2)
            wait_for = get_diff_servertime_to_now(t)
            print('{} 초 남았습니다'.format(wait_for))
            continue

        if wait_for <= 0:
            break
        else:
            time.sleep(0.2)
            wait_for = get_diff_servertime_to_now(t)

    print("GO!")
    driver.refresh()
    # reserve_btn = EC.element_to_be_clickable(
    #     (By.XPATH, '/html/body/div[2]/div[4]/div[4]/div[5]/div[5]')
    # )
    reserve_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div[4]/div[4]/div[5]/div[5]')
        )
    )
    reserve_btn.click()

    time.sleep(3600)


if __name__ == '__main__':
    target_time = '2024-02-22 06:57:00 GMT'
    run(target_time)
