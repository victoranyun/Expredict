from server import db


class Instagram(db.Model):  # model for each instagram account
    __tablename__ = 'instagram_info'  # name of the table
    id = db.Column(db.Integer, primary_key=True)  # primary key of db (required)
    username = db.Column(db.String())  # instagram username
    access_token = db.Column(db.String())  # access token of the app
    instagram_id = db.Column(db.String())  # instagram user id

    def __init__(self, username, access_token, instagram_id):
        self.username = username
        self.access_token = access_token
        self.instagram_id = instagram_id

    def __repr__(self):  # can return a printable representation of the object
        return '<id {}>'.format(self.id)

    def serialize(self):  # not needed but conventional
        return {
            'id': self.id,
            'username': self.username,
            'access_token': self.access_token,
            'instagram_id': self.instagram_id
        }
