#!/usr/bin/python
import sys
import getopt

from datetime import datetime
from datetime import date
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

m_gen_date = datetime.now()

def read_data(i_file, date_list, temp_list):
    line_cnt=0
    last_temperature=0
    f = open(i_file, 'r')

    f.seek(0,2)
    fsize = f.tell()
    f.seek(max(fsize-31*6*24*50, 0), 0)
    for line in f:
								line_cnt = line_cnt + 1

								if ( line_cnt == 1 ):
												continue
								line_split = line.split(',')
								measured = datetime( int(line_split[0]), int(line_split[1]), int(line_split[2])
																											, int(line_split[3]), int(line_split[4]), int(line_split[5]) )
								temperature = float(line_split[6])
								if ( line_cnt > 2 ):
												if ( abs(last_temperature-temperature) > 7.0 ):
																continue
								date_list.append(measured)
								temp_list.append(temperature)
								last_temperature = temperature
    f.close()

def gen_plot(title, strformat, start_date, end_date, date_list, temp_list, o_file):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.plot_date(date_list, temp_list, 'b-')
    
    formatter = mdates.DateFormatter(strformat)
    ax.xaxis.set_major_formatter(formatter)

    plt.xlim([start_date, end_date])
    fig.autofmt_xdate()

    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature(C)')
    ax.grid()
    
    plt.savefig(o_file)

def gen_date_plot(date_list, temp_list, o_file):
    print_date = m_gen_date+timedelta(days=-1)
    gen_plot(print_date.strftime('%Y-%m-%d(%a)')+' temperature', '%H:%M', m_gen_date-timedelta(days=1), m_gen_date, date_list, temp_list, o_file)
    
def gen_week_plot(date_list, temp_list, o_file):
    gen_plot('Week temperature', '%m/%d', m_gen_date-timedelta(days=7), m_gen_date, date_list, temp_list, o_file)    

def gen_month_plot(date_list, temp_list, o_file):
    gen_plot('Month temperature', '%m/%d', m_gen_date-timedelta(days=31), m_gen_date, date_list, temp_list, o_file)    

def process_arg(argv, i_file, o_dir):
    y = 0
    m = 0
    d = 0
    
    try:
        opts, args = getopt.getopt(argv,'y:m:d:i:o:',['i_file=','o_dir='])
    except getopt.GetoptError:
        print 'sys.argv[0] -y <year> -m <month> -d <day> -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-y':
            y = int(arg)
        elif opt == '-m':
            m = int(arg)
        elif opt == '-d':
            d = int(arg)    
        elif opt in ('-i', '--ifile'):
            i_file = arg
        elif opt in ('-o', '--odir'):
            o_dir = arg
    if (y > 0 or m > 0 or d > 0):
        if ( y == 0 or m == 0 or d == 0 ):
            print 'sys.argv[0] -y <year> -m <month> -d <day> -i <inputfile> -o <outputfile>'
            sys.exit(2)
        m_gen_date = datetime(y,m,d)

    return 0

def main(argv):
    i_file    = '/home/pi/www/sensor/data/sense_data.txt'
    o_dir     = '/home/pi/www/sensor/'
    date_list = []
    temp_list = []
    
    if ( process_arg(argv, i_file, o_dir) < 0 ):
        return -1

    read_data(i_file, date_list, temp_list)
    gen_date_plot(date_list, temp_list, o_dir+'temp_day.png')
    gen_week_plot(date_list, temp_list, o_dir+'temp_week.png')
    gen_month_plot(date_list, temp_list, o_dir+'temp_month.png')
    
if __name__ == '__main__':
   main(sys.argv[1:])
