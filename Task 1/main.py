from Speech_Recognition import recognize_speech
from Text_to_Speech import speak_text
from Answering_General_Knowledge_Questions import ask_wolframalpha
from Natural_Language_Processing import detect_intent_texts
from Send_Email import send_email
from Send_Email import extract_email_details
from Set_Reminder import set_reminder
from Weather import get_weather
from Controlling_Smar_Home_Devices import control_philips_hue
from Third_Party_API_Integrations import create_google_calendar_event
from Third_Party_API_Integrations import get_google_calendar_service

def main():
        while True:
                text = recognize_speech()
                if text:
                        response = detect_intent_texts('your_project_id', 'unique_session_id', text, 'en')
                        print(response)
                        if 'send email' in text:
                                subject, body, recipient = extract_email_details(text)
                                result = send_email(subject, body, recipient)
                                speak_text(result)
                        elif 'set reminder' in text:
                                Reminder = response['fields']['Reminder']['stringValue']
                                Date = response['fields']['Date']['stringValue']
                                Time = response['fields']['Time']['stringValue']
                                set_reminder(Reminder, Date + ' ' + Time)
                                speak_text("Reminder set successfully.")
                        elif 'weather' in text:
                                City = response['fields']['City']['stringValue']
                                weather_response = get_weather(City)
                                speak_text(weather_response)
                        elif 'turn on light' in text:
                                control_philips_hue('1', True)
                                speak_text("Light turned on.")
                        elif 'turn off light' in text:
                                control_philips_hue('1', False)
                                speak_text("Light turned off.")
                        elif 'what is' in text:
                                answer = ask_wolframalpha(text)
                                speak_text(answer)
                        elif 'create event' in text:
                                Event = response['fields']['Event']['stringValue']
                                StartDate = response['fields']['StartDate']['stringValue']
                                EndDate = response['fields']['EndDate']['stringValue']
                                create_google_calendar_event(Event, StartDate, EndDate)
                                speak_text("Event created successfully.")
                        else:
                                speak_text(response)

if __name__ == "__main__":
        main()