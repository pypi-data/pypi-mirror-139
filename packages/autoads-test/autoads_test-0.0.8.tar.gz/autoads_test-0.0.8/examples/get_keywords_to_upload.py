import os
import pandas as pd
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from autoads.keywords import get_keywords_metrics
from autoads.gads import get_existing

email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
match_extract = ['exact', 'phrase']  # exact, phrase, broad
df_path = 'data/df_final.csv' # csv where keywords are stored
save_path = 'data' #all the csvs will be stored on this folder
path = '/home/maunish/Upwork Projects/Google-Ads-Project/examples/google-ads.yaml'
customer_id = '6554081276'
threshold = 0.8
allowed_funnels = ['LF','MF'] # available options LF, MF, UF
allowed_status = ['PAUSED','REMOVED','UNKNOWN','UNSPECIFIED'] # options 'ENABLED','PAUSED','REMOVED','UNKNOWN','UNSPECIFIED'

googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")

df = pd.read_csv(df_path)
df_existing = get_existing(googleads_client,customer_id)
keywords_to_remove = df_existing[~df_existing['camp_status'].isin(allowed_status)]['keyword_name'].unique().tolist()
df = df[~df["Keywords"].isin(keywords_to_remove)]
# campaigns_to_remove = df_existing[df_existing['camp_status'].isin(allowed_status)]['camp_name'].unique().tolist()
# df = df[~df["Keywords2"].isin(campaigns_to_remove)]
df = df[df['similarity'] >= threshold]
df = df[df['lf/mf/uf'].isin(allowed_funnels)].reset_index(drop=True)

os.makedirs(save_path,exist_ok=True)
df_existing.to_csv(save_path+'/existing_keywords.csv')
df = df.drop_duplicates("Keywords")
df = get_keywords_metrics(email,api_key,df,match_extract)
df.to_csv(save_path+'/keywords_to_upload.csv',index=False)

