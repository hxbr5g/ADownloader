import time
import cloudscraper
import re
import subprocess
import os
from unpacker import decode_packed_codes
# 从网上 楚人无依大佬博客抄的解密函数
# https://www.cnblogs.com/crwy/p/7659579.html
# https://github.com/yt-dlp/yt-dlp

# 定义用到的变量
out_result = ''
re_title = ''
scraper = cloudscraper.create_scraper()
site_pattern = ''
#设置用clash的代理

http_proxy  = "http://127.0.0.1:7890"
https_proxy = "http://127.0.0.1:7890"
ftp_proxy   = "ftp://127.0.0.1:7890"

proxies = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

def get_m3u8(url):
    title_pattern = re.compile(r'<title>(.*?)</title>')#定义标题查询规则
    jable_pattern = 'jable'
    missav_pattern = 'missav'
    global site_pattern
    get_result = scraper.get(url,proxies=proxies)#抓取网页信息
    if (re.findall(jable_pattern,url)):
        print('是JABLE')
        site_pattern = 'jable'
        result = re.search("https://.+m3u8", get_result.text)#jable查找m3u
    elif (re.findall(missav_pattern,url)):
        print('是MISSAV')
        site_pattern = 'missav'
        result = re.search(r"(?<=eval).*", get_result.text)#先找到包含m3u8网址的文字段
        result = re.search("https://.+m3u8", decode_packed_codes(result[0]).split(';',1)[0])#先解码再提取m3u8
    else:
        print('不支持的站点')
    titles  = title_pattern.findall(get_result.text)#查找标题
    titles = titles[0].split(' - J',1)[0]#调整标题名字
    print(result[0])
    print(titles)
    return result[0],titles[0:8]#返回标题

def main_thread(main_url):
    while out_result == '':
        re,re_title = get_m3u8(main_url)
        time.sleep(1.2)
        print(site_pattern)
        if re != '':
            print('已经得到正确的结果，等待下一步操作')
            script_directory = os.path.dirname(os.path.abspath(__file__))   # 获取当前脚本所在的目录
            
            print("当前工作目录为：  " + script_directory)
            cli_program = script_directory + "\\N_m3u8DL-RE.exe "      # 设置核心执行程序的位置
            
            print("当前工作文件为：  " + cli_program)
            if site_pattern == "jable":
                command = [cli_program,re,"--tmp-dir","./tmp","--save-dir","./Download","--save-name",re_title,"--use-system-proxy" ]#执行外部命令行
                subprocess.run(command)
                break
            elif site_pattern == "missav":
                print('这里')
                command = [cli_program,re,"--tmp-dir","./tmp","--save-dir","./Download","--save-name",re_title,"--header","'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'","--header","Origin:https://missav.com","--header","Sec-Fetch-Mode:cors","--header","Sec-Fetch-Site:cross-site","--auto-select","true"]#执行外部命令行
                subprocess.run(command)
                break
            else:
                print('未匹配的站点')
        else:
            time.sleep(1.2)
            continue

if __name__ == '__main__':
    any_url =input('请输入类似https://jable.tv/videos/msfh-054/这样的网址\n')
    main_thread(any_url)
