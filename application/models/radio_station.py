from application.application_factory import db
from application.application_factory import ma


class Radio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.TEXT, index=True, nullable=False)
    url = db.Column(db.TEXT, index=True, nullable=False)
    stream_link = db.Column(db.TEXT, index=True, nullable=False)
    img_logo = db.Column(db.TEXT, index=True, nullable=False)

    '''def __init__(self,id,  r_name, url, stream_link, img_logo):
        self.id = id
        self.r_name = r_name
        self.url = url
        self.stream_link = stream_link
        self.img_logo = img_logo'''

    def __init__(self, r_name, url, stream_link, img_logo):
        self.r_name = r_name
        self.url = url
        self.stream_link = stream_link
        self.img_logo = img_logo

    def __str__(self):
        return "Radio(r_name:{self.r_name!r}, url:{self.url!r} , stream_link:{self.stream_link!r} ," \
               "img_logo:{self.img_logo!r})".format(self=self)

    def __repr__(self):
        return "radio(r_name:{self.r_name!r}, url:{self.url!r} , stream_link:{self.stream_link!r} ," \
               " img_logo:{self.img_logo!r})".format(self=self)

    def asdict(self):
        return {'r_name':self.r_name, 'url':self.url , 'stream_link':self.stream_link , 'img_logo':self.img_logo}
    def __iter__(self):
        yield 'r_name',self.r_name
        yield 'url',self.url
        yield 'stream_link',self.stream_link
        yield 'img_logo',self.img_logo

class RadioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Radio
        load_instance = True
