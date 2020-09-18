import yagmail
yag=yagmail.SMTP("harsh.mangal03acc@gmail.com")
yag.login()
yag.send(to=["harsh_student@citabu.ac.in","hamamagarwal007@gmail.com"],
         subject="Testing Yagmail",
         attachments="/home/harsh/Desktop/redhat.jpg",
         contents="Hello here is pic lit!:"
        )
### can be lists for number of attachments

