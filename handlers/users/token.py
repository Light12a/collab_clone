import jwt
import datetime
from utils.config import config

class JwtTokenTransfrom(object):

    def __init__(self, user_id):
        self.user_id = user_id
        

    def _transform_token(self):
        token = {
            "id": self.user_id, 
            "time":int(int(datetime.datetime.strptime(str(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), 
                '%Y-%m-%d %H:%M:%S').timestamp()*1000) +  int(config.getint('token','login_expiry')*1000))}
        res = jwt.encode(token, "secret", algorithm='HS256')

        return res
