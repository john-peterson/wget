#!/usr/bin/env python3
from sys import exit
from test.http_test import HTTPTest
from misc.wget_file import WgetFile

"""
    This test executed Wget in Spider Browser mode.
"""
TEST_NAME = "Recursive Spider Browser"
############# File Definitions ###############################################
mainpage = """
<html>
<head>
  <title>Main Page</title>
</head>
<body>
  <p>
    Some text and a link to a <a href="http://127.0.0.1:{{port}}/secondpage.html">second page</a>.
    Also, an inline image <img src="http://127.0.0.1:{{port}}/image.svg">
    Also, a linked image <a href="http://127.0.0.1:{{port}}/linkedimage.svg">
    Also, a <a href="http://127.0.0.1:{{port}}/nonexistent">broken link</a>.
  </p>
</body>
</html>
"""


secondpage = """
<html>
<head>
  <title>Second Page</title>
</head>
<body>
  <p>
    Some text and a link to a <a href="http://127.0.0.1:{{port}}/thirdpage.html">third page</a>.
    Also, a <a href="http://127.0.0.1:{{port}}/nonexistent">broken link</a>.
  </p>
</body>
</html>
"""

thirdpage = """
<html>
<head>
  <title>Third Page</title>
</head>
<body>
  <p>
    Some text and a link to a <a href="http://127.0.0.1:{{port}}/dummy.txt">text file</a>.
    Also, another <a href="http://127.0.0.1:{{port}}/againnonexistent">broken link</a>.
  </p>
</body>
</html>
"""

dummyfile = "Don't care."


index_html = WgetFile ("index.html", mainpage)
image_svg = WgetFile ("image.svg", dummyfile)
linkedimage_svg = WgetFile ("linkedimage.svg", dummyfile)
secondpage_html = WgetFile ("secondpage.html", secondpage)
thirdpage_html = WgetFile ("thirdpage.html", thirdpage)
dummy_txt = WgetFile ("dummy.txt", dummyfile)

Request_List = [
    [
        "HEAD /",
        "HEAD /",
        "GET /",
        "GET /robots.txt",
        "HEAD /secondpage.html",
        "HEAD /image.svg",
        "HEAD /linkedimage.svg",
        "HEAD /nonexistent",
        "HEAD /linkedimage.svg",
        "HEAD /image.svg",
        "HEAD /secondpage.html",
        "GET /secondpage.html",
        "HEAD /thirdpage.html",
        "HEAD /thirdpage.html",
        "GET /thirdpage.html",
        "HEAD /dummy.txt",
        "HEAD /againnonexistent",
        "HEAD /dummy.txt",
    ]
]

WGET_OPTIONS = "--spider -r --queue-type=browser"
WGET_URLS = [[""]]

Files = [[index_html, image_svg, linkedimage_svg, secondpage_html, thirdpage_html, dummy_txt]]

ExpectedReturnCode = 0
ExpectedDownloadedFiles = []

################ Pre and Post Test Hooks #####################################
pre_test = {
    "ServerFiles"       : Files
}
test_options = {
    "WgetCommands"      : WGET_OPTIONS,
    "Urls"              : WGET_URLS
}
post_test = {
    "ExpectedFiles"     : ExpectedDownloadedFiles,
    "ExpectedRetcode"   : ExpectedReturnCode,
    "FilesCrawled"      : Request_List
}

err = HTTPTest (
                name=TEST_NAME,
                pre_hook=pre_test,
                test_params=test_options,
                post_hook=post_test
).begin ()

exit (err)
