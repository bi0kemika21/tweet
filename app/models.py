from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class Trends(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    keyword = db.Column(db.String(140))  
    woe_id = db.Column(db.Integer)
    woe_code = db.Column(db.String(6))
    timestamp = db.Column(db.DateTime)    

    def __repr__(self):
        return ' %r' % (self.keyword)

        
class Trace(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(140))
    tweet = db.Column(db.String(140))
    retweet = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    name = db.Column(db.String(140))
    real = db.Column(db.String(140))
    pic = db.Column(db.String(140))
    followers = db.Column(db.Integer)
    date = db.Column(db.String(140))
    embed = db.Column(db.String(140))
    enable = db.Column(db.Boolean)
    def __repr__(self):
        return ' %r' % (self.key)
class Search(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(140))
    tweet = db.Column(db.String(140))
    retweet = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    name = db.Column(db.String(140))
    real = db.Column(db.String(140))
    pic = db.Column(db.String(140))
    followers = db.Column(db.Integer)
    date = db.Column(db.String(140))    
    embed = db.Column(db.String(140))

    
    def __repr__(self):
        return ' %r' % (self.key)