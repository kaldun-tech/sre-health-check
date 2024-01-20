'''SRE health check main functionality'''
from argparse import ArgumentParser
from pynput import keyboard
import sys
import time
from scripts.endpoint_reader import read_endpoints
from scripts.http_requests import HTTPRequester
from scripts.availability import AvailabilityMetrics

class RunState:
    '''Class to hold run state'''
    def __init__(self):
        self.is_running = True

    def is_running(self):
        '''Checks whether program should continue to run'''
        return self.is_running

    def pause(self):
        '''Pauses program'''
        self.is_running = False
        print('Program paused, press space to resume or Esc to quit...')

    def resume(self):
        '''Resumes execution'''
        self.is_running = True
        print('Execution resumed, press p to pause or Esc to quit...')

    def on_release(self, key):
        '''Listens for key press'''
        if key == keyboard.Key.esc or key.char == 'x':
            # Exit
            sys.exit(0)
        elif key == keyboard.Key.pause or key.char == 'p':
            self.pause()
        elif key == keyboard.Key.space or key.char == ' ':
            self.resume()


def do_query_report(metrics : AvailabilityMetrics, endpoints : dict):
    '''Query and report on endpoints'''
    responses = HTTPRequester.query_endpoints(endpoints)
    metrics.update_for_list(responses)
    metrics.report_metrics()

def main():
    '''Main entry point'''
    parser = ArgumentParser(description='Query and report on endpoints')
    parser.add_argument('-f', '--filename', type=str, help='YAML file containing endpoint definitions', required=False)
    args = parser.parse_args()

    endpoints = read_endpoints(args.filename)
    if endpoints is None:
        print('ERROR: Failed to read endpoints')
        sys.exit(1)

    print(f'Found {len(endpoints)} endpoints')
    state = RunState()
    sleeptime = 15
    metrics = AvailabilityMetrics()

    listener = keyboard.Listener(on_release=state.on_release)
    listener.start()

    print(f'Program will query endpoints and report results every {sleeptime} seconds, press p to pause or x to quit...')
    while True:
        if state.is_running:
            do_query_report(metrics, endpoints)
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
