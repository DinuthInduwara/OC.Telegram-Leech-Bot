import requests, re, urllib
from bs4 import BeautifulSoup




class Bypass:
    def __init__(self):
        self.session = requests.Session()    
    def bypass_redirect(self, url):
        """
        regex: https?://bit\.ly/[^>]+
        regex: https?://(?:link\.zonawibu\.cc/redirect\.php\?go|player\.zafkiel\.net/blogger\.php\?yuzu)\=[^>]+
        """
        head = self.session.head(url)
        return head.headers.get("Location", url)
    
    
    def bypass_fembed(self, url):
        """
        regex: https?://(?:www\.naniplay|naniplay)(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+
        regex: https?://layarkacaxxi\.icu/[fv]/[^>]+
        regex: https?://fem(?:bed|ax20)\.com/[vf]/[^>]+
        """

        url = url.replace("/v/", "/f/")
        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self.bypass_redirect(f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result

    def bypass_streamtape(self, url):
        """
        regex: https?://streamtape\.com/v/[^/]+/[^>]+
        """

        raw = self.session.get(url)

        if re.findall(r"document.*((?=id\=)[^\"']+)", raw.text):
            videolink = re.findall(r"document.*((?=id\=)[^\"']+)", raw.text)
            nexturl = "https://streamtape.com/get_video?" + videolink[-1]
         
            if self.bypass_redirect(nexturl):
                redirect = self.bypass_redirect(nexturl)
                return redirect
            





async def gen_link(url, imp=None):
    session = requests.Session()
    if (
        "mega.nz" in url
        or "uptobox.com" in url
        or "1fiecher.com" in url
    ):
        return None

    # streamtape.com
    elif imp == "st" or "streamtape.com" in url:
        cli = Bypass()
        return cli.bypass_streamtape(url)
    
    
    # fembed.com
    elif imp == "fem":
        cli = Bypass()
        x = cli.bypass_fembed(url)
        if '1080p/mp4' in x:
            return x['1080p/mp4']
        elif '720p/mp4' in x:
            return x['720p/mp4']
        elif '480p/mp4' in x:
            return x['480p/mp4']
        elif '360p/mp4' in x:
            return x['360p/mp4']
    
    # mediafire.com
    elif "mediafire.com" in url:
        try:
            link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]

            resp = await session.get(link)
            restext = await resp.text

            page = BeautifulSoup(restext, "lxml")
            info = page.find("a", {"aria-label": "Download file"})
            ourl = info.get("href")
            return ourl
        except:
            return None
    
    # google drive
    elif "drive.google.com" in url:
        API_KEY= 'AIzaSyCgLwZyQowbFOlvQ1YDt0F6DdQdyiXQ8Lg'
        SPLITID =  url.split("/")
        FILEID =(SPLITID[5])
        DIRECT = (f"https://www.googleapis.com/drive/v3/files/{FILEID}?alt=media&key={API_KEY}")
        return DIRECT

    # disk.yandex.com
    elif "yadi.sk" in url or "disk.yandex.com" in url:
        try:
            link = re.findall(
                r"\b(https?://.*(yadi|disk)\.(sk|yandex)*(|com)\S+)", url
            )[0][0]
            print(link)
        except:
            return None

        api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
        try:
            resp = await session.get(api.format(link))
            restext = await resp.json()
            ourl = restext["href"]
            return ourl
        except:
            return None

    # zippyshare.com
    elif "zippyshare.com" in url:
        try:
            link = re.findall(r"\bhttps?://.*zippyshare\.com\S+", url)[0]
            resp = await session.get(link)
            restext = await resp.text
            base_url = re.search("http.+.com", restext).group()
            page_soup = BeautifulSoup(restext, "lxml")
            scripts = page_soup.find_all("script", {"type": "text/javascript"})
            for script in scripts:
                if "getElementById('dlbutton')" in script.text:
                    url_raw = re.search(
                        r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
                    ).group("url")
                    math = re.search(
                        r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
                    ).group("math")
                    url = url_raw.replace(math, '"' + str(eval(math)) + '"')
                    break
            ourl = base_url + eval(url)
            urllib.parse.unquote(url.split("/")[-1])
            return ourl
        except:
            return None

    # racaty.net
    elif "racaty.net" in url:
        try:
            link = re.findall(r"\bhttps?://.*racaty\.net\S+", url)[0]

            resp = await session.get(link)
            restext = await resp.text
            bss = BeautifulSoup(restext, "html.parser")
            op = bss.find("input", {"name": "op"})["value"]
            id = bss.find("input", {"name": "id"})["value"]


            rep = await session.post(link, data={"op": op, "id": id})
            reptext = rep.text
            bss2 = BeautifulSoup(reptext, "html.parser")
            ourl = bss2.find("a", {"id": "uniqueExpirylink"})["href"]
            return ourl
        except:
            return None

    elif "pixeldrain.com" in url:
        url = url.strip("/ ")
        file_id = url.split("/")[-1]

        info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
        dl_link = f"https://pixeldrain.com/api/file/{file_id}"


        resp = await session.get(info_link)
        restext = await resp.json()

        if restext["success"]:
            return dl_link
        else:
            return None
    else:return url