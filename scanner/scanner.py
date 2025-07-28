import nmap
import pandas as pd
import sys
import time
import google.generativeai as genai

genai.configure(api_key="AIzaSyBNSdzgxptmnLVGLtUm3URS6p_FdB2ddqU") 

def ai_analysis(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# scans for open ports
def port_scan(target, scanner):
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

    if not results:
        return f"No open ports detected on {target}.\n\n"
    else:
        return f"Nmap Scan Results for {target}:\n\n" + pd.DataFrame(results).to_string() + "\n\n"

# scans operating system
def os_detection_scan(target, scanner):
    try:
        result = scanner.scan(target, '5000', arguments='-O')
        if 'osmatch' in result['scan'][target] and result['scan'][target]['osmatch']:
            guessed_os = result['scan'][target]['osmatch'][0]
            accuracy = guessed_os.get('accuracy', '?')
            name = guessed_os.get('name', 'Unknown OS')
            return f"There is a(n) {accuracy}% chance that the host is running {name}.\n\n"
        else:
            return "OS detection failed or returned no results.\n\n"
    except Exception as e:
        return f"Error during OS detection: {e}\n\n"

####################################################################################################

if __name__ == "__main__":

    to_file = input("\nWrite results to a file? (Y/N): ")

    print(f"{"\033[34m"}\nScanning with Nmap...\n{"\033[0m"}")

    target = sys.argv[1]
    nm_scan = nmap.PortScanner()

    # initial status scan
    nm_scanner = nm_scan.scan(target, '5000', arguments='-Pn')
    host_results = f"The host {target} is " + nm_scanner['scan'][target]['status']['state'] + "\n\n"
    print(host_results, end = "")

    # nmap scan
    scan_results = port_scan(target, nm_scan)
    print(scan_results, end = "")

    # os detection scan
    os_results = os_detection_scan(target, nm_scan)
    print(os_results, end = "")

    time.sleep(1)
    print(f"{"\033[35m"}Passing results to Gemini AI...\n{"\033[0m"}")

    ai_results = ai_analysis("Analyze this nmap scan. Give me a quick summary, possible vulnerabilities, possible attack techniques, exploitation likelihood, and suggested remediation. Keep it simple. Less than 1200 characters.\n" + scan_results + os_results) + '\n'

    print(ai_results, end = "")

    # timestamp
    time.sleep(1)
    print(f"{"\033[36m"}Time of report:\n{"\033[0m"}")
    timestamp = "Report generated at " + time.strftime("%Y-%m-%d_%H:%M:%S GMT", time.gmtime()) + "\n"
    print(timestamp)

    # write results to file
    if to_file == 'Y':
        with open(f"{sys.argv[1]}_scan.txt", 'w') as file:
            file.write(host_results + scan_results + os_results + ai_results + timestamp)
        time.sleep(1)
        print(f"{"\033[32m"}Saved report to {sys.argv[1]}_scan.txt.\n{"\033[0m"}")
    
    time.sleep(1)
    print(f"{"\033[31m"}Finished.\n{"\033[0m"}")
