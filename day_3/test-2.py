import re

content = '''Subject: Re: Spam
From: Foo Fie <foo@bar.baz>
To: Magnus Lie Hetland <magnus@bozz.floop>
CC: <Mr.Gumby@bar.baz>
Message-ID: <B8467D62.84F foo@baz.com> %
In-Reply-To: <20041219013308.A2655@bozz.floop> Mime-version: 1.0
Content-type: text/plain; charset="US-ASCII" Content-transfer-encoding: 7bit
Status: RO
Content-Length: 55
Lines: 6
So long, and thanks for all the spam!
Yours,
Foo Fie'''
res = re.findall('<.+>', content)
print(res)
for i in res:
    i = i[1:-1]
    print(i)

