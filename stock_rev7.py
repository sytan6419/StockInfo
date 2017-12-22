from bs4 import BeautifulSoup
import re
import requests
import datetime
import time
from yahoo_finance import Share
import os

def print_volume(_):
    try:
        f = open('{}_{}.txt'.format(date_now,stock_code),'r+').read()

        t = [line.split(':')[0] for line in f.splitlines()]
        v = [line.split(':')[1] for line in f.splitlines()]
        
        if len(v)>1:
            print 'Time : Chg in Vol'
            for inc in range(len(v)+1):
                for i,k in zip(v[inc::len(v)], v[inc+1::len(v)]):
                    print t[inc] + ' : ' + str(abs(int(i)-int(k)))
            else:
                print 'Last traded volume: ' + str(abs(int(v[-1])-int(v[-2])))
    except IOError:
        print 'File not exist!'
    except:
        print 'Fatal Error in printing volume'
    return
            
def pause():
    #programPause = raw_input("Press the <ENTER> key to continue...")
    print 'Wait 10 mins for next update!!!'
    print '\n\n'
    time.sleep(30)
    return

def get_data(item):
    now_hour = str(now.hour) if int(str(now.hour)) > 9 else '0'+str(now.hour)
    now_mins = str(now.minute) if int(str(now.minute)) > 9 else '0'+str(now.minute)

    try:
        for tag in soup.find_all(id=item):
            if item == 'volume':
                with open ('{}_{}.txt'.format(date_now,stock_code),'a+') as txt_file:
                    current_volume = tag.get_text().replace(',','')
                    txt_file.write(now_hour + now_mins + ':' + current_volume+'\n')
            return tag.get_text().split()[0]
        else:
            txt_file.close()
    except IOError:
        print 'Not able to create file.'
    except:
        print 'Fatal Error in getting data'

def display_data(stock_code):
    #share = Share(stock_code+'.KL')       
    #print 'Share name: ' + share.get_name() + ' (' +stock_code + ')'
    print 'Stock Code' + ' (' +stock_code + ')'
    print 'Current Price: '+ get_data('price')
    print 'Chg(%): ' + get_data('priceDiff')
    print 'Traded Volume: ' + get_data('volume')
    print 'Low/High: ' + get_data('priceLow') + '/' + get_data('priceHigh')
    print_volume(stock_code)
    print '\n'

    return

def main():

    print '====== Welcome to stock tracking tool ======'
    print '====== This tool will update on interval of 10 mins ====='

    init_flag = 0
    while(True):
        ##Add your stock code at here
        ##stock = ['<code>:<market_share>']
        ##=======================================
        stock_list = ['7160','3204']
        ##=======================================
        global soup
        global stock_code
        global date_now
        global now


        now = datetime.datetime.now()
        date_now = str(now.year)+str(now.month)+str(now.day)

        if (now.hour == 17 and now.minute == 01 and now.second == 0):
            print 'End of Trading dayyyy.'
            break;
            
        #check trading hours and set interval for the data pulling
        if (now.hour >= 9 and now.hour <= 12) or (now.hour >= 14 and now.hour <= 17):
            if not init_flag:
                for stock_code in stock_list:
                    r  = requests.get(r'https://www.klsescreener.com/v2/stocks/view/'+stock_code)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    display_data(stock_code)
                    init_flag = 1
                else:
                    pause()
                
            if now.minute % 10 == 0 and now.second == 0 and now.microsecond == 0:
                os.system('cls')
                print now
                for stock_code in stock_list:
                    r  = requests.get(r'https://www.klsescreener.com/v2/stocks/view/'+stock_code)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    display_data(stock_code)
                else:
                    pause()
        else:
            print 'Not in trading hour...'
            exit(0)
    return

main()               
exit(0)
