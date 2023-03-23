# Comparing Kayak flight prices ✈

## Goals
- Collect and analyze plane ticket prices - scraped from Kayak Explore - to determine whether factors like day of the week and time of the day directly influence ticket prices.  
- Find low ticket prices programatically for my own use 😁
- Set up an **email alert system to let me know when the ticket prices are lower than usual (or ever) for some route I'm interested in.**

Obs: Why not just use Google Flights or other competitor, you might ask? With this project, I can track price changes and receive alerts for 100s of routes compiled in a single email without having to set up several alerts. And also, I want the expertise of integrating several systems and architectures using Python, SQL, BigQuery, GitHub Actions (and more to come).

Airports of interest so far:
- Porto (OPO)
- Lisbon (LIS)
- Madrid (MAD)
- Milano Malpensa (MXP)
- Napoli (NAP)

## Challenges
In addition to the obvious learning curve of each tool and package used:
- Security - Concerns regarding secure access to Google Cloud account to use a BigQuery database (using Github Secrets)
- Scalability - Pretty soon we could be dealing with hundreds of files and thousands of rows
- Resource efficiency - Reducing BigQuery storage and queries must be a priority

## Limitations
- No way to obtain historical prices as the API used only returns upcoming flights.
- Straightforward logic for determining which prices to report: simply reports flights which prices are lower than historical minimum prices for that route/month

## Roadmap
### Should (and will) do it:

- [x] Setting up automated scraper script ( Python )  
- [x] Determine criteria for finding out if a price should be reported
- [x] Test e-mail output
- [x] Integrate Github Actions and Google Big Query
- [x] Determine price baseline for each destination
- [x] Read baselines from files stored in Github 
- [x] Setting up alert system that will send automated e-mail when tickets are available at good prices
- [x] Save new baselines to Google Bigquery
- [ ] Read baselines from Google Bigquery at the end of each execution
- [x] Store results in a Google Bigquery database
- [ ] Add one airport of interest: São Paulo
- [x] Adjust small details on email sent with deals:
   - [x] Add weekday
   - [x] Order by price (asc)
   - [x] Add number of days
- [ ] Design diagram explaining project/data flow
- [ ] Create slide deck with project summary and goals attained
- [x] Set up new automation to acquire data from another of Kayak's APIs - that one shows every possible flight on a certain route
- [ ] Decide what to do regarding large files resulted from calling the second API (1.5K rows for each route)

### Would be nice:
- [ ] Create parameter file for reading configs like departing airports and filter conditions (time of the year, one-way or round trip, etc.)
- [ ] Create parameter with different email addresses to send results for each city
- [ ] Streamlit page to show results
- [ ] Powerpoint presentation highlighting challenges, solutions and results
- [ ] Ad-hoc analysis to determine with a good amount of certainty best times to buy

Automated data collection task No. 1:  

[![Scraping flights from Kayak](https://github.com/rafabelokurows/scrapingKayak/actions/workflows/scrape.yml/badge.svg)](https://github.com/rafabelokurows/scrapingKayak/actions/workflows/scrape.yml)
