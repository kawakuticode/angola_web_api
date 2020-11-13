from application.application_factory import db
from application.application_factory import ma


class Radio(db.Model):
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
        return f"radio station(name:{self.r_name}, url:{self.url}, stream_link:{self.stream_link}, logo:{self.img_logo})"

    def __repr__(self):
        return "<Radio(name={self.r_name!r} ,url={self.url!r} , stream_link:{self.stream_link!r} ,img_logo:{self.img_logo!r} )>".format(self=self)


class RadioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Radio
        load_instance = True
