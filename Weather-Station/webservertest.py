import usocket as socket
import time
from machine import Pin, I2C
import BME280
i2c = I2C(scl=Pin(22),sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)
#while True:
  #print(bme.temperature, bme.pressure, bme.humidity)
  #time.sleep(1)


def read_sensor():
  global temp, temp_percentage, hum, pressure
  temp = temp_percentage = hum = 0
  temp = bme.temperature[0:-1]
  hum = bme.humidity[0:-1]
  temp_percentage = (float(temp)+6)/(40+6)*(100)
  pressure = bme.pressure[0:-3]


def web_page():
  html = """
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="30">
    <meta charset="UTF-8">
    <style>

        .message {
            font-weight: 600;
            color: crimson;
        }
        .navbar {
            background-color: lightslategray;
            font-size: 1em;
            font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
            color: white;
            padding: 8px 5px 8px 5px;
        }

        .navbar a {
            text-decoration: none;
            color: inherit;
        }

        .navbar-brand {
            font-size: 1.2em;
            font-weight: 600;
        }

        .navbar-item {
            font-variant: small-caps;
            margin-left: 30px;
        }

        .body-content {
            padding: 5px;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .progress {
            background-color: #F5F5F5;
        }
        .progress.vertical {
            position: relative;
            width: 25%;
            height: 60%;
            display: inline-block;
            margin: 20px;
        }
        .progress.vertical > .progress-bar {
            width: 100% !important;
            position: absolute;
            bottom: 0;
        }
        .progress-bar {
            background: linear-gradient(to top, #f5af19 0%, #f12711 100%);
        }
        .progress-bar-hum {
            background: linear-gradient(to top, #9CECFB 0%, #65C7F7 50%, #0052D4 100%);
        }
        .progress-bar-pressure {
            background: linear-gradient(to top, #9CECFB 0%, #65C7F7 50%, #0052D4 100%);
        }
        p {
            position: absolute;
            font-size: 1.5rem;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 5;
        }
        .button {
            background-color: #4CAF50;
            /* Green */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
        }
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #111;
        }
        li {
            float: left;
        }
        li a {
            display: block;
            color: #818181;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }
        li a:hover {
            background-color: #f1f1f1;
                }
    </style>
</head>
    <meta charset="utf-8" />
    <title>Testapp</title>
<body>
        <header>
                <div class="navbar">
                    <h1 class="logo">NYOY</h1>
                    <strong><nav>
                        <ul class="menu">
                            <li><a href="http://nyoy.no/testapp/">Home</a></li>
                            <li><a href="http://nyoy.no/testapp/about">About</a></li>
                            <li><a href="http://nyoy.no/testapp/contact">Contact</a></li>
                        </ul>
                    </nav></strong>
                </div>
                
        </header>
                <h1>BME 280 by Øystein Nyhus</h1>
                    <div class="progress vertical">
                        <p>"""+str(temp)+"""*<p>
                        <div role="progressbar" style="height: """+str(temp_percentage)+"""%;" class="progress-bar">
                    </div>
                    </div>
                        <div class="progress vertical">
                            <p>"""+str(hum)+"""%</p>
                            <div role="progressbar" style="height: """+str(hum)+"""%;" class="progress-bar progress-bar-hum">
                    </div>
                    </div>
                        <div class="progress vertical">
                        <p>"""+str(pressure)+"""%</p>
                        <div role="progressbar" style="height: """+str(float(pressure)-1000)+"""%;" class="progress-bar progress-bar-pressure">
                    </div>
                    </div>
           <input type="button" value="Refresh Page" onClick="location.href=location.href">
       </body>
                <script>
                    function startTime() {
                        var today = new Date();
                        var h = today.getHours();
                        var m = today.getMinutes();
                        var s = today.getSeconds();
                        m = checkTime(m);
                        s = checkTime(s);
                        document.getElementById('txt').innerHTML =
                        h + ":" + m + ":" + s;
                        var t = setTimeout(startTime, 500);
                    }
                    function checkTime(i) {
                        if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
                        return i;
                    }
                </script>     
        </head>
</html>
"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  read_sensor()
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

