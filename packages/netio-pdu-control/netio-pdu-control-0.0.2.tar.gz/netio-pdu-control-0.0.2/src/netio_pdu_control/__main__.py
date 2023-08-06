import argparse
from os.path import isfile
from netio_pdu_control.NetioClient import Client
import sys
import configparser
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description='Netio control script')
    parser.add_argument('-c', '--credentials', help='Credentials file path.',
                        default="credentials.cfg")
    parser.add_argument('-d', '--device',
                        help='Device name as in the credentials file.')
    parser.add_argument('-s', '--socket', required=any(x in sys.argv for x in ['--action', '-a ']),
                        help='Socket outlet identifier.', type=int)
    parser.add_argument('-a', '--action', choices=['power', 'cycle',
                        'toggle'], required=any(x in sys.argv for x in ['--socket', '-s ']), type=str.lower,
                        help='''power: sets the socket state according to --state.\n'''
                        '''cycle: sets the socket state according to --state for '''
                        '''--time miliseconds and then toggles the state.\n'''
                        '''toggle: flips the socket state.''')
    parser.add_argument('-S', '--state', choices=['on', 'off', 'true', 'false'],
                        required=any(x in sys.argv for x in [
                                     'power', 'cycle']),
                        type=str.lower, help='Boolean state of a socket.')
    parser.add_argument('-t ', '--time', required='cycle' in sys.argv,
                        type=int, help='Time duration in milliseconds.')
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    args.state = (lambda x: True if (
        x == "on" or x == "true") else False)(args.state)
    return args


def get_config(args):
    if not isfile(args.credentials):
        raise argparse.ArgumentTypeError("Configuration file not found.")
    config = configparser.ConfigParser()
    config.read(args.credentials)
    devices = [k for k in config.keys() if k != "DEFAULT"]
    device = devices[0] if (args.device is None) and (
        len(devices) == 1) else args.device
    if device is None:
        raise argparse.ArgumentTypeError("Device name not specified.")
    try:
        device_config = config[device]

        wlogin = (device_config["WriteUser"], device_config["WritePassword"])
        rlogin = (device_config["ReadUser"], device_config["ReadPassword"])
        address = device_config["EntryPoint"]
    except KeyError as e:
        raise argparse.ArgumentTypeError(
            "Configuration file illformed: "+str(e)) from None
    return rlogin, wlogin, address


args = parse_arguments()
rlogin, wlogin, address = get_config(args)
c = Client(read_login=rlogin, write_login=wlogin,
           address=address)

result = None
if args.action is None:  # Read Mode
    result = c.status()
else:  # Write Mode
    if args.action == "power":
        result = c.set_power(args.socket, args.state)
    elif args.action == "cycle":
        result = c.set_power_period(args.socket, args.state, args.time)
    else:
        result = c.toggle_power(args.socket)
print(json.dumps(result, sort_keys=True, indent=4))
