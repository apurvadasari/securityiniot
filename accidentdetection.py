import smbus
import time
import serial              
import webbrowser           
import sys  
from http.server import BaseHTTPRequestHandler, HTTPServer
bus = smbus.SMBus(1)

bus.write_byte_data(0x5C, 0x20, 0x90)

time.sleep(0.1)

data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)

# Convert the data to hPa
pressure = (data[2] * 65536 + data[1] * 256 + data[0]) / 4096.0

# Output data to screen
print("Barometric Pressure is : %.2f hPa" %pressure)
ser = serial.Serial (“/dev/ttyS0”)
gpgga_info = “$GPGGA,”
GPGGA_buffer = 0
NMEA_buff = 0

if pressure> 18000 and pressure<25000:
    GPS_info()
    class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        messagetosend = bytes('Hello',"utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        Request = self.requestline
        Request = Request[5: int(len(Request)-9)]
        print(Request)
        if Request=='dontsend':
            #dontsendsms
            print("USER DENIED")
        else:
            #sendsms
            #return
        return
    server_address_httpd = ('127.0.0.1',8080)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
    print('Starting server')
    httpd.serve_forever()



def GPS_info():
    try:
        while True:
            received_data = (str)(ser.readline()) #read NMEA string received
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
            if (GPGGA_data_available>0):
                GPGGA_buffer = received_data.split(“$GPGGA,”,1)[1]  #store data coming after “$GPGGA,” string
                NMEA_buff = (GPGGA_buffer.split(‘,’))
                nmea_time = []
                nmea_latitude = []
                nmea_longitude = []
                nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
                nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                print(“NMEA Time: “, nmea_time,’\n’)
                lat = (float)(nmea_latitude)
                lat = convert_to_degrees(lat)
                longi = (float)(nmea_longitude)
                longi = convert_to_degrees(longi)
                print (“NMEA Latitude:”, lat,”NMEA Longitude:”, longi,’\n’)           

    except KeyboardInterrupt:
        sys.exit(0)



def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value – int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = “%.4f” %(position)
    return position

