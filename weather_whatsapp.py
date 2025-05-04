#!/usr/bin/env python3
import os, sys, requests
from datetime import datetime
from twilio.rest import Client

# Weather icons mapping
WEATHER_ICONS = {
    "2xx": "⛈️",  # Thunderstorm
    "3xx": "🌧️",  # Drizzle
    "5xx": "🌧️",  # Rain
    "6xx": "❄️",   # Snow
    "7xx": "🌫️",  # Atmosphere
    "800": "☀️",   # Clear
    "8xx": "☁️",   # Clouds
    "default": "⚠️"  # Extreme
}

def get_env_variables():
    """Get environment variables"""
    vars = {
        "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID"),
        "TWILIO_AUTH_TOKEN": os.environ.get("TWILIO_AUTH_TOKEN"),
        "TWILIO_FROM_NUMBER": os.environ.get("TWILIO_FROM_NUMBER"),
        "TO_WHATSAPP_NUMBER": os.environ.get("TO_WHATSAPP_NUMBER"),
        "OPENWEATHER_API_KEY": os.environ.get("OPENWEATHER_API_KEY"),
        "CITY": os.environ.get("CITY"),
        "TWILIO_MESSAGING_SID": os.environ.get("TWILIO_MESSAGING_SID")
    }
    
    if vars["OPENWEATHER_API_KEY"]:
        print(f"API Key loaded: {vars['OPENWEATHER_API_KEY'][:6]}...")
    return vars

def get_weather_icon(weather_id):
    """Get appropriate weather icon"""
    if 200 <= weather_id < 300: return WEATHER_ICONS["2xx"]
    elif 300 <= weather_id < 400: return WEATHER_ICONS["3xx"]
    elif 500 <= weather_id < 600: return WEATHER_ICONS["5xx"]
    elif 600 <= weather_id < 700: return WEATHER_ICONS["6xx"]
    elif 700 <= weather_id < 800: return WEATHER_ICONS["7xx"]
    elif weather_id == 800: return WEATHER_ICONS["800"]
    elif 801 <= weather_id < 900: return WEATHER_ICONS["8xx"]
    else: return WEATHER_ICONS["default"]

def get_location_by_ip():
    """Get location by IP address"""
    try:
        print("Detecting location by IP...")
        response = requests.get("https://ipapi.co/json/", timeout=5)
        data = response.json()
        if data.get("city"):
            print(f"Location detected: {data['city']}")
            return data["city"]
    except Exception as e:
        print(f"Location detection error: {e}")
    return "London"  # Default

def check_weather_alerts(lat, lon, api_key):
    """Check for weather alerts"""
    if not api_key: return ""
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            print("Warning: Weather alerts not available with your current plan")
            return ""
            
        response.raise_for_status()
        alerts = response.json().get("alerts", [])
        
        if not alerts: return ""
        
        alert_messages = []
        for alert in alerts:
            event = alert.get("event", "Weather Alert")
            desc = alert.get("description", "")
            short_desc = desc[:100] + "..." if len(desc) > 100 else desc
            alert_messages.append(f"⚠️ {event}: {short_desc}")
        
        return "\n\n" + "\n".join(alert_messages)
    except Exception as e:
        print(f"Weather alerts unavailable: {e}")
        return ""

def get_weather(city, api_key):
    """Fetch weather data"""
    if not api_key: return "Error: OpenWeatherMap API key is required"
    if not city: city = get_location_by_ip()
    
    try:
        print(f"Fetching weather for {city}...")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return f"Error: Could not retrieve weather data for {city}"
            
        data = response.json()
        
        # Validate data
        if not all(k in data for k in ["weather", "main", "wind", "coord"]) or not data["weather"]:
            return f"Error: Invalid weather data format for {city}"
        
        # Extract data
        weather_id = data["weather"][0]["id"]
        icon = get_weather_icon(weather_id)
        desc = data["weather"][0]["description"].capitalize()
        temp = round(data["main"]["temp"], 1)
        feels = round(data["main"]["feels_like"], 1)
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        
        # Check for alerts
        alerts = check_weather_alerts(data["coord"]["lat"], data["coord"]["lon"], api_key)
        
        # Format message
        message = (
            f"{icon} Weather Update for {city} - {datetime.now().strftime('%d %b %Y')}\n\n"
            f"• Condition: {desc} {icon}\n"
            f"• Temperature: {temp}°C\n"
            f"• Feels like: {feels}°C\n"
            f"• Humidity: {humidity}%\n"
            f"• Wind speed: {wind} m/s\n\n"
            f"Have a great day! {WEATHER_ICONS['800']}"
        )
        
        if alerts: message += alerts
        return message
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except Exception as e:
        return f"Error processing weather data: {str(e)}"

def send_whatsapp_message(message, account_sid, auth_token, from_number, to_number, messaging_sid=None):
    """Send WhatsApp message"""
    if not all([account_sid, auth_token, to_number]) or not (from_number or messaging_sid):
        return False
        
    try:
        print(f"Sending message to WhatsApp: {to_number}")
        client = Client(account_sid, auth_token)
        
        if messaging_sid:
            msg = client.messages.create(
                body=message,
                messaging_service_sid=messaging_sid,
                to=f"whatsapp:{to_number}"
            )
        else:
            msg = client.messages.create(
                body=message,
                from_=f"whatsapp:{from_number}",
                to=f"whatsapp:{to_number}"
            )
        
        print(f"Message sent successfully! SID: {msg.sid}")
        return True
    
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return False

def main():
    print("Loading environment variables...")
    env = get_env_variables()
    
    # Check required variables
    required = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TO_WHATSAPP_NUMBER", "OPENWEATHER_API_KEY"]
    missing = [var for var in required if not env.get(var)]
    
    if not env.get("TWILIO_FROM_NUMBER") and not env.get("TWILIO_MESSAGING_SID"):
        missing.append("TWILIO_FROM_NUMBER or TWILIO_MESSAGING_SID")
    
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)
    
    # Get weather and send message
    weather_msg = get_weather(env.get("CITY"), env.get("OPENWEATHER_API_KEY"))
    
    if weather_msg.startswith("Error:"):
        print(weather_msg)
        sys.exit(1)
    
    success = send_whatsapp_message(
        weather_msg,
        env.get("TWILIO_ACCOUNT_SID"),
        env.get("TWILIO_AUTH_TOKEN"),
        env.get("TWILIO_FROM_NUMBER"),
        env.get("TO_WHATSAPP_NUMBER"),
        env.get("TWILIO_MESSAGING_SID")
    )
    
    if not success: sys.exit(1)

if __name__ == "__main__":
    main() 