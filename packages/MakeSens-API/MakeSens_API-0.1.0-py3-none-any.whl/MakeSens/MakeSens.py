class MakeSens:
  import pandas
  import requests
  import json
  from typing import Union
  from datetime import datetime
  def __init__(self, proyecto:str,token:str):
    self.headers = {'content-type': 'application/json',
                  'Authorization':f'Bearer {token}'}
    self.project=self.json.loads(self.requests.get(f'https://makesens.aws.thinger.io/v1/users/MakeSens/devices?project={proyecto}',headers=self.headers).content)
    self.devices_dfs=[]
    self.devices=[]
    for p in self.project:
      device=self.json.loads(self.requests.get(f'https://makesens.aws.thinger.io/v1/users/MakeSens/devices/{p["device"]}',headers=self.headers).content)['connection']['location']
      lat,lon=device['lat'],device['lon']
      self.devices.append(p['device'])
      device_df={'device':p['device'],'name':p['name'],'active':p['connection']['active'],'description':p['description'],'last_timestamp':
                 self.datetime.utcfromtimestamp(p['connection']['ts']/1000).strftime('%Y-%m-%d %H:%M:%S'),
        'lat':lat,'lon':lon}
      self.devices_dfs.append(device_df)
    self.devices_dfs=self.pandas.DataFrame(self.devices_dfs).set_index('device')
    self.data_total={}

  def request_data(self,id_devices:Union[list,tuple]=[],start:str='2015-01-01',end:str='2023-01-01',items:int=1000)->dict:
    if not id_devices:
      id_devices=self.devices
    start=int((self.datetime.strptime(start,"%Y-%m-%d") - self.datetime(1970, 1, 1)).total_seconds())*1000
    end=int((self.datetime.strptime(end,"%Y-%m-%d") - self.datetime(1970, 1, 1)).total_seconds())*1000
    self.data_total={}
    for id in id_devices:
      data=[]
      min_ts=start
      while min_ts-1<end:
        d=self.json.loads(self.requests.get(f'https://makesens.aws.thinger.io/v1/users/MakeSens/buckets/{"B"+id}/data?items={items}&min_ts={min_ts}&sort=asc',headers=self.headers).content)
        if not d: break
        data+=d
        min_ts=d[-1]['ts']+1
      self.data_total[id]=self.pandas.DataFrame([i['val'] for i in data],index=[self.datetime.utcfromtimestamp(i['ts']/1000).strftime('%Y-%m-%d %H:%M:%S') for i in data])
    return self.data_total

  def request_device_status(self,id_devices:Union[list,tuple]=[])->list:
    if not id_devices:id_devices=self.devices
    return {id:self.json.loads(self.requests.get(f'https://makesens.aws.thinger.io/v1/users/MakeSens/devices/{id}',headers=self.headers).content) for id in id_devices}

  def data_types(self,data:dict={})->dict:
    if not data:
      data=self.data_total
    return {id:df.dtypes for id,df in data.items()}
  
  def plot_data(self):
    for id,df in self.data_total.items():
      n=len(df.columns)
      ax=df.plot(subplots=True,sharex=False,figsize=(20,4*n),title=[id]*n)
  def save_data(self):
    [df.to_csv(id) for id,df in self.data_total.items()]
