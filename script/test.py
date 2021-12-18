import requests
import ssl
import sys
from bs4 import BeautifulSoup

#Warningの非表示
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#プロキシ設定
proxies = {
  "http(またはhttps)": "<プロキシサーバ>:<ポート番号>",
}

url = "<URL>"
#引数にプロキシ設定，オートリダイレクトOFF，SSL認証OFFを指定してリクエスト
r = requests.get("https://www.ugtop.com/spill.shtml",proxies=proxies,verify=False,allow_redirects = False)
print (r)

#要素を抽出
soup = BeautifulSoup(r.text, 'lxml')

#HTMLファイルとして保存したい場合はファイルオープンして保存
with open('originDataOld.html', mode='w', encoding = 'utf-8') as fw:
    fw.write(soup.prettify())