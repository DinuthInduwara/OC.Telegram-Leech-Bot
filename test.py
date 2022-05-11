# import sys
# import requests
# import mimetypes
# url ='https://awscc3001.r18.com/litevideo/freepv/j/jul/jul00794/jul00794_dmb_w.mp4'

# def filenamegen(url, content_type):
#     filename = url.split("/")[-1].replace('%', ' ').strip()
#     if filename == "":
#         filename = url.split("/")[-2].replace('%', ' ').strip()
#     if '.' not in filename:
#         filename = filename+mimetypes.guess_extension(content_type)
#     return filename



# def download(url,  filename=None):
#     response = requests.get(url, stream=True)
#     total = response.headers.get('content-length')
#     filename = filenamegen(url, response.headers.get('content-type').strip())
    
#     with open('./downloads/'+filename, 'wb') as f:
#         if total is None:
#             f.write(response.content)
#         else:
#             downloaded = 0
#             total = int(total)
#             for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
#                 downloaded += len(data)
#                 f.write(data)
#                 done = int(50*downloaded/total)
#                 sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
#                 sys.stdout.flush()
#     sys.stdout.write('\n')

# download(url)


# import subprocess
# url = "https://sample.mgstage.com/sample/prestige/yrh/295/yrh-295_20211018T155302.mp4"


# x = subprocess.Popen(["wget", url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)



# for i in iter(x.stdout.readline, b''):
    
#     print(i.decode().strip())



import os 


x = [i for i in range(1, 100)]

output = []
for i in range(0 , len(x), 10):
    l = x[i: i+10]
    output.append(l)
print(output)