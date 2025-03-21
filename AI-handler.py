def generate_dispute_response(
    url_abuz=os.getenv('NOTICE_URL'), 
    url_site=os.getenv('SITE_URL'), 
    url_answer=os.getenv('ANSWER_FORM_URL') 
    ):

    openai.api_key = os.getenv('OPEN_API_KEY')
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # (Подумать о выборе модели)
        messages=[
            {"role": "system", "content": "Ты — эксперт по защите авторских прав. Помогаешь пользователям составлять ответы на фейковые жалобы об авторских правах."},
            {"role": "user", "content": f"На сайт пришла жалоба на контент, размещённая на сайте: {url_abuz}\n\n"
                                        f"Контент размещён на странице: {url_site}\n\n"
                                        f"Составь убедительный ответ в соответствии с формой размещённой на странице {url_answer}, указывая, что контент оригинальный, и приведи аргументы для разжалобы."}
        ]
    )
    return response["choices"][0]["message"]["content"] # Часть метаданных формата JSON
