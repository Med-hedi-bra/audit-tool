import re
def extract_ports_info():
    res = []
    matching_lines = []
    pattern = r"^\d+/tcp.+"
    pattern_os_version_2 = r"OS details: (.+?)\n"
    with open("/home/mohamed/Desktop/rest/venv/src/nmap.txt", 'r') as file:
        for line in file:
            if re.match(pattern, line):
                matching_lines.append(line.strip())
            if re.match(pattern_os_version_2, line):
                os_version = line.split(":")[1].strip() if line else ""
    for line in matching_lines:
        temp = re.sub(r'\s+', ' ', line).split(" ")
        port = temp[0].split("/")[0]
        protcol = temp[0].split("/")[1]
        state = temp[1]
        service = temp[2]
        version = " ".join(temp[3:]) if len(temp) > 3 else ""
        res.append({
            "port": port,
            "protocol": protcol,
            "state": state,
            "service": service,
            "version": version
        })
    print(os_version)
    return res
        

print(extract_ports_info())