import json
import requests
import pandas as pd
import calendar
from datetime import datetime
from datetime import date
from time import gmtime, strftime
import glob
import os
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl 

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
    
    format = "%Y%m%d"
    res = False
    try:
        res = bool(datetime.strptime(start, format))
    except ValueError:
        res = False
    if res: 
        #print(res)
        url = "https://www.kayak.pt/s/horizon/exploreapi/destinations?airport=" + airport + "&budget=&depart=" + start + "&return="+ end + "&tripdurationrange=4%2C7&duration=&flightMaxStops=&stopsFilterActive=false&topRightLat=51.82490080841914&topRightLon=8.962652968749989&bottomLeftLat=28.636584579286538&bottomLeftLon=-26.32543296874999&zoomLevel=5&selectedMarker=&themeCode=&selectedDestination="
    else: 
        url = "https://www.kayak.pt/s/horizon/exploreapi/destinations?airport=" + airport + "&budget=&tripdurationrange=4%2C7&duration=&flightMaxStops=&stopsFilterActive=false&topRightLat=51.82490080841914&topRightLon=8.962652968749989&bottomLeftLat=28.636584579286538&bottomLeftLon=-26.32543296874999&zoomLevel=5&selectedMarker=&themeCode=&selectedDestination="
    
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
  
    
def generate_baseline(city):
    """
    This function loads all files from a city origin stored in folder 'data' and generates a new baseline file, i.e. a file with the minimum prices for each route and month.
    The next step after this will be to upload this to a BigQuery database.
    Parameters:
    city: 
    Returns:
    A data frame containing all destination cities and minimum historical prices for each route.
    """
    all_files = glob.glob("data/*"+city+"*.csv")
    df = pd.DataFrame()
    #loop through all the files and store them in the dataframe
    for f in all_files:
        file_name = f.split("/")[-1]
        filename = file_name.split(".")[0]
        df_temp = pd.read_csv(f)
        df_temp["filename"] = filename
        df = df.append(df_temp)
    #reorder the columns
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    
    df['date_query'] = pd.to_datetime(df['filename'].str[:11], format='%Y%m%d%H%M')
    df['year_query'] = pd.DatetimeIndex(df['date_query']).year
    df['month_query'] = pd.DatetimeIndex(df['date_query']).month
    df['day_query'] = pd.DatetimeIndex(df['date_query']).day
    df['weekday_query'] = pd.DatetimeIndex(df['date_query']).weekday
    df['hour_query'] = pd.DatetimeIndex(df['date_query']).hour
    df['year_depart'] = pd.DatetimeIndex(df['Depart']).year
    df['month_depart'] = pd.DatetimeIndex(df['Depart']).month
    df['days_advance'] = pd.to_datetime(df['Depart'], infer_datetime_format=True)-pd.to_datetime(df['date_query'], infer_datetime_format=True)
    df['CityOrigin'] = city

    baseline = df.query("Depart >= date_query").groupby(['City','Country','year_depart','month_depart']).agg(minPrice=('Price', 'min'),meanPrice=('Price', 'mean'),medianPrice=('Price', 'median')).sort_values(['minPrice'],ascending=True).reset_index()
    #menoresprecos=df.query("Depart >= dateQuery").groupby(['City','Country','year_depart','month_depart']).agg({'Price': lambda x: (x < min(x)*1.2).sum()})
    #baselineOPO = baselineOPO.join(menoresprecos, rsuffix='_minPrices').reset_index().rename(columns={'Price': 'inside20pct'})
    baseline.insert(0, 'CityOrigin', city)
    baseline['timestamp'] = datetime.now()
    baseline['timestamp']  = baseline['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    return(baseline)

def compare_prices(newdf,basedf,city):
    
#     file=filename.replace(".csv","")
#     data = pd.read_csv(filename)
    newdf.sort_values(by=['Price'],ascending=True)
    newdf['year_depart'] = pd.DatetimeIndex(newdf['Depart']).year
    newdf['month_depart'] = pd.DatetimeIndex(newdf['Depart']).month

    compare = pd.merge(newdf, basedf, on=['City', 'Country', 'month_depart', 'year_depart'],how='left')
    compare['is_smaller'] = compare['Price'] < compare['minPrice']
    compare['difPrice'] = (compare['Price'] -compare['minPrice'])
    compare['difPricePct'] = ((compare['Price'] -compare['minPrice']) / compare['minPrice'])*100
    smaller = compare.query("is_smaller").sort_values('difPricePct')

    smallerUnder100=len(smaller.query("Price <= 100"))
    smallerUnder50=len(smaller.query("Price <= 50"))

    summarydf=pd.DataFrame(columns=['Date', 'CityOrigin', 'SmallerPrices', 'SmallerUnder100', 'SmallerUnder50'])
    summarydf.loc[0] = [date.today(), city,  len(smaller), smallerUnder100, smallerUnder50]
    
    return(smaller,summarydf)

def send_mail(smallerprices,summarydf,city):
    
    tableSummary = summarydf.to_html()
# tableUnder20pct = df.query("difPricePct < -20").loc[:,["CityOrigin","City","Country","Depart","Return","Price","minPrice","difPrice","difPricePct"]].reset_index(drop=True).to_html(formatters={
#     'difPricePct': '{:,.2f}'.format,
#     'difPrice': '€{:,.2f}'.format
# })
    tableUnder100 = smallerprices.query("difPricePct < 0 & Price < 100").loc[:,["CityOrigin","City","Country","Depart","Return","Price","minPrice","difPrice","difPricePct","Link"]].reset_index(drop=True).sort_values('Depart').to_html(formatters={
        'difPricePct': '{:,.2f}%'.format,
        'difPrice': '{:,.2f}'.format,
        'Price': '€{:,.2f}'.format,
        'minPrice': '€{:,.2f}'.format},render_links=True)
    sender = 'rafabelokurows@gmail.com'
    recipient = 'rafabelokurows@gmail.com'
    #password = input(str('Enter your password: '))
    password = os.getenv('APP_PASSWORD') #change this when pushin to Github
    subject = 'Deals on airline tickets out of '+city
    
    textBefore = "<p>Hey, check out this new deals I've found for airline tickets out of "+city+".</p>This is the summary of the last run:\n"
    textMiddle = "<p>\nFlights below are the best price yet for these routes (on each specific month) and under 100 Euros!</p>\n"
    html = textBefore + tableSummary + textMiddle + tableUnder100

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(html, 'html'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,password)
        smtp.sendmail(sender,recipient,message.as_string())

    print('Email with deals sent to ',recipient)
    
    
#airport='OPO'
#start='20230601'
#end='20230630'
#data = datetime.strptime(start, '%Y%m%d')
#mes = datetime.strptime(start, '%Y%m%d').month
#calendar.month_name[data.month]
#str(data.year)

origins = ['OPO','MXP','NAP','LIS','MAD'] 
for origin in origins:
    #df=scrape_kayak(start,end,origin)
    df = scrape_kayak(airport = origin)
    #df.to_csv('data/'+strftime("%Y%m%d%H%M", gmtime())+'_'+origin+'_'+calendar.month_name[mes]+'_2023'+'.csv',index=False)
    df.to_csv('data/'+strftime("%Y%m%d%H%M", gmtime())+'_'+origin+'_2023.csv',index=False)
    baseline = generate_baseline(city = origin)
    a,b = compare_prices(newdf = df, basedf = baseline, city = origin)
    baseline.to_csv('data/baseline_'+strftime("%Y%m%d%H%M", gmtime())+'_'+origin+'_2023.csv',index=False)
    a.to_csv('data/smallerprices_'+strftime("%Y%m%d%H%M", gmtime())+'_'+origin+'_2023.csv',index=False)
    b.to_csv('data/summary_'+strftime("%Y%m%d%H%M", gmtime())+'_'+origin+'_2023.csv',index=False)
    send_mail(smallerprices = a,summarydf = b,city = origin)
