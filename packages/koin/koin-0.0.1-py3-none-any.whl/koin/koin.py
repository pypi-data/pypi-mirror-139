import json

class Koin():
 def __init__(self, **kwargs):
  credentials = self.__load_credentials(**kwargs)
  self.url = 'https://api.exchange.coinbase.com'
  if 'sandbox' in kwargs and kwargs['sandbox']:
   self.url = 'https://api-public.sandbox.exchange.coinbase.com'
  

 def accounts(self):
  return self.__get(path='/accounts')

 def orders(self):
  return self.__get(path='/orders')

 def place_market_order(self, **kwargs):
  if 'size' in kwargs and 'funds' in kwargs:
   raise ValueError('Specify either size or funds, not both')
  order = {
   'type':'market',
   'side': kwargs['side'],
   'product_id': kwargs['product_id'],
  }
  if 'size' in kwargs:
   order['size'] = kwargs['size']
  elif 'funds' in kwargs:
   order['funds'] = kwargs['funds']
  else:
   raise ValueError('Specify either size or funds')
  return self.__post(path='/orders', data=order)

 def place_limit_order(self, **kwargs):
  order = {
   'size': kwargs['size'],
   'price': kwargs['price'],
   'type':'limit',
   'side': kwargs['side'],
   'product_id': kwargs['product_id'],
  }
  return self.__post(path='/orders', data=order)

 def candles(self, **kwargs):
  path = '/products/{product_id}/candles'.format(**kwargs)
  parameters = {}
  if 'granularity' in kwargs:
   granularities = [60, 300, 900, 3600, 21600, 86400]
   if kwargs['granularity'] in granularities:
    parameters['granularity'] = kwargs['granularity']
   else:
    raise ValueError('Granularity must be one of ' + str(granularities))
  results = self.__get(path=path, parameters=parameters)
  #Convert to list of dictionaries
  from datetime import datetime, timezone
  keys = ['time','low','high','open','close','volume']
  transforms = [
   lambda x: datetime.fromtimestamp(x, timezone.utc).isoformat(),
   lambda x: x,
   lambda x: x,
   lambda x: x,
   lambda x: x,
   lambda x: x
  ]
  results = [{k:t(v) for k,v,t in zip(keys,r, transforms)} for r in results]
  return results



###############################################################################

 def __get(self, **kwargs):
  import requests
  headers = self.__get_headers(path=kwargs['path'], method='GET')
  if 'parameters' in kwargs:
   response = requests.get(
    self.url + kwargs['path'], 
    headers=headers, 
    params=kwargs['parameters']
   )
  else:
   response = requests.get(self.url + kwargs['path'], headers=headers)
  response.raise_for_status()
  return json.loads(response.text)
 
 def __post(self, **kwargs):
  import requests
  headers = self.__get_headers(path=kwargs['path'], body=kwargs['data'], method='POST')
  response = requests.post(
   self.url + kwargs['path'], json=kwargs['data'], headers=headers)
  print(response.text)
  response.raise_for_status()
  return json.loads(response.text)
 
 def __get_headers(self, **kwargs):
  from time import time
  timestamp = str(time())
  if 'body' in kwargs:
   body = json.dumps(kwargs['body'])
  else:
   body = ''
  return {
   'Accept': "application/json",
   'CB-ACCESS-KEY':self.key,
   'CB-ACCESS-SIGN':self.__get_signature(timestamp, kwargs['path'], body, kwargs['method']),
   'CB-ACCESS-TIMESTAMP':timestamp,
   'CB-ACCESS-PASSPHRASE':self.passphrase
  }


 def __get_signature(self, timestamp, path, body, method):
  import base64, hmac, hashlib, json
  message = timestamp + method + path + body
  print(message)
  hmac_key = base64.b64decode(bytes(self.secret,'utf-8'))
  signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
  signature = base64.b64encode(signature.digest()).decode()
  print(signature)
  return signature

 def __load_credentials(self, **kwargs):
  import json
  #Custom credentials file
  credentials_file = 'credentials.json'
  if 'credentials_file' in kwargs:
   credentials_file = kwargs['credentials_file']
  with open(credentials_file, 'r') as f:
   credentials = json.load(f)
  self.passphrase = credentials['passphrase']
  self.key = credentials['key']
  self.secret = credentials['secret']