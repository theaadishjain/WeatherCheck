#!/usr/bin/env python3
"""
Test script to run the WhatsApp Weather notification locally.
This loads variables from .env file and runs the main program.
"""

import os
from dotenv import load_dotenv

# Load environment variables BEFORE importing weather_whatsapp
print("Loading environment variables from .env file...")
load_dotenv()

# Now import the weather_whatsapp module after environment variables are loaded
import weather_whatsapp

def main():
    required_vars = [
        "TWILIO_ACCOUNT_SID", 
        "TWILIO_AUTH_TOKEN", 
        "TWILIO_FROM_NUMBER",
        "TO_WHATSAPP_NUMBER", 
        "OPENWEATHER_API_KEY"
    ]
    
    # Check if all required variables are set
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        print(f"Error: Missing the following environment variables: {', '.join(missing)}")
        print("Please run setup_local.py first to configure your environment.")
        return
    
    print("Running weather notification test...")
    weather_whatsapp.main()
    print("Test complete.")

if __name__ == "__main__":
    main() 