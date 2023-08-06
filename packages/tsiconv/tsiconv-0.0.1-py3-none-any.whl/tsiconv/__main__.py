#from __future__ import (print_function, unicode_literals, division, absolute_import)
__metaclass__ = type
__package_name__ = 'tsiconv'

## Standard Libraries
import sys
import argparse
import logging
from pprint import pprint

## Third Party libraries
import pkg_resources
import pytz
from dateutil.parser import isoparse

C_ERR_USAGE = 1

## Load up some metadata
try:
    __code_name__  = __package_name__
    # spacing is deliberate
    __code_desc__ = """ a program to convert timezones \n    ex: python {name}
        """.format(name=str(__package_name__)+'.py')
    _distro = pkg_resources.get_distribution(__package_name__)
    __code_version__ = _distro.version
    __code_meta__ = vars(_distro)
    __code_debug__ = False
except pkg_resources.DistributionNotFound:
    # when debugging with vscode
    __code_debug__ = True
    stubs = [ '__code_version__', '__code_meta__']
    for s in stubs:
        globals()[s] = 'Not Available'

def isNaive(t):
    if t.tzinfo is None or t.tzinfo.utcoffset(t) is None:
        return True
    else:
        return False

def isAware(t):
    if t.tzinfo is not None and t.tzinfo.utcoffset(t) is not None:
        return True
    else:
        return False

def naiveToAware(dt, tz):
    src = pytz.timezone(tz)
    return dt.astimezone(src)

def handle_user_time(t, verbose, log):
    """ Parse the  time using ISO-8601; then determine if naive/aware """
    # convert user input
    dt = isoparse(t)
    dt_f = None                 # how to handle the datetime
    dt_n = isNaive(dt)          # check if naive
    dt_a = isAware(dt)          # check if aware
    if verbose:
        log.info(f"[*] Checking if {dt} is a Naive or Aware format")

    if dt_n:
        dt_f = 'naive'
        if verbose:
            log.info(f"[*] {dt} is a Naive format: {dt_n}")
    elif dt_a:
        dt_f = 'aware'
        if verbose:
            log.info(f"[*] {dt} is an Aware format: {dt_a}")
    else:
        # panic?
        msg = "Unable to detect naive/aware format for {dt}"
        raise ValueError(msg)

    return dt, dt_f

def naiveToUTC(dt, tz):
    dtz = naiveToAware(dt, tz)
    utz = awareToUTC(dt)
    return utz

def awareToUTC(dt):
    return dt.astimezone(pytz.utc)

def convertTime(dt, tz):
    dst = pytz.timezone(tz)
    return dt.astimezone(dst)

def print_12h(dt):
    print(to12h(dt))

def print_24h(dt):
    print(to24h(dt))

def to12h(dt, fmt='%Y-%m-%d %I:%M:%S %p'):
    return dt.strftime(fmt)

def to24h(dt, fmt='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(fmt)

def usage_list():
    for i in pytz.all_timezones:
        print(i)
    sys.exit(C_ERR_USAGE)

def print_usage_and_exit(parser, msg):
    if msg:
        print(msg)
    parser.print_help()
    sys.exit(C_ERR_USAGE)

def begin_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            style="{",
            fmt="[{name}:{filename}] {levelname} - {message}"
        )
    )
    log = logging.getLogger(__package_name__)
    if __code_debug__:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    log.addHandler(handler)
    return log

def collect_args():
    parser = argparse.ArgumentParser(description=__code_desc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-t', '--time', action='store', required=True, help="A datetime to convert. This should be in ISO-8601 format")
    parser.add_argument('-s', '--source', action='store', help="A source timezone to translate from. Only required if --time is a naive format")
    parser.add_argument('-d', '--destination', action='store', help="A destination timezone to translate from")
    parser.add_argument('-l', '--list', action='store_true', help="List out the timezones supported by this application")
    args = parser.parse_args()
    return parser, args

def handle_args():
    # collect parser if needed to conditionally call usage: parser.print_help()
    parser, args = collect_args()

    # print out timezones?
    if args.list:
        usage_list()

    # validate arguments

    if args.source:
        if args.source not in pytz.all_timezones:
            msg  = f"[!] Provided argument {args.source} not a supported timezone\n"
            msg += f"[!] Consider using the -l option\n"
            print_usage_and_exit(parser, msg)

    if args.destination:
        if args.destination not in pytz.all_timezones:
            msg  = f"[!] Provided argument {args.destination} not a supported timezone\n"
            msg += f"[!] Consider using the -l option\n"
            print_usage_and_exit(parser, msg)

    return parser, args

def main():
    log = begin_logging()
    parser, args = handle_args()

    try:
        # Capture user input, convert to UTC
        dt, na = handle_user_time(args.time, args.verbose, log)
        assert na in ['naive', 'aware']
        if na == 'naive':
            if args.source is None:
                msg = "[!] A naive timestamp was provided with no identifying timezone information. See option -s"
                print_usage_and_exit(parser, msg)
            utctime = naiveToUTC(dt, args.source)
        else:
            utctime = awareToUTC(dt)

        # Convert UTC into requested timezone
        if args.destination:
            dsttime = convertTime(utctime, args.destination)

        # Print results
        print(f"[*] Args:")
        if args.source:
            if na == 'naive':
                print(f"[*] source: {args.source}")
            else:
                print(f"[*] source: {args.source} [IGNORED]")
        if args.destination:
            print(f"[*] destination: {args.destination}")
        print(f"[+] Input  24h: {to24h(dt)}")
        print(f"[+] Input  12h: {to12h(dt)}")
        print(f"[+] UTC    24h: {to24h(utctime)}")
        print(f"[+] UTC    12h: {to12h(utctime)}")
        if args.destination:
            print(f"[+] Output 24h: {to24h(dsttime)}")
            print(f"[+] Output 12h: {to12h(dsttime)}")

    except Exception as e:
        pprint(e)
        raise e
    finally:
        pass

if __name__=="__main__":
    main()
