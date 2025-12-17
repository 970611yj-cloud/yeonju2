import requests
import streamlit as st

def send_sms(phone_number, message):
    """
    Sends an SMS to the given phone number with the message.
    Currently a placeholder for Solapi/CoolSMS or Twilio.
    """
    # TODO: Implement actual API call
    # This is a simulation
    if not phone_number or not message:
        return False, "Phone number or message is empty."

    print(f"I> [Mock SMS] To: {phone_number} | Msg: {message}")
    
    # Simulate API success
    return True, f"SMS sent to {phone_number} (Simulation)"

    # --- Solapi Example Structure ---
    # api_key = "..."
    # api_secret = "..."
    # url = "https://api.coolsms.co.kr/messages/v4/send"
    # headers = generate_auth_headers(api_key, api_secret) 
    # data = { "message": { "to": phone_number, "from": "01012345678", "text": message } }
    # res = requests.post(url, headers=headers, json=data)
    # return res.status_code == 200, res.json()
