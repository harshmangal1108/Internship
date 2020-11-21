try:
    import unittest
    import json
    from api import app
    import pprint
    from main import *
    # from os.path import abspath, dirname
except Exception as e:
    print(format(e))


##################
# ResponseCode
##################
# class ResponseCode(unittest.TestCase):
    # def test_GetAll_no_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configuration/0/")
    #     data = json.loads(response.get_data(as_text=True))
    #     # pprint.pprint(data)
    #     self.assertEqual(response.status_code, 200)

    # def test_GetAll_with_mail(self):
    #     tester =global  app.test_client(self)
    #     response = tester.get("/configuration/1/")
    #     data = json.loads(response.get_data(as_text = True))
    #     pprint.pprint(data)
    #     self.assertEqual(response.status_code, 200)
        
    # ---- Single ----#
    # def test_Single_no_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configs/<string:name>/0/")
    #     data = json.loads(response.get_data(as_text=True))
    #     # pprint.pprint(data)
    #     self.assertEqual(response.status_code, 200)

    # def test_Single_with_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configs/<string:name>/1/", headers={"Content-Type": "application/json"})
    #     data = json.loads(response.get_data(as_text = True))
    #     pprint.pprint(data)
    #     self.assertEqual(response.status_code, 200)



# ##################
# # Split_Sheet
# ##################
# class main_sheet_check(unittest.TestCase):
#     def test_Sheet_no_value_no_mail(self):
#         tester = app.test_client(self)
#         response = tester.get("/configuration/0/")
#         data = json.loads(response.get_data(as_text=True))
#         message = data["final_file"]
#         print(message)
#         assertion = 0
#         if message == "No value in DB or config":
#             assertion = 1
#         self.assertEqual(assertion, 1)
        
#     # def test_Sheet_value_no_mail(self):
#     #     tester = app.test_client(self)
#     #     response = tester.get("/configuration/0/")
#     #     data = json.loads(response.get_data(as_text=True))
#     #     message = data["final_file"]
#     #     print(message)
#     #     assertion = 1
#     #     if message == "values are in DB or config":
#     #         assertion = 0
#     #     self.assertEqual(assertion, 1)



##################
# Mail_Server
##################
'''class mail_mail_check(unittest.TestCase):
    def test_Mail_server_mail_fail(self):
        tester = app.test_client(self)
        response = tester.get("/configuration/0/")
        data = json.loads(response.get_data(as_text=True))
        message = data["mail"]
        assertion = 1
        if message == "Mail Server Error or check Your credentials":
            assertion = 0
        self.assertEqual(assertion, 0)
        
    def test_Mail_server_mail_pass(self):
        tester = app.test_client(self)
        response = tester.get("/configuration/1/")
        data = json.loads(response.get_data(as_text=True))
        message = data["mail"]
        assertion = 0
        if message == "Mail Server Working Please check your mail":
            assertion = 1
        self.assertEqual(assertion, 1)'''


    
    
##################
# ContentType
##################
# class ContentType(unittest.TestCase):
    # def test_GetAll_no_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configuration/0/")
    #     data = json.loads(response.get_data(as_text=True))
    #     # pprint.pprint(data)
    #     self.assertEqual(response.content_type, "application/json")

    # def test_GetAll_with_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configuration/1/")
    #     data = json.loads(response.get_data(as_text = True))
    #     pprint.pprint(data)
    #     self.assertEqual(response.content_type, "application/json")

    # ---- Single ----#
    
    # def test_Single_no_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configs/<string:name>/0/")
    #     data = json.loads(response.get_data(as_text=True))
    #     # pprint.pprint(data)
    #     self.assertEqual(response.content_type, "application/json")

    # def test_Single_with_mail(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/configs/<string:name>/1/")
    #     data = json.loads(response.get_data(as_text = True))
    #     pprint.pprint(data)
    #     self.assertEqual(response.content_type, "application/json")



if __name__ == "__main__":
    unittest.main()
