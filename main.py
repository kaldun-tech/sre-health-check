from scripts.endpoint_reader import EndpointReader
import sys

def main():
    '''Main entry point'''
    endpoints = EndpointReader.read_endpoints()
    if endpoints is None:
        print('ERROR: Failed to read endpoints')
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
