import requests

def control_philips_hue(light_id, state):
        bridge_ip = "your_bridge_ip"
        username = "your_username"
        url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"
        payload = {"on": state}
        response = requests.put(url, json=payload)
        if response.status_code == 200:
                return "Light state changed successfully."
        else:
                return "Failed to change light state."