# Pobeda.aero promo tickets finder 
It is an easy tickets finder that can get some Pobeda offers using Python, Selenium and Chrome.

Requirements:
- Python 3.0 +
- Selenium 3.141 +
- Chrome 72.0 +
- Chromedriver same version as your chrome
- ConfigParser 3.74 

Ho to use:
1. Set in settings.txt:
- *from_IataCode* - Your IATA airport code (for example, VKO - Vnukovo International Airport)
- *to_IataCode* - Destination airport IATA code or ALL
- *checkLowerThan* - If you needs to check only offers lower certain price, set YES
- *chromeDriverPath* - Relative or full path to chromedriver executable
2. Run main.py and see at the console output.

Output example:
- *Tickets from  VKO  to  EIN :*
- Москва (Внуково)
- Эйндховен 
- 17 июл 2019 
- 3528  РУБ
