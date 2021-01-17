import RPi.GPIO as GPIO
import smtplib
from time import sleep
from time import time
import datetime
from os import path
from json import load
# 0 = open

LED_PIN = 4
CONTROLLER_LED = 21
ZONES = {17: 'controller button',
         27: 'garage door',
         22: 'front door',
         5: 'bedroom windows',
         6: 'back door',
         13: 'back windows',
         19: 'front windows',
         26: 'side door'}

ENABLED = True
curr_state = ''
EVENT_HISTORY = []
events_files = ''

"""
email.json should look somethng like this:
{
    "email_username":"<sender_username>",
    "email_password":"<sender_password>",
    "email_server":"<smtp_server>"
}
"""
with open('/home/pi/email.json') as f:
    email_data = load(f)
EMAIL_USER = email_data['email_username']
EMAIL_PASS = email_data['email_password']
SMTP_SERVER = email_data['email_server']

def log_event(pin):
    global events_files
    init_time = time()
    time_sequence = []
    # print('initial time = ' + str(init_time))
    while time() - init_time < 1.0:
        sleep(0.05)
        # print(time() - init_time)
        time_sequence.append(GPIO.input(pin))
        log_event_state()
    ts = datetime.datetime.fromtimestamp(init_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(str(ts) + ' ' + ZONES[pin] + ', pin ' + str(pin) + ' ' + str(time_sequence))
    EVENT_HISTORY.append(str(ts) + ' ' + ZONES[pin] + ', pin ' + str(pin) + ' ' + str(time_sequence))
    return str(time_sequence)

def gen_events_header():
    global events_files
    header = 'time, '
    for zone_number, zone_name in ZONES.items():
        header += str(zone_number) + ': ' + zone_name + ', '
    events_files.write(header[:-2] + '\n')
    events_files.flush()


def log_event_state():
    global ZONES
    event_status_string = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    event_status_string += ', '
    for zone_number, zone_name in ZONES.items():
        event_status_string += str(GPIO.input(zone_number)) + ', '
    events_files.write(event_status_string[:-2] + '\n')
    events_files.flush()


def get_state():
    global ZONES
    status_string = ''
    for zone_number, zone_name in ZONES.items():
        status_string += str(GPIO.input(zone_number))
    return status_string


def get_state_details():
    global ZONES
    status_string = ''
    for zone_number, zone_name in ZONES.items():
        status_string += str(GPIO.input(zone_number)) + zone_name + '\n'
    return status_string


def send_alert(title, alert_msg):

    SMTP_PORT = 587

    sender = EMAIL_USER
    recipient = EMAIL_USER
    subject = title
    body = alert_msg

    body = "" + body + ""

    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    # print(SMTP_SERVER)
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # print(sender)
    # print(EMAIL_PASS)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(sender, EMAIL_PASS)

    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()

    # try:
    #     refused = server.sendmail(from_addr, to_addr, msg)
    # except smtplib.SMTPRecipientsRefused as e:
    #     # print('got SMTPRecipientsRefused', file=DEBUGSTREAM)
    #     print('got SMTPRecipientsRefused')
    #     refused = e.recipients
    # except (OSError, smtplib.SMTPException) as e:
    #     # print('got', e.__class__, file=DEBUGSTREAM)
    #     print('got', e.__class__)
    #     # All recipients were refused.  If the exception had an associated
    #     # error code, use it.  Otherwise,fake it with a non-triggering
    #     # exception code.
    #     errcode = getattr(e, 'smtp_code', -1)
    #     errmsg = getattr(e, 'smtp_error', 'ignore')
    #     print(str(errcode))
    #     print(str(errmsg))
    #     # for r in rcpttos:
    #     #    refused[r] = (errcode, errmsg)
    # server.quit()
    print('sent')


def send_alert_to(to_addr, title, alert_msg):
    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    message = alert_msg
    msg = 'Subject: {}\n\n{}'.format(title, message)
    from_addr = EMAIL_USER
    # TODO: catch email failures and requeue!
    print('send now')
    try:
        server.sendmail(from_addr, to_addr, msg)
    except:
        print('dang email')
    server.quit()
    print('sent')


def zone_event(pin):
    global curr_state
    if GPIO.input(pin):
        open_zone_event(pin)
    else:
        close_zone_event(pin)


def open_zone_event(pin):
    global ZONES
    global ENABLED
    global curr_state
    global trigger_files
    # trigger_string = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    time_string = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # trigger_string += ', '
    # for zone_number, zone_name in ZONES.items():
    #     if zone_number == pin:
    #         trigger_string += 'C, '
    #     else:
    #         trigger_string += 'X, '
    # events_files.write(trigger_string[:-2] + '\n')
    # events_files.flush()
    if pin is not 17:
        time_sequence = log_event(pin)
        # TODO: use this to check if we've really got a trigger!
        new_state = get_state()
        print('transition')
        title = 'Open event detected on  ' + ZONES[pin] + ', pin: ' + str(pin) + '\n'  # this CR is required for some reason
        msg = time_string + '\n' + curr_state + '\n' + new_state + '\n'
        msg += get_state_details()
        msg += '\n\n\nPin Stability: ' + time_sequence + '\n'
        print(title)
        print(msg)
        if ENABLED and (new_state != curr_state):
            if curr_state == '0010000':
                print('!!!!!!!')
                # send_alert_to(EMAIL_USER, EMAIL_USER, title, msg)
                #send_alert_to(EMAIL_USER, EMAIL_USER, 'test', 'check doors')
                send_alert(title, msg)
            else:
                send_alert(title, msg)
        curr_state = new_state


def close_zone_event(pin):
    global ZONES
    global ENABLED
    global curr_state
    global events_files
    # trigger_string = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    time_string = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # trigger_string += ', '
    # for zone_number, zone_name in ZONES.items():
    #     if zone_number == pin:
    #         trigger_string += 'C, '
    #     else:
    #         trigger_string += 'X, '
    # events_files.write(trigger_string[:-2] + '\n')
    # events_files.flush()
    if pin is 17:
        print('Controller button pressed - waiting a second.')
        sleep(1)
        if not GPIO.input(pin):
            ENABLED = not ENABLED
            msg = 'Alarm has been DISABLED'
            if ENABLED: msg = 'Alarm has been ENABLED'
            print(msg)
            print('sending message')
            send_alert('System Status', msg)
    else:
        time_sequence = log_event(pin)
        # TODO: use this to check if we've really got a trigger!
        new_state = get_state()
        print('transition')
        title = 'Closed event detected on  ' + ZONES[pin] + ', pin: ' + str(pin) + '\n'  # this CR is required for some reason
        msg = time_string + '\n' + curr_state + '\n' + new_state + '\n'
        msg += get_state_details()
        msg += '\n\n\nPin Stability: ' + time_sequence + '\n'
        print(title)
        print(msg)
        # TODO: Give overall status
        if ENABLED and (new_state != curr_state):
            send_alert(title, msg)
        curr_state = new_state

# have a norun file for testing
if path.isfile('/home/pi/norun'):
    exit()

print('setting up files')
#for key, items in ZONES:
#    events_files.update({key: open('event' + str(key) + '.csv', 'w')})
#    trigger_files_files.update({key: open('trigger' + str(key) + '.csv', 'w')})
events_files = open('events.csv', 'w')
gen_events_header()

print('setting up GPIO')
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(CONTROLLER_LED, GPIO.OUT)
for zone_number, zone_name in ZONES.items():
    GPIO.setup(zone_number, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
curr_state = get_state()

print('set up interrupts')
for zone_number, zone_name in ZONES.items():
    GPIO.add_event_detect(zone_number, GPIO.BOTH, callback=zone_event, bouncetime=1)

print('flash LED for a while')
send_alert('System Status', 'Alarm System Started')

try:
    while True:
        GPIO.output(LED_PIN, True)
        if ENABLED: GPIO.output(CONTROLLER_LED, True)
        # print('on  ')
        sleep(0.5)
        GPIO.output(LED_PIN, False)
        GPIO.output(CONTROLLER_LED, False)
        sleep(0.5)
        # TODO: Exit on stop file.
        # TODO: Periodically send out an I am awake email.
        # TODO: Reboot at midnight.
        # TODO: Respond to query emails.
        # TODO: Send text on first open.
        # TODO: Add time tag to mail.
        # TODO: Start a retry thread.
        # TODO: Add recipient field to send mail.
        # TODO: Enable/Disable by email.
        # TODO: Send Status once per hour.

except KeyboardInterrupt:
    print('Exited with ctrl-c.')

except:
    print('Some other error')

finally:
    GPIO.cleanup()
    events_files.close()

GPIO.cleanup
events_files.close()

