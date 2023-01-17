from flask import Flask, render_template, request, Response
from flaskwebgui import FlaskUI
import time
import socket
import sys
import os

def getipaddress():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    ui = FlaskUI(app, host=getipaddress())
else:
    app = Flask(__name__)


@app.route("/")
def ConfGen():
    return render_template("ConfGen.html")


@app.route("/generate", methods=["POST"])
def generate():
    # Builds the DHCP Snooping allowed vlans
    def snoop_vlans(vl_list):
        # <!>dhcpvlans<!>
        return_string = ''
        for i in range(len(vl_list)):
            if i != len(vl_list) - 1:
                return_string += vl_list[i] + ','
            else:
                return_string += vl_list[i]

        return return_string

    def init_vlans(vl_list):
        # <!>createvlans<!>
        vlan_string = ''
        for vl in vl_list:
            vlan_string += 'vlan ' + vl[1] + '\n'
            vlan_string += 'name ' + vl[0] + '\n'
            vlan_string += '!\n'

        return vlan_string

    def buildstring(bsstack, bsports, bsport_type, bsAVLAN, bsVVLAN, bszoneid):
        # <!>portstart<!>
        if getattr(sys, 'frozen', False):
            bsfile_str = os.path.join(sys._MEIPASS, zoneid + '_PortConfig.txt\\' + zoneid + '_PortConfig.txt')
        else:
            bsfile_str = bszoneid + "_PortConfig.txt"
        bsfile = open(bsfile_str, "r")
        bsfile_contents = bsfile.read()
        bsfile_contents.splitlines()
        bsfile_string = ""
        for stackcount in range(1, int(bsstack) + 1):
            for portcount in range(1, int(bsports) + 1):
                for bsline in bsfile_contents.splitlines():
                    for bsword in bsline.split():
                        if bsword == "<!>interface<!>":
                            bsfile_string += bsport_type + str(stackcount) + "/0/" + str(portcount)
                        elif bsword == "<!>AccessVlan<!>":
                            bsfile_string += bsAVLAN
                        elif bsword == "<!>VoiceVlan<!>":
                            bsfile_string += bsVVLAN
                        else:
                            bsfile_string += bsword + " "
                    bsfile_string = bsfile_string.rstrip(" ")
                    bsfile_string += "\n"
        bsfile.close()
        return bsfile_string

    zoneid = request.form.get("Zone")
    if getattr(sys, 'frozen', False):
        zone_str = os.path.join(sys._MEIPASS, zoneid + '_SwitchTemplate.txt\\' + zoneid + '_SwitchTemplate.txt')
    else:
        zone_str = request.form.get("Zone") + "_SwitchTemplate.txt"

    file = open(zone_str, "r")
    file_contents = file.read()
    file_contents.splitlines()

    # Physical Switch Variables
    host_name = str(request.form.get("Hostname"))
    building = str(request.form.get("Building"))
    p_address = str(request.form.get("Address"))
    # == VLAN input ==
    access_vlan_num = request.form.get("AVlanNum")
    access_vlan_name = str(request.form.get("AVlanName"))

    voice_vlan_num = request.form.get("VVlanNum")
    voice_vlan_name = str(request.form.get("VVlanName"))

    mgmt_vlan_num = request.form.get("MVlanNum")
    mgmt_vlan_name = str(request.form.get("MVlanName"))

    vlan_extra_init = request.form.getlist("vlan_name[]")
    dynamic_vlan_entnum = request.form.getlist("vlan_num[]")
    dynamic_vlan_entname = request.form.getlist("vlan_name[]")

    vlan_extra_init = len(dynamic_vlan_entnum)
    snoop_init_list = [access_vlan_num, voice_vlan_num]

    vlan_init_list = [(access_vlan_name, access_vlan_num), (voice_vlan_name, voice_vlan_num),
                      (mgmt_vlan_name, mgmt_vlan_num)]

    i = 0
    while i < vlan_extra_init:
        snoop_init_list.append(dynamic_vlan_entnum[i])
        vlan_init_list.append((dynamic_vlan_entname[i], dynamic_vlan_entnum[i]))
        i += 1

    vlan_init_string = init_vlans(vlan_init_list)
    snoop_string = snoop_vlans(snoop_init_list)

    ip_address = str(request.form.get("SwitchIP"))
    subnet = str(request.form.get("SwitchSub"))
    gateway = str(request.form.get("SwitchGateway"))

    port_num = request.form.get("PortCount")
    stack_num = request.form.get("StackCount")

    port_type = request.form.get("PortType")

    interfaces_string = buildstring(stack_num, port_num, port_type, access_vlan_num, voice_vlan_num, zoneid)
    file_string = ""
    for line in file_contents.splitlines():
        for word in line.split():
            if word == "<!>hostname<!>":
                file_string += host_name + " "
            elif word == "<!>dhcpvlans<!>":
                file_string += snoop_string
            elif word == "<!>sourcevlan<!>":
                file_string += "Vlan" + str(mgmt_vlan_num)
            elif word == "<!>createvlans<!>":
                file_string += vlan_init_string
            elif word == "<!>gateway<!>":
                file_string += gateway
            elif word == "<!>mgmtvlan<!>":
                file_string += mgmt_vlan_num
            elif word == "<!>ipaddress<!>":
                file_string += ip_address + " "
            elif word == "<!>subnet<!>":
                file_string += subnet
            elif word == "<!>portstart<!>":
                file_string += interfaces_string
            elif word == "<!>building<!>":
                file_string += building
            elif word == "<!>address<!>":
                file_string += p_address
            elif word == "<!>zone<!>":
                file_string += zoneid
            else:
                file_string += word + " "

        file_string = file_string.rstrip(" ")
        file_string += "\n"

    time_string = ''
    time_tuple = time.localtime()
    for t in range(5):
        if t == 4:
            time_string += str(time_tuple[t])
        else:
            time_string += str(time_tuple[t]) + '-'
    return_string = app.response_class(file_string, mimetype='text/plain')
    filename = host_name + "-" + time_string + ".config"
    return_string.headers.set('Content-Disposition', 'attachment', filename=filename, content_type='text/plain; charset=UTF-16')
    file.close()
    return return_string


if __name__ == "__main__":
    app.run(host="0.0.0.0")
