def parse_ipv4(line, if_dict):
    if "." in line:
        l_status = line.split()[4]
        if "admin" in l_status:
            l_status = "administratively down"
        line = line.split()[:2]
        
        d_len = len(if_dict)
        if_dict["if"+str(d_len+1)] = {"name": line[0], "ip4-addr": line[1], "if-status": l_status}

def parse_ipv6(file_contents, if_dict):
    if_name = ipv6 = llocal = ""
    for line in file_contents:
        line = line.rstrip()
        split_len = len(line.split())
        col1 = line.lstrip().split()[0]
        # if line has more than 4 columns its ipv4 or text, disregard!
        if split_len > 4 or "unassigned" in line:
            continue
        # if line begins with a character (before splitting) and either
        # ipv6 or link local address has been set this means we reached a
        # new interface name, so we need to reset some values
        elif line[0] != " " and (ipv6 != "" or llocal != ""):
            #print("interface: {}\tipv6: {}\tlink-local: {}".format(if_name, ipv6, llocal))
            from_parse = (if_name + "," + llocal + "," + ipv6)
            check_dictionary(from_parse, if_dict)
            if_name, ipv6, llocal = col1, "", ""
        elif line[0] != " " and ipv6 == "" and llocal == "":
            if_name = col1
        elif "FE80::" in line.lstrip().split()[0]:
            llocal = col1
        elif ":" in line.lstrip().split()[0]:
            ipv6 = col1 
        
def check_dictionary(from_parse, if_dict):
    # first check if the entry contains ipv4 or ipv6 information
    if ":" in from_parse:
        # this is an ipv6 entry!
        print("ipv6!")
    else:
        # this is an ipv4 entry!
        print("ipv4")

interfaces = {}

fil_object = open("brouter-all", "r")
contents = fil_object.readlines()
for row in contents:
    parse_ipv4(row, interfaces)

parse_ipv6(contents, interfaces)
#print(interfaces)

'''interfaces["if"+str(len(interfaces)+1)] = {
    'name': 'GigabitEthernet 1/0/1', 
    'ip4-addr': '192.168.5.1', 
    'ip4-mask': '255.255.255.0', 
    'ip6-addr': '2001:6B0:1D:1::/64', 
    'ip6-ll': 'FE80::10',
    'if-status': 'up', (or administratively down)
    'desc': 'This is a cool interface'
}'''

'''        print(len(line.split()))
        if len(line.split()) < 3 and if_name == "" and ipv6 == "" and llocal == "" and ":" not in line:
            if_name = line.split()[0]
            print("if_name", if_name)
        elif "FE80" in line.split()[0]:
            llocal = line.split()[0]
            print("llocal", llocal)
        elif ":" in line.split()[0]:
            ipv6 = line.split()[0]
            print("ipv6", ipv6)
        elif "unassigned" in line.split()[0]:
            if_name = ipv6 = llocal = ""
            break
        else:
            #iterera över dict interface namn, finns dem, skriv in ivp6 adresser
            #annars skapa nya interface
            d_len = len(if_dict)
            if d_len != 0 and if_name != "":
                for part in if_dict.keys():
                    if if_name == if_dict[part]["name"]:
                        if_dict[part]["ip6-addr"] = ipv6
                        if_dict[part]["ip6-ll"] = llocal
                    print(part, if_dict[part])
                if_dict["if"+str(d_len+1)] = {"name": if_name, "ip6-addr": ipv6, "ip6-ll": llocal}
            elif d_len == 0:
                if_dict["if1"] = {"name": if_name, "ip6-addr": ipv6, "ip6-ll": llocal}
'''                
