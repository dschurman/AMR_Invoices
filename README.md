# GAMIR: Generation of Automatic Meter Invoice Records

Allows Automatic Meter Reading (AMR) using an [RTL-SDR](https://www.amazon.com/gp/product/B011HVUEME/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1) and Raspberry Pi 3 with bemasher's [rtlamr](https://github.com/bemasher/rtlamr) library. A tool for landlords to automatically generates invoice PDFs for their tenants. 

Dependencies: 

[rtlamr](https://github.com/bemasher/rtlamr) (follow link for installation instructions)<br>
rtl_tcp (helpful installation instructions [here](https://photobyte.org/using-the-raspberry-pi-as-an-rtl-sdr-dongle-server/))<br>
[python fpdf](https://pyfpdf.readthedocs.io/en/latest/)

Deployment (/insert to append to mySQL, /query_by_tenant to query mySQL):

[dschurma.pythonanywhere.com](https://dschurma.pythonanywhere.com)

See [the sample spreadsheet](
https://docs.google.com/spreadsheets/d/1TRYBGVfX7MxZW_Zdk1KU23LdNNQpnMQoGqK6AY0Jrw0/edit?usp=sharing
).
