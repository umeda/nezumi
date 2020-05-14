#!/usr/bin/python

DUMMY_MODE = False

if not DUMMY_MODE:
    import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pprint import pprint

TIME_CELLS = 'A2:A289'
TEMP_1_CELLS = 'B2:B289'
TEMP_2_CELLS = 'F2:F289'
TEMP_3_CELLS = 'J2:J289'
HUMIDITY_1_CELLS = 'D2:D289'
HUMIDITY_2_CELLS = 'H2:H289'
HUMIDITY_3_CELLS = 'L2:L289'



def update_column(sheet, cell_range, new_value):
    cells = sheet.range(cell_range)
    col_num = ord(cell_range[0])-64
    # print('cell_range = ', cell_range)
    # print('col_num = ', col_num)
    new_cell = gspread.Cell(289, col_num, value=new_value)
    for index in range(len(cells)):
        if index is not 0:
            cells[index - 1].value = cells[index].value
    # pprint(cells)
    cells[-1] = new_cell
    # pprint(cells)
    resp = sheet.update_cells(cells, value_input_option='USER_ENTERED')
    # resp = sheet.update_cells(cells, value_input_option='RAW')
    # resp = sheet.update_cells(cells)
    print(resp)


if not DUMMY_MODE:
    sensor_22 = Adafruit_DHT.DHT22
    sensor_11 = Adafruit_DHT.DHT11

vent_pin = 4
room_pin = 17
back_pin = 22

if not DUMMY_MODE:
    vent_humidity, vent_temperature = Adafruit_DHT.read_retry(sensor_22, vent_pin)
    room_humidity, room_temperature = Adafruit_DHT.read_retry(sensor_11, room_pin)
    back_humidity, back_temperature = Adafruit_DHT.read_retry(sensor_11, back_pin)
else:
    vent_temperature = 11.0
    vent_humidity = 12.0
    room_temperature = 13.0
    room_humidity = 14.0
    back_temperature = None
    back_humidity = None

if vent_temperature is not None:
    vent_temperature = vent_temperature * 9 / 5 + 32
if room_temperature is not None:
    room_temperature = room_temperature * 9 / 5 + 32
if back_temperature is not None:
    back_temperature = back_temperature * 9 / 5 + 32

if vent_humidity is not None and vent_temperature is not None:
    print('Vent: Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(vent_temperature, vent_humidity))
else:
    print('Failed to get vent reading')
    vent_humidity = ''
    vent_temperature = ''

if room_humidity is not None and room_temperature is not None:
    print('Room: Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(room_temperature, room_humidity))
else:
    print('Failed to get room reading')
    room_humidity = ''
    room_temperature = ''

if back_humidity is not None and back_humidity is not None:
    print('Back: Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(back_temperature, back_humidity))
else:
    print('Failed to get back reading')
    back_humidity = ''
    back_temperature = ''

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/ac_log/ac logger-xxxxxxxxxxxx.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open("ac_performance").sheet1
update_column(spreadsheet, TIME_CELLS, str(datetime.utcnow()))
update_column(spreadsheet, TEMP_1_CELLS, str(vent_temperature))
update_column(spreadsheet, TEMP_2_CELLS, str(room_temperature))
update_column(spreadsheet, TEMP_3_CELLS, str(back_temperature))
update_column(spreadsheet, HUMIDITY_1_CELLS, str(vent_humidity))
update_column(spreadsheet, HUMIDITY_2_CELLS, str(room_humidity))
update_column(spreadsheet, HUMIDITY_3_CELLS, str(back_humidity))
