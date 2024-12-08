declarations = (
    { "name": "nmap",      "function": "port_scaning_nmap",      "screenshot": "desktop" },
    { "name": "nikto",     "function": "server_scaning_nikto",    "screenshot": "desktop" },
    { "name": "wapiti",     "function": "server_scaning_wapiti",    "screenshot": "desktop" },
    { "name": "arachni",     "function": "server_scaning_arachni",    "screenshot": "desktop" },

) # yapf: disable

module_name = "security"

for dec in declarations:
    dec["module"] = module_name
