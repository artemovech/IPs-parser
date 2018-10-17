# IPs-parser
Simple parser that can simply parse all IP adresses in your file (log, txt, etc) and check information about it from ip-api.com 

## Usage:
 
 ```sh
$ python main.py -f file_name
```

## Notice
ip-api.com API has a limit of 500 requests per minute. 
So, after 500 requests program has a 60s sleep time, before starts parsing next IPs
