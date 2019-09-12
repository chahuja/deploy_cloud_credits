### Deploy a server to distribute cloud credits like aws and gcp

* save the coupon codes as a csv file in the directory `codes`
  - the column headers that must exist in the csv file are
  - 'Andrew ID', 'Code 1 ($50)','Code 2 ($50)','Code 3 ($50)'

* you would have to run 2 different servers for aws and gcp; hence you would need to use 2 different ports
   - AWS: 8000
   - GCP: 7000
   if you want to change these ports, you would have to modify the `index.html` file in `aws_ext` and `gcp_ext` directories as well


* Finally, run the the server.py file in `aws_ext` and `gcp_ext` using the following commands

GCP:

```
Usage: python server.py -csv <file-to-gcp_codes> -port 7000 -code GCP -FROM <your-andrew-id>

Example: python server.py -csv ../codes/gcp2019codes.csv -port 7000 -code GCP -FROM cahuja
```

AWS:

```
Usage: python server.py -csv <file-to-aws_codes> -port 8000 -code AWS -FROM <your-andrew-id>

Example: python server.py -csv ../codes/aws2019codes.csv -port 8000 -code AWS -FROM cahuja
```

* Use your andrew-id and the script will ask you for your password. This password is not stored anywhere except the RAM and it gets removed as soon as the program is killed.
