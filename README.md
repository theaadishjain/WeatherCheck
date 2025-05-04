# Daily Weather WhatsApp Notification

This project automatically sends daily weather updates via WhatsApp at 9 AM using GitHub Actions. The service is completely free to set up and use.

## How It Works

1. A GitHub Actions workflow runs every day at 9 AM
2. The script fetches weather data for your configured city
3. It sends the weather report to your WhatsApp number

## Features

- **Daily Weather Updates**: Receive weather information every morning at 9 AM
- **Weather Icons**: Visual weather indicators with emoji icons that match current conditions
- **Auto-Location Detection**: Automatically detects your location if no city is specified
- **Weather Alerts**: Includes any current weather warnings or alerts for your area (requires OneCall API subscription)
- **Custom Business Name**: Option to customize how the sender appears in WhatsApp
- **Persistent Connection**: Keeps WhatsApp connection active without manual reconnection

## Setup Instructions

### 1. Create Required Accounts

- **Twilio**: Sign up for a [Twilio account](https://www.twilio.com/try-twilio) (free tier)
- **OpenWeatherMap**: Create an account on [OpenWeatherMap](https://openweathermap.org/api) and get a free API key
  - Note: For weather alerts, you'll need to subscribe to the [OneCall API](https://openweathermap.org/api/one-call-3) (optional)

### 2. Set Up Twilio WhatsApp Sandbox

1. In your Twilio console, navigate to "Messaging" → "Try it" → "WhatsApp"
2. Follow the instructions to connect your WhatsApp number to the Twilio sandbox
3. Note down the Twilio WhatsApp number you'll be using

### 3. (Optional) Create a Messaging Service for Custom Business Name

1. In your Twilio console, navigate to "Messaging" → "Services"
2. Click "Create Messaging Service" and give it a name (e.g., "Weather Updates")
3. Select "WhatsApp" when asked about use case
4. Add your WhatsApp sender number to the Sender Pool
5. Go to "WhatsApp Settings" and configure your business profile
6. Note down the Messaging Service SID (starts with "MG")

### 4. Fork and Configure this Repository

1. Fork this repository to your GitHub account
2. Go to your forked repository's Settings → Secrets → Actions
3. Add the following secrets:
   - `TWILIO_ACCOUNT_SID` - Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN` - Your Twilio Auth Token
   - Either:
     - `TWILIO_FROM_NUMBER` - Your Twilio WhatsApp number (without the "whatsapp:" prefix), OR
     - `TWILIO_MESSAGING_SID` - Your Twilio Messaging Service SID (to use custom business name)
   - `TO_WHATSAPP_NUMBER` - Your personal WhatsApp number (in format: +1234567890)
   - `OPENWEATHER_API_KEY` - Your OpenWeatherMap API key
   - `CITY` - Your city name (e.g., "London") - *Optional: will auto-detect if not provided*

### 5. Test the Workflow

1. Go to the "Actions" tab in your repository
2. Select the "Daily Weather Notification" workflow
3. Click "Run workflow" to test it immediately

### 6. Keep WhatsApp Connection Active

The Twilio WhatsApp Sandbox connection expires after 72 hours of inactivity. To keep it active:

1. Enable the "Keep WhatsApp Connection Alive" workflow in your repository:
   - Go to the "Actions" tab
   - Select "Keep WhatsApp Connection Alive"
   - Click "Enable workflow"

2. This workflow automatically sends an invisible keep-alive message daily to maintain the connection.

## Customization

- To change the scheduled time, edit the cron expression in `.github/workflows/weather_notification.yml`
- To modify the message format, edit the `get_weather()` function in `weather_whatsapp.py`
- To change how the business appears in WhatsApp:
  - Use a Messaging Service as described in step 3
  - Configure your business profile in the Twilio console
  - Set a business name, description, and logo
- To use auto-location detection, simply don't set the `CITY` secret or set it to an empty value

## Notes

- The GitHub Actions workflow runs in UTC timezone
- Free tiers of both Twilio and OpenWeatherMap are sufficient for basic functionality
- Weather alerts require a subscription to the OneCall API from OpenWeatherMap
- Location detection uses IP geolocation as a fallback when no city is specified 