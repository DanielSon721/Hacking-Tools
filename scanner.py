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
    results = pd.DataFrame(results).to_string()

    if not results:
        return "No open ports detected.\n\n"
    else:
        return f"Nmap Scan Results for {target}:\n\n" + results + "\n"

def os_detection_scan(target, scanner):
    try:
        result = scanner.scan(target, '5000', arguments='-O')
        if 'osmatch' in result['scan'][target] and result['scan'][target]['osmatch']:
            guessed_os = result['scan'][target]['osmatch'][0]
            accuracy = guessed_os.get('accuracy', '?')
            name = guessed_os.get('name', 'Unknown OS')
            return f"\nThere is a(n) {accuracy}% chance that the host is running {name}.\n\n"
        else:
            return "\nOS detection failed or returned no results.\n\n"
    except Exception as e:
        return f"Error during OS detection: {e}\n\n"

####################################################################################################

if __name__ == "__main__":

    to_file = input("\nWrite results to a file? (Y/N): ")

    print('\nRunning...\n')

    target = sys.argv[1]
    nm_scan = nmap.PortScanner()

    # initial status scan
    nm_scanner = nm_scan.scan(target, '5000', arguments='-Pn')
    host_results = f"The host {target} is " + nm_scanner['scan'][target]['status']['state'] + "\n\n"

    # nmap scan
    scan_results = nmap_scan(target, nm_scan)

    # os detection scan
    os_results = os_detection_scan(target, nm_scan)

    # timestamp
    timestamp = "Report generated " + time.strftime("%Y-%m-%d_%H:%M:%S GMT", time.gmtime())

    #print results
    print(host_results + scan_results + os_results + timestamp)

    # write results to file
    if to_file == 'Y':
        with open(f"{sys.argv[1]}_scan.txt", 'w') as file:
            file.write(host_results + scan_results + os_results + timestamp)

    print("\nFinished.\n")
