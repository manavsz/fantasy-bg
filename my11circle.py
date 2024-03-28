import requests
import imaplib
import email
from email.header import decode_header
import time
import os

class My11Circle:


    urls = {
        'match_points': "https://www.my11circle.com/api/lobbyApi/matches/v1/getMatchPlayerPoints",
        'otp': "https://www.my11circle.com/api/fl/auth/v2/getLogin",
        'login': "https://www.my11circle.com/api/fl/auth/v2/login",
        'matches': "https://www.my11circle.com/api/lobbyApi/v1/getMatches"
    }

    headers = {"Content-Type": "application/json"}

    # data_payload = {
    #     "matchId": 77024
    # }

    cookies = ''

    session = None


    def __init__(self) -> None:
        self.session = requests.Session()
    

    def get_otp(self):

        otp_payload = {
            "loginid": "fantasynag@outlook.com", 
            "deviceId": "5bc3a16e-dea5-4385-814a-9be4e628309f"
        }

        resp = self.session.post(self.urls['otp'], json=otp_payload, headers=self.headers)
        resp_data = resp.json()
        print(resp_data)
        time.sleep(5)
        otp = self.get_otp_from_email()

        resp_data['data']['otp'] = otp

        return resp_data
    
    def login(self, otp_data):

        login_payload = {
            "loginid": "fantasynag@outlook.com", 
            "deviceId": "5bc3a16e-dea5-4385-814a-9be4e628309f",
            "deviceName": "Linux",
            "reasonCode": otp_data["reasonCode"],
            "challenge": otp_data["challenge"],
            "otp": otp_data["otp"]
        }

        login_resp = self.session.post(self.urls['login'], json=login_payload, headers=self.headers)


        return login_resp


    def getMatches(self):
        
        matches_payload = {
            'isNonCashAppVersion': False,
            'sportsType': 1
        }

        match_resp = self.session.post(self.urls['matches'], json=matches_payload, cookies=self.cookies)
        match_resp_data = match_resp.json()


        return match_resp_data
    
    
    
    def getMatchPoints(self, id):
        match_points_payload = {
            'matchId': id
        }

        points_resp = self.session.post(self.urls['match_points'], json=match_points_payload, cookies=self.cookies)
        points_resp_data = points_resp.json()


        return points_resp_data
    

    def refreshSession(self):

        otp_resp = self.get_otp()

        if otp_resp['success']:
            otp_data = otp_resp['data']
            login_resp = self.login(otp_data)
            login_resp_data = login_resp.json()

            if login_resp_data['success']:
                return True
            

        return False
    
    def get_otp_from_email(self):

        otp = ''

        # create an IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        # authenticate
        eml = os.getenv('EMAIL')
        passwrd = os.getenv('EPASS')
        imap.login(eml, passwrd)

        status, messages = imap.select("Inbox")
        # number of top emails to fetch
        N = 1
        # total number of emails
        messages = int(messages[0])
        for i in range(messages, messages - N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            # print(msg)
            for response in msg:
                # print(response[1])
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                # depending on your where your OTP is in the email, you will have to modify the string split method
                                body = body.split(' is your OTP to login')[0]
                                otp = body[-6:]
                                print(otp)
                    else:
                        body = response[1].decode().split(' is your OTP to login')[0]
                        otp = body[-6:]
                        print(otp)

        imap.close()
        imap.logout()
        return otp



# circle = My11Circle()
# valid = circle.refreshSession()

# points = circle.getMatchPoints(77109)
# print(points)

# with open('match3.csv', 'w') as csvf:

#     writer = csv.writer(csvf)

#     writer.writerow(['Name', 'Points'])

#     for p in data['players']:

#         writer.writerow([p['name'], p['points']])
