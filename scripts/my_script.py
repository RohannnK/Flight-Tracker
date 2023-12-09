from my_module.functions import fetch_real_time_flights

def main():
    api_key = "1b72576d264f229fe85c9a9f8ddda862" # This API key is free and public, so I can show it
    #Reminder that only 1000 requests are permitted for this free plan
    flights = fetch_real_time_flights(api_key)
    for flight in flights:
        print(flight)

if __name__ == "__main__":
    main()
