"""Class to test dns lookups and show good/bad hits"""
import socket
from time import sleep
import curses

class dnsTroubleShoot:
    """Test out dns lookups continously and get info on the lookups failing or succeeding"""
    ok_count=0
    resolve_error_count=0
    lookup_dict_ok={}
    lookup_dict_fail={}
    last_error={}

    domains=[]
    number_of_requests = int()

    def __init__(self,domains, number_of_requests=100) -> None:
        """
            domains: A list with domains i.e. ["num1.com","num2.com"]
            number_of_requests: the number of times to look up the domain
        """
        self.domains = domains
        self.number_of_requests = number_of_requests
        self.init_counters()
        self.do_lookups()
    
    def init_counters(self):
        for domain in self.domains:
            self.lookup_dict_fail[domain] = 0
            self.lookup_dict_ok[domain] = 0
            self.last_error[domain] = ""

    def do_lookups(self):
        self.stdscr = curses.initscr()
        lookup_dict={}
        for i in range(0, self.number_of_requests):
            for domain in self.domains:
                self.resolve_hostname(domain)
            sleep(1)
            self.stdscr.refresh()
            
            self.show_counts()
        curses.endwin()

    def show_counts(self):
        output=""
        line=0
        self.stdscr.addstr(line,0,f"Testing {len(self.domains)} domains")
        for domain in self.domains:
            line += 1
            self.stdscr.addstr(line,0,f"{domain} OK/NOK: {self.lookup_dict_ok[domain]}/{self.lookup_dict_fail[domain]} {self.last_error[domain]}\n")
            

    def resolve_hostname(self,hostname):
        try:
            ipinfo = socket.getaddrinfo(hostname,0)
            self.ok_count += 1
            self.lookup_dict_ok[hostname] += 1
            return(ipinfo[0][4])
        except socket.gaierror as e:
            self.resolve_error_count += 1
            self.lookup_dict_fail[hostname] += 1
            self.last_error[hostname] = f"Last error: {e}"
            

domains = ['dr.dk','google.com']
ts = dnsTroubleShoot(domains,200)
