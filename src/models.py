from server import db


class Instagram(db.Model):
    __tablename__ = 'instagram_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    access_token = db.Column(db.String())
    page_id = db.Column(db.String())
    instagram_id = db.Column(db.String())

    def __init__(self, username, access_token, page_id, instagram_id):
        self.username = username
        self.access_token = access_token
        self.page_id = page_id
        self.instagram_id = instagram_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'access_token': self.access_token,
            'page_id': self.page_id,
            'instagram_id': self.instagram_id
        }
