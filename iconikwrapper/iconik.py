from . import session
from string import Template
import math
import json
import requests


job_create_payload = """{
  "object_id":"$objectID",
  "object_type":"$object_type",
  "status":"$job_status",
  "title":"$job_title",
  "type":"$job_type"
}"""

job_update_payload = """{
  "id": "$job_id",
  "progress_processed": $progress,
  "status": "$status",
  "message": "$latest_comment"
}"""

class assets(object):
    def __init__(self, id):
        self.id = id
        #self.title

    def info(self):
        path = 'https://app.iconik.io/API/assets/v1/assets/{}/'.format(self.id)
        assetinfo = {}
        try:
            response = session.get(path)
            response.raise_for_status()
            # Code here will only run if the request is successful
            json_dict = json.loads(response.content.decode('utf-8'))
            assetinfo['asset_id'] = json_dict['id']
            assetinfo['title'] = json_dict['title']

            for x in json_dict['versions']:
                if x['status'] == 'ACTIVE':
                    assetinfo['version_id'] = x['id']

        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return assetinfo

    def duration(self):
        #get asset duration from technical metadata view, convert to seconds from milliseconds
        path = 'https://app.iconik.io/API/metadata/v1/assets/{}/views/66c826b0-5e46-11ea-ab85-0a580a3f8c8d/'.format(self.id)

        try:
            response = session.get(path)
            response.raise_for_status()
            #code here will only run if successful 
            r = response.json()
            ms_duration = int(r['metadata_values']['Duration']['field_values'][0]['value'])
            seconds = math.ceil((ms_duration/1000)%60)
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return seconds

    
    def proxy_url(self):
       
        path = 'https://app.iconik.io/API/files/v1/assets/{}/proxies/'.format(self.id)
        payload = {'generate_signed_url': True, 'content_disposition': 'attachment'}
        try:
            response = session.get(path, params=payload)
            response.raise_for_status()
            # Code here will only run if the request is successful
            asset_proxy_info = json.loads(response.content.decode('utf-8'))
            signed_link = asset_proxy_info['objects'][0]['url']
            asset_format = asset_proxy_info['objects'][0]['format']
            asset_filename = asset_proxy_info['objects'][0]['name']
            proxy_info = {'signed_link' : signed_link, 'asset_format' : asset_format, 'asset_filename' : asset_filename}

        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:  
            return proxy_info

    def create_transcription(self, asset_id, version_id, body):
        payload = json.dumps(body, indent=4)
        path = 'https://app.iconik.io/API/assets/v1/assets/{}/versions/{}/transcriptions/properties/'.format(asset_id, version_id)
        try:
            response = session.post(path, data=payload)
            response.raise_for_status()
            #code here will only run if successful 
            #print(content)
            print(response.text)
            content = response.json()
            transcription_id = content['id']
            print('transcription id is: ',transcription_id)
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            print(response.text)

            
            return transcription_id

    def add_metadata(self, asset_id, metadata_payload, view_id):
        path = 'https://app.iconik.io/API/metadata/v1/assets/{}/views/{}/'.format(asset_id, view_id)
        print('attempting to update metadata fields in Iconik')
        try:
            response = session.put(path, data=metadata_payload)
            #print(response.url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
            raise SystemError(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
            raise SystemError(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
            raise SystemError(errt)
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
            raise SystemError(err)
        else:
            print(response.status_code, 'sucessfully updated asset metadata')
            return(response.text)

    def add_bulk_segments(self, asset_id, bulk_assets):
        path = 'https://app.iconik.io/API/assets/v1/assets/{}/segments/bulk/'.format(asset_id)
        print('attempting to add bulk segments to asset in Iconik')
        try:
            response = session.post(path, data=bulk_assets)
            print(response.status_code)
            #print(response.url)
            #print(response.text)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
            raise SystemError(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
            raise SystemError(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
            raise SystemError(errt)
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
            raise SystemError(err)
        else:
            print('sucessfully added bulk segments to asset in Iconik')
            print(response.status_code, response.text)
            return(response.status_code)



class users(object):
    def __init__(self, id):
        self.id = id
    
    def info(self, id):
        path = 'https://app.iconik.io/API/users/v1/users/{}/'.format(self.id)
        try:
            response = session.get(path)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return response.json()
    

class jobs(object):
    def __init__(self):
        pass
    
    def info(self, job_id):
        path = 'https://app.iconik.io/API/jobs/v1/jobs/{}/'.format(job_id)
        try:
            response = session.get(path)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return response.json()
    
    def create_job(self, object_id, object_type, job_title, job_type, job_status):
        self.job_title = job_title
        path = 'https://app.iconik.io/API/jobs/v1/jobs/'
        payload = Template(job_create_payload)
        formatted_payload = payload.safe_substitute(objectID=object_id, object_type=object_type, job_title=job_title, job_type=job_type, job_status=job_status)
        try:
            response = session.post(path, data=formatted_payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return response.json()
    
    def update_job(self, job_id, progress, status):
        path = 'https://app.iconik.io/API/jobs/v1/jobs/{}/'.format(job_id)
        payload = Template(job_update_payload)
        formatted_payload = payload.safe_substitute(id=job_id, progress=progress, status=status)
        
        try:
            response = session.patch(path, data=formatted_payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print(response.json())
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            print(response.json())
        except requests.exceptions.Timeout as errt:
            print(errt)
            print(response.json())
        except requests.exceptions.RequestException as err:
            print(err)
            print(response.json())
        else:
            return response.json()

