# Comparing Kayak flight prices

## Goals
Collecting and analyzing plane ticket prices - scraped from Kayak Explore - to determine whether factors like day of the week and time of the day where tickets are usually cheaper.  

Also, I will set up an email alert system to let me know when the ticket prices are lower than usual (or ever) for some route I'm interested in.

Why not just use Google Flights or other competitor, you might ask? With this project, I can track price changes and receive alerts for 100s of routes compiled in a single email without having to set up several alerts. And also, I want the expertise of integrating several systems and architectures using Python, SQL, BigQuery, GitHub Actions (and more to come).

Airports of interest so far: Porto, Lisbon, Madrid, Milano (Malpensa) and Napoli

Automated task:
[![Scraping flights from Kayak](https://github.com/rafabelokurows/scrapingKayak/actions/workflows/scrape.yml/badge.svg)](https://github.com/rafabelokurows/scrapingKayak/actions/workflows/scrape.yml)

## Should (and will) do it:

- [x] Setting up automated scraper script ( Python )  
- [x] Determine criteria for finding out if a price should be reported
- [x] Test e-mail output
- [x] Integrate Github Actions and Google Big Query
- [ ] Determine price baseline for each destination
- [ ] Save new baselines to Google Bigquery
- [ ] Read baselines from Google Bigquery at the end of each execution
- [ ] Setting up alert system that will send automated e-mail when tickets are available at good prices (see item above)
- [ ] Store results in a Google Bigquery database
- [ ] Design diagram explaining project flow

## Would be nice:
- [ ] Create parameter file for reading configs like departing airports and filter conditions (time of the year, one-way or round trip, etc.)
- [ ] Streamlit page to show some results
- [ ] Ad-hoc analysis to determine with a good amount of certainty best times to buy
