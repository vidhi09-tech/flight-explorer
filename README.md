# Scraping Kayak flight prices

## Business goal
Collecting and analyzing plane ticket prices - scraped from Kayak Explore - to determine whether factors like day of the week and time of the day where tickets are usually cheaper.  

Departing airports: Porto, Lisbon, Madrid, Milano (Malpensa) and Napoli

[![Scraping flights from Kayak](https://github.com/rafabelokurows/scrapingKayak/actions/workflows/scrape.yml/badge.svg)](https://github.com/rafabelokurows/scrapingKayak/actions/workflows/scrape.yml)

## Roadmap: 

- [x] Setting up automated scraper script ( Python )  
- [ ] Creating parameter file for reading configs like departing airports and filter conditions (time of the year, one-way or round trip, etc.)
- [ ] Determining price baseline for each destination
- [ ] Save new baselines to Google Bigquery
- [ ] Read baselines from Google Bigquery at the end of each execution
- [ ] What criteria should I use to determine whether a price is good for a certain route?
- [ ] Test e-mail output
- [ ] Setting up alert system that will send automated e-mail when tickets are available at good prices (see item above)
- [ ] Ad-hoc analysis to determine with a good amount of certainty best times to buy
- [ ] Store results in a Google Bigquery database
- [ ] Streamlit page to show some results
