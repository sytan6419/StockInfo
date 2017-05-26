from bs4 import BeautifulSoup
import re
import requests
import datetime
from yahoo_finance import Share

now = datetime.datetime.now()
date_now = str(now.year)+str(now.month)+str(now.day)

def get_volume(_):
    with open ('{}_{}.txt'.format(date_now,_),'a+') as txt_file:
        for tag in soup.find_all(id="volume"):
            current_volume = (str(tag).split('>')[1]).replace('\'','')
            current_volume = (str(current_volume).split('<')[0]).replace(',','')
            txt_file.write(str(now.hour) + ':' + current_volume+'\n')
            break
    return current_volume

def print_volume(_):
    f = open('{}_{}.txt'.format(date_now,_),'r+')
    f = f.read()
    volume = {}
    vol_list = []
    time_list = []
    
    for line in f.splitlines():
        if line:
            t,v = line.split(':')
            vol_list.append(v)
            time_list.append(t)

    if len(vol_list) > 1:
        print 'time : Diff in volume'
        for trade_vol in range(1,len(vol_list)):
            diff_vol = int(vol_list[trade_vol]) - int(vol_list[trade_vol-1])
            print time_list[trade_vol] + ' : ' + str(diff_vol)
        else:
            print '\n'
    
        
def get_price():
    for tag in soup.find_all(id="price"):
        current_price = (str(tag).split('>')[1]).replace('\'','')
        current_price = (str(current_price).split('<')[0]).split()[0]
        break  
    return current_price

def get_change():
    for tag in soup.find_all(id="priceDiff"):
        current_change = (str(tag).split('>')[1]).replace('\'','')
        current_change = (str(current_change).split('<')[0])
        break
    return current_change

def get_high_low():
    for tag in soup.find_all(id="priceHigh"):
        price_hi = (str(tag).split('>')[1]).replace('\'','')
        price_hi = (str(price_hi).split('<')[0])
        break
    for tag in soup.find_all(id="priceLow"):
        price_low = (str(tag).split('>')[1]).replace('\'','')
        price_low = (str(price_low).split('<')[0])
        break 
    return price_low+' - '+price_hi

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
    
def main():

    ##Add your stock code at here
    ##===================================
    stock = ['7160','7089','7087']
    ##===================================
    global soup
    
    for _ in stock:
        r  = requests.get(r'https://www.klsescreener.com/v2/stocks/view/{}'.format(_))
        soup = BeautifulSoup(r.content, 'html.parser')

        share = Share('{}.KL'.format(_))
        print 'Share name: ' + share.get_name() + ' (' + _ + ')'
        print 'Current Price: '+ get_price()
        print 'Chg(%): ' + get_change()
        print 'Current Volume: ' + get_volume(_)
        print 'Low/High: ' + get_high_low()
        print_volume(_)
    else:
        print '=== Completed for all ==='
    pause()
    return 0

main()
