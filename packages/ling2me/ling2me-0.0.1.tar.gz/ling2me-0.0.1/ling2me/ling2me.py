import requests
import json

class Ling2MeRequest():

    def translate(apikey, source_text, from_language, to_language):
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer '+apikey
	}
	data = {
            'text': source_text,  # text
            'from': from_language,  # from language
            'to': to_language,  # to language
        }
        response = requests.post('https://app.ling2me.com/api/translate', headers=headers, data=data)
        
        json_response = json.loads(response.text)

        return json_res['translated_text']
