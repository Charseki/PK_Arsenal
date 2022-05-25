import sys
from urllib.parse import unquote
import pyperclip

# while True:
#     s = input()
#     try:
#         s = s.strip()
#         if s.find(':')!=-1:
#             s = s.split(":")[1].strip().strip(",\"")
#         else:
#             s = s.strip().strip(",\"")
#         s = unquote(s)
#         breaklocal = s.find("********************")
#         if (breaklocal != -1): s = s[:breaklocal]
#         sys.stdout.write(s)
#         pyperclip.copy(s)
#     except Exception as e:
#         print(e)


s = "POST%20/cqva/resources/vendor/orionis/fonts/9816A80F1330C1219B721F47689_1AC12A3D_8C7A.php%3Fpid%3D2%26WalVT%3DJJJ75QQQ%26tagId%3D989321572332339200%26DashboardID%3D0%26nIJIk%3DJJJ75QQQ%26LeafID%3D280586%26mobilephone%3D15632791692%26realp%3D0%26channelIdStr%3D2496%252C2556%252C2632%252C2663%252C2589%252C2850%252C3300%252C%20HTTP/1.1%0D%0AHost%3A%2068.26.4.44%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0Ax-tif-paasid%3A%20hzhz%0D%0ACLIENTIP%3A%20111.19.78.249%0D%0ArtnType%3A%20html%0D%0AX-From-Cdn%3A%20aliyun%0D%0AX-Ws-Request-Id%3A%205f3211d6_PSzqstdxnw128_7620-26398%0D%0AX-FeatureVersion%3A%201%0D%0AX-Office-Major-Version%3A%2016%0D%0AAccept-Encoding%3A%20gzip%2Cdeflate%0D%0Ax-csrftoken%3A%20XnEO0XpCYGJ5Klo9brJjlMYD1BqY13QXKVum2i7Ej7yXuJgPluaqKSDdi9FM8aLu%0D%0AX-SWEB-AuthCustID%3A%201190713419%0D%0APragma%3A%20no-cache%0D%0AX-Real-IP%3A%20118.193.103.11%0D%0AX-SWEB-ClientIP%3A%20z8KubMIQ0H5JKEl4howqTCaGtD%2B8rpiv5WA%3D%0D%0AContent-length%3A%20250%0D%0A%0D%0Acon%3D2%26searchkey%3Dx%26offset%3D%253Cimg%2520src%253D%2522livescript%253Adocument.vulnerable%253Dtrue%253B%2522%253E%26viewUniqueId%3Du8%269%25255B%25255D%3Dph%26nickname%3DGRLpGpAG%26LeafID%3D280586%26pformname%3Db114943b%26Section%3DNoAuthREQ%26fdName%3DZP%26ip%3D111.201.247.233%252C%25E5%258C%2597%25E4%25BA%25AC%25E5%25B8%2582"
try:
    s = s.strip()
    if s.find(':')!=-1:
        s = s.split(":")[1].strip().strip(",\"")
    else:
        s = s.strip().strip(",\"")
    s = unquote(s)
    breaklocal = s.find("********************")
    if (breaklocal != -1): s = s[:breaklocal]
    sys.stdout.write(s)
    pyperclip.copy(s)
except Exception as e:
    print(e)