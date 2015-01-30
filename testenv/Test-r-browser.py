#!/usr/bin/env python3
from sys import exit
from test.http_test import HTTPTest
from misc.wget_file import WgetFile

"""
    This test executed Wget in Browser mode.
"""
TEST_NAME = "Recursive Browser"
############# File Definitions ###############################################
mainpage = """
<html>
<head>
  <title>Main Page</title>
</head>
<body>
  <p>
    Some text and a link to a <a href="secondpage.html">second page</a>.
    Also, an inline image <img src="image.svg">
    Also, a linked image <a href="linkedimage.svg">
    Also, a <a href="nonexistent">broken link</a>.
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
    Some text and a link to a <a href="thirdpage.html">third page</a>.
    Also, a <a href="nonexistent">broken link</a>.
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
    Some text and a link to a <a href="dummy.txt">text file</a>.
    Also, another <a href="againnonexistent">broken link</a>.
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
        "GET /",
        "GET /robots.txt",
        "HEAD /secondpage.html",
        "HEAD /image.svg",
        "HEAD /linkedimage.svg",
        "HEAD /nonexistent",
        "GET /linkedimage.svg",
        "GET /image.svg",
        "GET /secondpage.html",
        "HEAD /thirdpage.html",
        "GET /thirdpage.html",
        "HEAD /dummy.txt",
        "HEAD /againnonexistent",
        "GET /dummy.txt",
    ]
]

WGET_OPTIONS = "-r -nd --queue-type=browser"
WGET_URLS = [[""]]

Files = [[index_html, image_svg, linkedimage_svg, secondpage_html, thirdpage_html, dummy_txt]]

ExpectedReturnCode = 0
ExpectedDownloadedFiles = Files[0]

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
