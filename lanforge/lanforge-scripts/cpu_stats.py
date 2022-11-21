#!/usr/bin/env python3
''' Author: Nikita Yadav

	This script will calculate the cpu and memory utilization by the system during runtime the output of which is a graph on html page also the second tab of html gives the system logs

steps to run script:
1-	On mate terminal type – python3 (file_name) -t (your duration in minutes for how much time you want to run the script).
2-	Example – python3 cpu_stat.py  -t 1
3-	Wait for the time provided to calculate statistics.
4-	After the script ends check for log.html file.
5-	Log.html file file show results in tab format selected.

'''

import argparse
import os
import matplotlib.pyplot as plt
import datetime
import base64
import logging
import threading
import time

fh = ''
fh_1 = ''

def cpu_percent(cmd):
    global fh
    fh = os.popen(cmd)

def memory_percent(cmd):
    global fh_1
    fh_1 = os.popen(cmd)

def htmlimage(data_4, data):
    html = open("log.html", 'w')
    img = data_4 + " " + data
    html.write(img)

def main():
    global duration
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--duration", type=int, help="Enter the Time for which you want to run test (in minutes)")
    try:
        args = parser.parse_args()
        if (args.duration is not None):
            duration = args.duration
    except Exception as e:
        logging.exception(e)
        exit(2)
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    now = datetime.datetime.now()
    starttime = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    delta = datetime.timedelta(seconds=10)
    cpu_stats_data = {"system": [], "kernel": []}
    memory_stats_data = {"Total": [], "Used": []}
    iterations = duration * 60

    cmd_1 = "top -bn1 -d 1 -n " + str(iterations) + " | grep '%Cpu(s)' "
    cmd_2 = "top -bn1 -d 1  -n " + str(iterations) + " | grep 'MiB Mem'"

    t1 = threading.Thread(target=cpu_percent, args=(cmd_1,))
    t2 = threading.Thread(target=memory_percent, args=(cmd_2,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    time.sleep(10)

    output = fh.read() + fh.readline()
    output_1 = fh_1.read() + fh_1.readline()
    data = output.split('\n')
    data_1 = output_1.split('\n')
    for i in data:
        # print(i.split(','))
        if len(i) > 3:
            cpu_stats_data["system"].append(float(i.split(',')[0].split()[1]))
            cpu_stats_data["kernel"].append(float(i.split(',')[1].split()[0]))
        # print(cpu_stats_data)

    for i in data_1:
        if len(i) > 3:
            memory_stats_data["Total"].append(float(i.split(',')[0].split()[3]))
            memory_stats_data["Used"].append(float(i.split(',')[2].split()[0]))
     # print(memory_stats_data)
    sample_times = [starttime + i * delta for i in range(len(cpu_stats_data["system"]))]
    label_locations = [d for d in sample_times if d.minute % 1 == 0]
    labels = [d.strftime('%Y-%m-%d %H:%M:%S') for d in label_locations]
    # print(labels)
    #print(sample_times)
    # thread creation

    # graphs
    #plot1
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(sample_times, cpu_stats_data['system'], '-', lw=1, color='r', label="system cpu%")
    ax.plot(sample_times, cpu_stats_data['kernel'], '-', lw=1, color='b', label="kernel cpu%")
    ax.set_ylabel('CPU (%)', color='r')
    ax.set_xlabel('time (s)')
    plt.tight_layout()
    ax.set_ylim(0., max(cpu_stats_data['system']) + 20)
    plt.xticks(rotation='vertical')
    fig.legend(["System CPU Utilization", "Kernel CPU Utilization"], loc='upper center')
    ax.grid()
    fig.savefig("cpu.png")

    #plot2
    fig_1 = plt.figure()
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.plot(sample_times, memory_stats_data["Total"], '-', lw=1, color='r', label="Total MEMORY AVAILABLE")
    ax_1.plot(sample_times, memory_stats_data["Used"], '-', lw=1, color='b', label="Total MEMORY USED")
    ax_1.set_ylabel('Total available', color='r')
    ax_1.set_xlabel('time (s)')
    plt.tight_layout()
    ax_1.set_ylim(0., max(memory_stats_data["Total"]) + 2000)
    plt.xticks(rotation='vertical')
    fig_1.legend(["TOTAL MEMORY AVAILABLE", "TOTAL MEMORY USED"], loc='upper center')
    ax_1.grid()
    fig_1.savefig("MEMORY.png")

    cmd_1 = "timeout 2s journalctl -p err --since '24 hour ago' > syslog.txt"
    fh_2 = os.system(cmd_1)
    fi_open = open("syslog.txt", "r+")
    out = fi_open.read()
    data_3 = out.split(" ")
    data_uri = base64.b64encode(open('cpu.png', 'rb').read()).decode('utf-8')
    data_uri_1 = base64.b64encode(open('MEMORY.png', 'rb').read()).decode('utf-8')
    data_a = '<img title="CPU utilization" src="data:image/png;base64,{0}">'.format(
    data_uri) + " " + '<img title="CPU utilization" src="data:image/png;base64,{0}">'.format(data_uri_1)

    data_4 = "<!DOCTYPE html><html><head> <meta name='viewport' content='width=device-width, initial-scale=1''><style>.accordion {background-color: #eee;color: #444;cursor: pointer;padding: 18px;width: 50%; border: none;text-align: left;outline: none;font-size: 15px;transition: 0.4s;}.active, .accordion:hover {background-color: #ccc; }.panel {padding: 0 18px;display: none;background-color: white;overflow: hidden;}</style></head><body> <button class='accordion''>CPU UTILIZATION</button> <div class='panel'> <p>" + data_a + "</p></div><script>acc = document.getElementsByClassName('accordion');var i;for (i = 0; i < acc.length; i++) {acc[i].addEventListener('click', function() {this.classList.toggle('active');var panel = this.nextElementSibling;if (panel.style.display === 'ock') {panel.style.display = 'none;} else {panel.style.display = 'block';}});}</script></body></html>"
    logs = " "
    for i in data_3:
        logs = logs + i
    data = "<head> <meta name='viewport' content='width=device-width, initial-scale=1'> <style>.accordion { background-color: #eee; color: #444; cursor: pointer;padding: 18px; width: 50%; border: none;text-align: left;outline: none;font-size: 10px;transition: 0.4s;} .active, .accordion:hover { background-color: #ccc;} .panel { padding: 0 18px; display: none; background-color: white; overflow: hidden;} </style> </head> <button class='accordion'>SYSTEM LOGS</button> <div class='panel'> <font face = 'Courier New' size = '2' color='#ff0000'>" + logs + "</font><br /> </div> <script> var acc = document.getElementsByClassName('accordion'); var i; for (i = 0; i < acc.length; i++) {acc[i].addEventListener('click', function() { this.classList.toggle('active');var panel = this.nextElementSibling;if (panel.style.display === 'block') {panel.style.display = 'none';} else {panel.style.display = 'block';}});} </script> "
    htmlimage(data_4, data)

if __name__ == '__main__':
    main()








