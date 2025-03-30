import openai
from dotenv import load_dotenv
import os
from read_db import read_all_notifications
import sqlite3

load_dotenv()

openai.api_key = os.getenv('OPEN_API_KEY')

def generate_dispute_response(
    notice,
    url_notice, 
    url_site, 
    url_answer=os.getenv('ANSWER_FORM_URL') 
    ):

    user_content = (
        f"На сайт пришла жалоба на контент, размещённая на сайте: {url_notice}\n"
        f"Контент размещён на странице: {url_site}\n"
        f"Составь убедительный ответ в соответствии с формой, размещённой на странице {url_answer}, "
        f"указывая, что контент оригинальный, и приведи аргументы для разжалобы."
    )
    
    if notice[3] and notice[3] != 'Без названия':
        user_content += f"Название жалобы: {notice[3]}"
        
    if notice[4] and 'REDACTED' not in notice[4] and notice[4] != 'Без описания':
        user_content += f"Текст жалобы: {notice[4]}\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # (Подумать о выборе модели)
        messages=[
            {"role": "system", "content": "Ты — эксперт по защите авторских прав. Помогаешь пользователям составлять ответы на фейковые жалобы об авторских правах на русском языке. Не пиши лишнюю информацию т.к отправка полностью автоматизирована"},
            {"role": "user", "content": user_content}
            ]
    )
            
    return response["choices"][0]["message"]["content"] # Часть метаданных формата JSON

def main():    
    for notice in read_all_notifications():
        #ID, site, notice_id, title, description, response, processed = notice
        print(notice)
        print(
            generate_dispute_response(
                notice,
                url_notice='https://lumendatabase.org/notices/{notice[2]}',
                url_site=notice[1]
            )
        )
        break
    
main()
