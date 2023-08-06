import os
import pandas as pd
from datetime import datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from autoads.gads import get_existing, get_search_term_report,create_keyword,_handle_googleads_exception,create_adgroup


save_path = 'data' #all the csvs will be stored on this folder
path = '/home/maunish/Upwork Projects/Google-Ads-Project/examples/google-ads.yaml'
customer_id = '6554081276' # google ads customer id
conversion_threshold = 1 #  get conversion >= conversion_threshold

os.makedirs(save_path,exist_ok=True)
googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")

print("Getting existing keywords")
# df_existing = get_existing(googleads_client,customer_id)
df_existing = pd.read_csv('data/df_existing.csv')
keywords_to_remove = df_existing[df_existing['camp_status'].isin(['ENABLED'])]['keyword_name'].unique().tolist()

print("Getting search term report")
# df_search_term_report = get_search_term_report(googleads_client,customer_id)
df_search_term_report = pd.read_csv('data/search_term_df.csv')
df_search_term_report = df_search_term_report.loc[df_search_term_report['metrics_conversions']>=conversion_threshold,['stv_search_term','adgroup_camp']]
df_search_term_report['Keywords'] = df_search_term_report['stv_search_term']
df_search_term_report = df_search_term_report[~df_search_term_report["Keywords"].isin(keywords_to_remove)]
# df_search_term_report['camp_id'] = df_search_term_report['adgroup_camp'].apply(lambda x: x.split('/')[-1])
df_search_term_report['camp_id'] = '16285319969'
df_search_term_report.drop(['stv_search_term','adgroup_camp'],axis=1,inplace=True)
df_search_term_report.to_csv(save_path+'/keywords_to_upload_report.csv',index=False)
df_search_term_report =  df_search_term_report.drop_duplicates('Keywords')
df_search_term_report = df_search_term_report.head()
df_search_term_report.to_csv(save_path+'/df_search_term_report.csv')

info_dict = {
        'campaign_id': list(),
        'adgroup_id': list(),
        'keyword_id': list(),
        'keyword_id2': list(),
        'type':list(),
}

if len(df_search_term_report) != 0:
    #code for expanding existing campaign
    print("Adding to existing campaign")
    try:
        for i, row in df_search_term_report.iterrows():
            keyword = row['Keywords']
            campaign_id = str(int(row['camp_id']))
            ad_group = create_adgroup(googleads_client,customer_id,campaign_id, adgroupName=keyword)
            if ad_group is None:
                continue
            ad_group_id = ad_group.split('/')[-1]
            keyword_id1 = create_keyword(
                googleads_client,customer_id,
                ad_group_id, keyword, kw_type='PHRASE')
            keyword_id1 = keyword_id1.split('/')[-1]
            keyword_id2 = create_keyword(
                googleads_client,customer_id,
                ad_group_id, keyword, kw_type='EXACT')
            keyword_id2 = keyword_id2.split('/')[-1]
            info_dict['campaign_id'].append(campaign_id)
            info_dict['adgroup_id'].append(ad_group_id)
            info_dict['keyword_id'].append(keyword_id1)
            info_dict['keyword_id2'].append(keyword_id2)
            info_dict['type'].append('expanded')
        print(f"{df_search_term_report.shape[0]} campaigns expanded")
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
else:
    print("No keywords to add into existing campaigns")

info_df = pd.DataFrame.from_dict(info_dict)
df_search_term_report = pd.concat([df_search_term_report, info_df], axis=1)
df_search_term_report.to_csv(save_path+f'/history/{datetime.now().strftime("%m-%d-%Y %H-%M-%S")}.csv', index=False)
