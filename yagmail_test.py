import yagmail
yag=yagmail.SMTP("sarvidigilocker@gmail.com")
yag.login()
yag.send(to=["18eucs100@skcet.ac.in"],
        subject="Testing Yagmail",
        attachments="",
        contents="Hello here is pic lit!:"
        )
yag.close()
### can be lists for number of attachments

