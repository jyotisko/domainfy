# !/bin/python3

import socket
import requests
import optparse
import sys
from colorama import Fore


def getArguments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='target',
                      help='Specify the target domain')
    parser.add_option('-w', '--wordlist', dest='wordlist',
                      help='Specify the wordlist containing available domains.')
    (options, _) = parser.parse_args()
    if not options.target or not options.wordlist:
        print(Fore.RED + 'Please specify a target/wordlist, type -h for more info.' + Fore.RESET)
        sys.exit()
    return options.target, options.wordlist


def request(url):
    try:
        return requests.get('http://' + url)
    except requests.exceptions.ConnectionError:
        pass


def readDomains(file):
    with open(file, 'r') as f:
        wordsArr = []
        lines = f.readlines()
        for line in lines:
            word = line.strip()
            wordsArr.append(word)
        return wordsArr


def checkAvailableDomains(domains, target):
    for domain in domains:
        link = str(target) + str(domain)
        response = request(link)
        if response:
            ip = socket.gethostbyname(link)
            print(Fore.GREEN + link + ' at ' + ip)


if __name__ == "__main__":
    try:
        target, wordlist = getArguments()
        domains = readDomains(wordlist)
        checkAvailableDomains(domains, target)
    except Exception as e:
        if 'No such file or directory' in e:
            print(Fore.RED + 'Please specify the correct wordlist path.' + Fore.RESET)
        if 'KeyboardInterrupt' in e:
            print(Fore.RED + '[+] Quitting now' + Fore.RESET)
