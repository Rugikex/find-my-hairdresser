# <div align=center>Find my hairdresser</div>

This Python script utilizes the Google Maps API to help users find hair salons in a specific area.

### Configuration:
Before running the script, make sure to set the GOOGLE_API_KEY environment variable with your Google API key with Places API enabled.

### Usage:
```bash
python find_my_hairdresser.py
```

### Restrictions:

The script is limited to 60 hair salons per search. If more than 60 hair salons are found, the script will only return the first 60 result because of the Google API restrictions.