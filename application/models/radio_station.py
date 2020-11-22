from application.application_factory import db


class Radio(db.Model):
    __tablename__ = 'radio'
    id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.TEXT, index=True, nullable=False)
    url = db.Column(db.TEXT, index=True, nullable=False)
    stream_link = db.Column(db.TEXT, index=True, nullable=False)
    img_logo = db.Column(db.TEXT, index=True, nullable=False)

    def __init__(self, r_name, url, stream_link, img_logo):
        self.r_name = r_name
        self.url = url
        self.stream_link = stream_link
        self.img_logo = img_logo

    def __str__(self):
        return f"Radio(r_name:{self.r_name}, url:{self.url} , stream_link:{self.stream_link} ," \
               f"img_logo:{self.img_logo})"

    def __repr__(self):
        return f"Radio(r_name:{self.r_name}, url:{self.url} , stream_link:{self.stream_link} ," \
               f"img_logo:{self.img_logo})"
