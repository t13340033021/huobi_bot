import os
if(os.path.exists("huobi/privateconfig.py")):
    from huobi.privateconfig import *
    g_api_key = p_api_key
    g_secret_key = p_secret_key
else:
    g_api_key="feaf06c0-00de3aa3-fe8b99ff-1qdmpe4rty"
    g_secret_key="f5e1dda1-d33078ec-7115892b-f57e8"

g_account_id = 12345678

g_sub_uid = 87654321

