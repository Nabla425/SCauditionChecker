#%%
import sqlite3
import pandas as pd
from google.oauth2 import service_account
import gspread
import pandas as pd
from stqdm import stqdm

# df = pd.read_csv('C:\\Users\Ryusei Tanigutchi\\OneDrive\\Desktop\\audition_sim_flask\\datas\\Audition_index.csv',encoding="shift_jis")
# db_name = "datas/data.db"
# conn = sqlite3.connect(db_name)
# df.to_sql('audition',conn,if_exists='replace')

aountkey = {
    "type" : "service_account",
    "project_id" : "spreadsheet-test-367007",
    "private_key_id" : "bb0728c8484901117e3e17ea9f443b1f9a9635f6",
    "private_key" : "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCufuHt2uPj7XiZ\nnPZDSdJb91PcaFfZSiSFnRjFYHOtx60CvRfqNDOVq0xHzcX1qH3029tqDE8hioDx\ngDa07T5ymKT6w3GktsBN5xk33ahH8zD5C8bGURHFd4QXWMwF+FtnFYTHoKF9JvTy\nJWezxUpEECjRNzHJBHVHT8UacVShx6Onx3HN189RRUshxJ3CBqpJ/5AO3HVoaGpE\nrH6lSepz8XstknsjTtnRnofdoITucE/8GmjDMzwHQuhX3mBs8kO+LGDO9Gm5GN25\nHQT/PtHzk6br7rPA29e71gNjWeilrOZMdcnX341TqWbK2FOX0AMLh1QaFZbV5PYi\npuZxzZ0xAgMBAAECggEADciKfqAVc73gkpu+LRsB8Y9EEcsxM0ICyAYcfIzNnmrB\nHRAEOVUFxRsKk7pqmmjEiEismIAf6QmYfVsQFzMNRX6Ou5sgGS9xWcX5LTtGTWal\nleqK+UPSmEtERRbXyNnxGF+wBRfIYcsnuo/fVOku4Fj5bGtEdLk0LV2c92V/1qZ9\nY0S6MQa3q9eOX1ZXzO0B9RZnPs7jsRb/++/nYshbfLx6WurprTQe3wE8MbiZg3IQ\nVTg9c0961epIpFE2vb7LHY386Jjc3LA1ZeE3/XcCaaxDUyRYZEFs169h654Gm5r/\n+QGK/jG/JzU0W3Ho+nLDp5yafT8VQhLtlC0hejAl9QKBgQD06XtjteI7FaxMFL7F\n69wtypBsFJVoLGFORUYE6FLhAbdeRPE6h70CsgWnkZ9DKb1YuyWyGmLMxqLXqOx/\n077viw/mZqeod33BTuzz4w+Jr3JbSMMG9Q2SIpEiYFYIyx4cwkikRcENdW+FId4H\n/bJJpxFSIYh0XfHaLlVgIFz/XQKBgQC2ZUcsdPVCnArS65uAnWrEZWeVKZvTF6vR\nSpXFzFtyrNdwhk5qc1nCGaU0XgP9aUiRl2TpUgRp5GEV28SKGMWzc5Q6SfKbLQF1\nsh9Cd2LnWy2lbAX6h4vnEOT2OgVI+DYRFX5u7uqFT13d60eK/nRPMDPJYXKQ/4NE\nJ1FU5mH75QKBgFbJxmf3NEwryfrL/y6z/jpb5gHm6WsZDwJlmgJzMat6qDhHxhQv\ntdMWstpGyGFMkUS4TQtoPkrCuUIjImvJ5YeNh/zls9QHRBEUnvNuKztnaObgSfxV\nKpH2nefIq7RCBlG6p3NPJLJYQ0SyU7QROvTOt1ybdXeHMwVWFfsSfOIhAoGBAJWq\nm3GWc156DsOug4ZRJbgMgae7YdsglGODsUyCeROrUolKG/RrvN5yDsbe0qVRjDOz\nqCFwpKCDv0qhcC/lTe0HzTzbSxEcKBN82vu+XVD814LjFjDSovEzQr3tNEMBMdRo\n77t1nslPK/YaxzT9wVDte8Emjkz+7aayIKHq/cIlAoGAJaFUS+lOv0q6Rnv/oPr+\nt3LEJ0kLBTtc4hnHXk/0spVWcOegQUbpSv3ZCwXfSbtVb2Yc8aYlohCc/6TT+2ah\neXQ+vK6wOJhXA+w6qf3g5b/UltRoKnyLMZQUUxgtxR5eUnNRRWoW+x95/GTmMpOM\npMmA23XoN8OsqIBfOPtEcCQ=\n-----END PRIVATE KEY-----\n",
    "client_email" : "python@spreadsheet-test-367007.iam.gserviceaccount.com",
    "client_id" : "103434675863683856497",
    "auth_uri" : "https://accounts.google.com/o/oauth2/auth",
    "token_uri" : "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url" : "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/python%40spreadsheet-test-367007.iam.gserviceaccount.com"
}

scopes = [ 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(aountkey, scopes=scopes)
gc = gspread.authorize(credentials)
# スプレッドシートからデータ取得
SP_SHEET_KEY = '1_yC-107Od6CYlLbU_jtH_EUmZ3naQ5rmtG5tWQ5LJS4' # スプレッドシートのキー
sh = gc.open_by_key(SP_SHEET_KEY)
SP_SHEET = 'SupportCard_index' # シート名「シート1」を指定
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values() # シート内の全データを取得
support_df = pd.DataFrame(data[1:], columns=data[0]).fillna(0).replace('','0') # 取得したデータをデータフレームに変換
print(support_df.dtypes)

db_name = "datas/support.db"
conn = sqlite3.connect(db_name)
print(support_df.head)
support_df.to_sql("support",conn,conn,if_exists='replace')
# %%
