from dotenv import load_dotenv

load_dotenv()

def fill_fields():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:

        form_data = {
            "Страна" : os.getenv('COUNTRY'),
            "Полное имя" : os.getenv('NAME'),
            "Электронная почта" : os.getenv('EMAIL'),
            "Адрес": os.getenv('ADDRESS'),
            "Номерь телефона": os.getenv('PHONE_NUMBER'),
            "URL": os.getenv('URL')
        }

        driver.get("https://reportcontent.google.com/forms/counter_notice?web-redirect=f&product=appengine&visit_id=638777606370602424-101465267&rd=1")
        time.sleep(3)

        response_text = generate_dispute_response()
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        input_textarea = driver.find_elements(By.TAG_NAME, "textarea")

        if len(input_fields) < 3:
            logging.error("Error")
            return

        input_fields[0].send_keys(form_data["Страна проживания"])
        input_fields[1].send_keys(form_data["Полное имя"])
        input_fields[2].send_keys(form_data["Полное имя"])
        input_fields[2].send_keys(form_data["Полное имя"])
        input_fields[3].send_keys(form_data["Электронная почта"])
        input_fields[3].send_keys(form_data["Адрес"])

        input_textarea[0].send_keys(form_data["Номерь телефона"])
        input_textarea[1].send_keys(form_data["URL"])
        time.sleep(1)

        button = driver.find_elemente(By.XPATH, "/html/body/div[1]/root/div/main/page-counter-notice-form/chip-form/div/div/span/div/div[2]/button/div[2]")
        button.click()
        logging.info("Success")

    except Exception as e:
        logging.error("Error")

    finally:
        driver.quit()
