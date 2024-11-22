import requests

def send_to_google_analytics(user_id, endpoint):
    payload = {
        'v': '1',
        'tid': 'UA-XXXXX-Y',
        'cid': user_id,
        't': 'event',
        'ec': 'API',
        'ea': endpoint,
    }
    requests.post('https://www.google-analytics.com/collect', data=payload)