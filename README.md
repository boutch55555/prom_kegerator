# Prometheus kegerator (Internet Of Beer)
## overview
Quick and dirty POC to control a beer fridge with the Prometheus monitoring stack. Totally overkill, but fun project.

I used a Raspberry PI zero with a pair of DS18B20 for temperature monitoring and a cheap eBay relay board for control. One of the temperature probes is for ambiant, the other is held against the keg.

The exporter serves double duty, it also receives calls from Alertmanager's webhook to toggle the relay state.

The Docker swarm stack runs on an old laptop so I don't have to use ARM containers on the PI. 

There are also Slack notifications in case something goes wrong.

## Setup
Plug the sensors and relay board on the PI, adjust pin numbers if required.  
Put the exporter code somewhere on the PI and set it to launch on boot. I used a @reboot crontab. Make sure to use Python 3.  
Adjust the PI IP in prometheus.yml and alertmanager.yml  
Configure your Slack api_url or send the route's receiver to devnull.  
Make the data folders and put config files on the Docker host. I used /data base, adjust the compose file if going with something else.  
Deploy the Docker stack.  
Add the Prometheus data source in Grafana and import the dashboard.  
Fix what I forgot to write here.  
