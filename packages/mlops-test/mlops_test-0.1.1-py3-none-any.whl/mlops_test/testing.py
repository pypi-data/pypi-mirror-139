import requests
import pandas as pd
import time


class Test():
    def __init__(self) -> None:
        self.URL = "https://lh7l3f26qk.execute-api.eu-central-1.amazonaws.com/test/test"

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
        
    def test_api(self, df: pd.DataFrame):
        DATA = df.to_json()
        r = requests.post(url = self.URL, json = DATA)
        data = r.json()

        return data



if __name__ == "__main__":
    pass