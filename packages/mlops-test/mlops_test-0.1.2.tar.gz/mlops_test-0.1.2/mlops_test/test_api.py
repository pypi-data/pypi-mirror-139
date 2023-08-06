import requests
import pandas as pd
import time


class TestAPI():
    def __init__(self) -> None:
        pass

    def deploy_code(self):
        URL = 'https://lh7l3f26qk.execute-api.eu-central-1.amazonaws.com/test/trigger_pipeline'
        r = requests.get(url = URL)
        data = r.json()
        status = data.get('status')
        print(status)
        time.sleep(10)
        
        while 'job is triggered' in status  or 'job is building' in status:
            status = self.get_jenkins_job_status()
            time.sleep(5)
            
            
        return status
     
    def get_jenkins_job_status(self):
        URL = 'https://lh7l3f26qk.execute-api.eu-central-1.amazonaws.com/test/get_pipeline_status'
        r = requests.get(url = URL)
        data = r.json()
        status = data.get('status')
        print(status)
        return status
        
    def test_api(self, df: pd.DataFrame, api_url):

        dfj = pd.DataFrame.to_json(df)

        r = requests.post(url = api_url, json = dfj)
        data = r.content

        return data



if __name__ == "__main__":
    pass