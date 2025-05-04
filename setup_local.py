#!/usr/bin/env python3
"""
Local setup script to help configure the environment variables
for testing the weather WhatsApp notification locally.
"""

import os
import json
from pathlib import Path

def main():
    print("WhatsApp Weather Notification - Local Setup")
    print("------------------------------------------")
    print("This script will help you set up environment variables for local testing.")
    print("The values will be saved to a .env file that you should not commit to Git.")
    print()
    
    # Collect variables
    env_vars = {
        "TWILIO_ACCOUNT_SID": input("Enter your Twilio Account SID: "),
        "TWILIO_AUTH_TOKEN": input("Enter your Twilio Auth Token: ")
    }
    
    # Ask user if they want to use a messaging service or direct number
    use_messaging_service = input("\nDo you want to use a Twilio Messaging Service for custom business name? (y/n): ").lower() == 'y'
    
    if use_messaging_service:
        env_vars["TWILIO_MESSAGING_SID"] = input("Enter your Twilio Messaging Service SID: ")
        print("\nNote: To customize your business name in WhatsApp:")
        print("1. Go to Twilio Console → Messaging → Services")
        print("2. Select your Messaging Service")
        print("3. Go to 'Sender Pool' and add your WhatsApp number")
        print("4. Configure your WhatsApp profile with custom business name and logo")
    else:
        env_vars["TWILIO_FROM_NUMBER"] = input("Enter your Twilio WhatsApp number (without 'whatsapp:' prefix): ")
    
    # Continue with other variables
    env_vars["TO_WHATSAPP_NUMBER"] = input("Enter your WhatsApp number to receive messages (e.g., +1234567890): ")
    env_vars["OPENWEATHER_API_KEY"] = input("Enter your OpenWeatherMap API key: ")
    env_vars["CITY"] = input("Enter your city name (e.g., London): ")
    
    # Write to .env file
    with open(".env", "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("\nConfiguration saved to .env file.")
    print("\nTo test locally:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Run: python test_locally.py")
    
    # Create GitHub Actions secrets instructions
    print("\nFor GitHub Actions setup, add these secrets to your repository:")
    for key in env_vars:
        print(f"  - {key}")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    main() 