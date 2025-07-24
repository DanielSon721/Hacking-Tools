These are my hacking tools made in Python!

NMAP SCANNER:

This script scans the inputted IP address to check its status (up/down), open ports, and the operating system that it is running on.

This script should be used with the following Linux command:

sudo python3 scanner.py [TARGET_IP_ADDRESS]

KEYLOGGER:

This code captures your keystrokes and writes them to a local text file. Every 10 key strokes, the program discreetly sends the data to an attacker machine via Metasploit.

The receiver.py must be running on the attacker machine and keylogger.py must be running on the victim machine.

The attacker machine will see a file named keylog.txt containing the exfiltrated keystrokes.

BRUTE FORCE PASSWORD CRACKER:

This script brute forces password guessing, testing over 80 million combinations in the span of 10 seconds.
