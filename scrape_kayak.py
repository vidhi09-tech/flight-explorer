import json
import requests
import pandas as pd
import calendar
import datetime
from time import gmtime, strftime

def scrape_kayak(start='', end='', airport = 'OPO'):
    """
    This function scrapes flight information from the kayak explore page.
    Parameters:
    start, end, airport - integer representing earliest possible departure date
    in YYYYMMDD format, integer representing latest return date, string with
    three letter code for starting airport. When both are start and end are
    left blank, results are returned from present date to one year in the
    future.
    Returns:
    df - a data frame containing all destination cities and corresponding
    flight information returned by the scrape
    """

    # Format the beginning and end dates to insert them into the URL
    #start = '&depart=' + str(start)
    #end = '&return=' + str(end)
    #"https://www.kayak.pt/s/horizon/exploreapi/destinations?airport=OPO&budget=&depart=20230601&return=20230630&tripdurationrange=4%2C7&duration=&flightMaxStops=&stopsFilterActive=false&topRightLat=51.82490080841914&topRightLon=8.962652968749989&bottomLeftLat=28.636584579286538&bottomLeftLon=-26.32543296874999&zoomLevel=5&selectedMarker=&themeCode=&selectedDestination="
    
    
    url = "https://www.kayak.pt/s/horizon/exploreapi/destinations?airport=" + airport + "&budget=&depart=" + start + "&return="+ end + \
    "&tripdurationrange=4%2C7&duration=&flightMaxStops=&stopsFilterActive=false&topRightLat=51.82490080841914&topRightLon=8.962652968749989&bottomLeftLat=28.636584579286538&bottomLeftLon=-26.32543296874999&zoomLevel=5&selectedMarker=&themeCode=&selectedDestination="
    response = requests.post(url).json()

    df = pd.DataFrame(columns=['City', 'Country', 'Duration','Price', 'Airline', 'Airport', 'Depart','Return', 'Link'])

    for i in range(len(response['destinations'])):
        destination = response['destinations'][i]
        row = list([destination['city']['name'], destination['country']['name'],
                    destination['flightMaxDuration'],
                    destination['flightInfo']['price'], destination['airline'],
                    destination['airport']['shortName'], pd.to_datetime(destination['departd']).date(),
                    pd.to_datetime(destination['returnd']).date(),
                    str('http://kayak.com'+destination['clickoutUrl'])])
        df.loc[i] = row
    
    city_mins = df.groupby(['City']).idxmin().astype(int)
    df['MinPrice'] = df.loc[city_mins['Price'].to_list()].Price
    df['is_MinPrice'] = df['Price'].eq(df['MinPrice']).astype(int)
    #df = df.loc[city_mins['Price'].to_list()]
    # There is a glitch where some flights are returned with unrealistically
    # prices, so we'll remove those entries.
    df = df.where(df['Price']!=999999).dropna()

    return df
  
#airport='OPO'
start='20230601'
end='20230630'

data = datetime.datetime.strptime(start, '%Y%m%d')
mes = datetime.datetime.strptime(start, '%Y%m%d').month
#calendar.month_name[data.month]
#str(data.year)

origins = ['OPO','MXP','NAP'] 
for origin in origins:
    df=scrape_kayak(start,end,origin)
    df.to_csv('data/'+strftime("%Y%m%d%H%M", gmtime())+'_'+origin+'_'+calendar.month_name[mes]+'_'+str(data.year)+'.csv',index=False)
