import network, time
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
# kobler til med SSID og passordet til nettverket
sta_if.connect("gamle skolevei5a", "tigermann")
# venter til tilkoblingen er etabert
while not sta_if.isconnected():
    time.sleep(0.1)
# printer ip adresse som enheten har f氓tt tilkobling til nett
print(sta_if.ifconfig())

#nets = sta_if.scan()
#for n in nets:
#   print(n)
