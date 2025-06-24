import nmap
import pandas as pd
import sys
import time

def nmap_scan(target, scanner):
    scanner.scan(target, arguments="-F")
    results = []
    
    for host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            for port in scanner[host][proto].keys():
                port_data = scanner[host][proto][port]
                reason = port_data.get('reason', 'N/A')
                results.append({
                    "Host": host,
                    "Port": port,
                    "Protocol": proto,
                    "State": port_data["state"],
                    "Method": f"{reason}"
                })
    return pd.DataFrame(results)

def os_detection_scan(target, scanner):
    try:
        result = scanner.scan(target, '5000', arguments='-O')
        if 'osmatch' in result['scan'][target] and result['scan'][target]['osmatch']:
            guessed_os = result['scan'][target]['osmatch'][0]
            accuracy = guessed_os.get('accuracy', '?')
            name = guessed_os.get('name', 'Unknown OS')
            print(f"\nThere is a {accuracy}% chance that the host is running {name}.\n")
        else:
            print("\nOS detection failed or returned no results.\n")
    except Exception as e:
        print(f"Error during OS detection: {e}")

if __name__ == "__main__":

    print('\nRunning...\n')

    target = sys.argv[1]
    nm_scan = nmap.PortScanner()

    # initial status scan
    nm_scanner = nm_scan.scan(target, '5000', arguments='-Pn')
    print(f"The host {target} is " + nm_scanner['scan'][target]['status']['state'] + "\n")

    # nmap scan
    scan_results = nmap_scan(target, nm_scan)
    if scan_results.empty:
        print("No open ports detected.\n")
    else:
        print(f"Nmap Scan Results for {target}:\n")
        print(scan_results)

    # os detection scan
    os_detection_scan(target, nm_scan)

    print("Report generated " + time.strftime("%Y-%m-%d_%H:%M:%S GMT", time.gmtime()))
    print("\nFinished.\n")
