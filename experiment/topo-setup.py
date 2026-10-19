#!/usr/bin/python

import sys
from time import sleep, perf_counter
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, CPULimitedHost
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from threading import Thread
import floodlightRestApi

class NsfnetTopo(Topo):
    """
    Topology Link: https://github.com/BNN-UPC/NetworkModelingDatasets/blob/master/assets/nsfnet_topology.png
    """
    def build(self, **params):
        # Hosts
        hostCount = 20
        h0 = self.addHost('h0', ip='10.0.0.1', cpu=0.8/hostCount)
        h1 = self.addHost('h1', ip='10.0.0.2', cpu=0.8/hostCount)
        h2 = self.addHost('h2', ip='10.0.0.3', cpu=0.8/hostCount)
        h3 = self.addHost('h3', ip='10.0.0.4', cpu=0.8/hostCount)
        h4 = self.addHost('h4', ip='10.0.0.5', cpu=0.8/hostCount)
        h5 = self.addHost('h5', ip='10.0.0.6', cpu=0.8/hostCount)
        h7 = self.addHost('h7', ip='10.0.0.8', cpu=0.8/hostCount)
        h8 = self.addHost('h8', ip='10.0.0.9', cpu=0.8/hostCount)
        h9 = self.addHost('h9', ip='10.0.0.10', cpu=0.8/hostCount)
        h10 = self.addHost('h10', ip='10.0.0.11', cpu=0.8/hostCount)
        h11 = self.addHost('h11', ip='10.0.0.12', cpu=0.8/hostCount)
        h14 = self.addHost('h14', ip='10.0.0.15', cpu=0.8/hostCount)
        h15 = self.addHost('h15', ip='10.0.0.16', cpu=0.8/hostCount)
        h16 = self.addHost('h16', ip='10.0.0.17', cpu=0.8/hostCount)
        h17 = self.addHost('h17', ip='10.0.0.18', cpu=0.8/hostCount)
        h18 = self.addHost('h18', ip='10.0.0.19', cpu=0.8/hostCount)
        h19 = self.addHost('h19', ip='10.0.0.20', cpu=0.8/hostCount)
        h20 = self.addHost('h20', ip='10.0.0.21', cpu=0.8/hostCount)
        h21 = self.addHost('h21', ip='10.0.0.22', cpu=0.8/hostCount)
        h22 = self.addHost('h22', ip='10.0.0.23', cpu=0.8/hostCount)

        # Switches
        s0 = self.addSwitch('s0', dpid='00:00:00:00:00:00:00:01', protocols="OpenFlow13")
        s1 = self.addSwitch('s1', dpid='00:00:00:00:00:00:00:02', protocols="OpenFlow13")
        s2 = self.addSwitch('s2', dpid='00:00:00:00:00:00:00:03', protocols="OpenFlow13")
        s3 = self.addSwitch('s3', dpid='00:00:00:00:00:00:00:04', protocols="OpenFlow13")
        s4 = self.addSwitch('s4', dpid='00:00:00:00:00:00:00:05', protocols="OpenFlow13")
        s5 = self.addSwitch('s5', dpid='00:00:00:00:00:00:00:06', protocols="OpenFlow13")
        s6 = self.addSwitch('s6', dpid='00:00:00:00:00:00:00:07', protocols="OpenFlow13")
        s7 = self.addSwitch('s7', dpid='00:00:00:00:00:00:00:08', protocols="OpenFlow13")
        s8 = self.addSwitch('s8', dpid='00:00:00:00:00:00:00:09', protocols="OpenFlow13")
        s9 = self.addSwitch('s9', dpid='00:00:00:00:00:00:00:10', protocols="OpenFlow13")
        s10 = self.addSwitch('s10', dpid='00:00:00:00:00:00:00:11', protocols="OpenFlow13")
        s11 = self.addSwitch('s11', dpid='00:00:00:00:00:00:00:12', protocols="OpenFlow13")
        s12 = self.addSwitch('s12', dpid='00:00:00:00:00:00:00:13', protocols="OpenFlow13")
        s13 = self.addSwitch('s13', dpid='00:00:00:00:00:00:00:14', protocols="OpenFlow13")

        # Links options
        linkopts1 = dict(delay='25ms', bw=10, loss=0, max_queue_size=1000, use_htb=True, cls=TCLink)
        linkopts2 = dict(delay='25ms', bw=10, loss=0, max_queue_size=1000, use_htb=True, cls=TCLink)

        # Switch to switch links
        self.addLink(s0, s1, **linkopts2)
        self.addLink(s0, s2, **linkopts2)
        self.addLink(s0, s3, **linkopts2)
        self.addLink(s1, s7, **linkopts2)
        self.addLink(s1, s2, **linkopts2)
        self.addLink(s2, s5, **linkopts2)
        self.addLink(s3, s4, **linkopts2)
        self.addLink(s3, s8, **linkopts2)
        self.addLink(s4, s5, **linkopts2)
        self.addLink(s4, s6, **linkopts2)
        self.addLink(s5, s12, **linkopts2)
        self.addLink(s5, s13, **linkopts2)
        self.addLink(s6, s7, **linkopts2)
        self.addLink(s7, s10, **linkopts2)
        self.addLink(s8, s9, **linkopts2)
        self.addLink(s8, s11, **linkopts2)
        self.addLink(s9, s10, **linkopts2)
        self.addLink(s9, s12, **linkopts2)
        self.addLink(s10, s11, **linkopts2)
        self.addLink(s10, s13, **linkopts2)
        self.addLink(s11, s12, **linkopts2)

        # Switch to host links
        self.addLink(s0, h0, **linkopts1)
        self.addLink(s1, h1, **linkopts1)
        self.addLink(s2, h2, **linkopts1)
        self.addLink(s3, h3, **linkopts1)
        self.addLink(s4, h4, **linkopts1)
        self.addLink(s5, h5, **linkopts1)
        self.addLink(s7, h7, **linkopts1)
        self.addLink(s8, h8, **linkopts1)
        self.addLink(s9, h9, **linkopts1)
        self.addLink(s10, h10, **linkopts1)
        self.addLink(s11, h11, **linkopts1)
        self.addLink(s3, h14, **linkopts1)
        self.addLink(s1, h15, **linkopts1)
        self.addLink(s8, h16, **linkopts1)
        self.addLink(s7, h17, **linkopts1)
        self.addLink(s11, h18, **linkopts1)
        self.addLink(s2, h19, **linkopts1)
        self.addLink(s10, h20, **linkopts1)
        self.addLink(s5, h21, **linkopts1)
        self.addLink(s3, h22, **linkopts1)


def generateBackgroundTraffic(net, duration=86400):
    """Spawns continuous background traffic between host pairs to simulate load."""
    traffic_pairs = [
        ("h8", "h3", "100M"),
        ("h16", "h14", "100M"),
        ("h7", "h1", "100M"),
        ("h17", "h15", "100M"),
        ("h10", "h11", "100M"),
        ("h20", "h18", "100M"),
        ("h5", "h2", "100M"),
        ("h21", "h19", "100M"),
        ("h4", "h22", "3M"),
    ]
    port = 5555
    for sender, receiver, bw in traffic_pairs:
        server = net.getNodeByName(sender)
        client = net.getNodeByName(receiver)
        
        # Use Mininet's native popen to run commands in the background
        server.popen(f"iperf3 -s -p {port} -i 1")
        sleep(0.5)
        client.popen(f"iperf3 -c {server.IP()} -p {port} -b {bw} -t {duration}")
        port += 1

def startNetwork():
    global net
    net = Mininet(topo=NsfnetTopo(), link=TCLink, build=False, switch=OVSKernelSwitch, autoSetMacs=True, waitConnected=True)

    info('[INFO] Connecting to Floodlight Controller...\n')
    net.addController('c1', controller=RemoteController, ip="127.0.0.1", port=6653, protocols="OpenFlow13")

    info('[INFO] Building and starting network...\n')
    net.build()
    net.start()
    sleep(2)

    info('[INFO] Setting base routing metric...\n')
    floodlightRestApi.setRoutingMetric("hopcount")

    info('[INFO] Testing initial connectivity...\n')
    net.pingAll()

    info('[INFO] Generating background traffic for RL training...\n')
    generateBackgroundTraffic(net)

    info('\n[READY] Network is live! You can now start python train.py in another terminal.\n')
    
    # Opens interactive Mininet CLI to keep topology alive while training
    CLI(net)
    
    info('[INFO] Stopping network...\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    startNetwork()