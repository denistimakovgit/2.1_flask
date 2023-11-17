import flask
from flask import views, jsonify, request
from models import Session, Announcements
from sqlalchemy.exc import IntegrityError
from errors import HttpError
from schema import CreateAnnouncement, UpdateAnnouncement
from tools import validate

app = flask.Flask("app")

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error":error.description})
    response.status_code = error.status_code
    return response

def get_announcement(id: int):
    announcement = request.session.get(Announcements, id)
    if announcement is None:
        raise HttpError(status_code=404, description='Announcement not found')
    return announcement

def add_announcement(announcement: Announcements):
    try:
        request.session.add(announcement)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError( status_code=409, description="announcement already exists")

class AnnouncementView(views.MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, id:int):
        announcement = get_announcement(id)
        return jsonify(announcement.dict)

    def post(self):
        announcement_data = validate(CreateAnnouncement, request.json)
        #announcement_data = request.json
        announcement = Announcements(**announcement_data)
        add_announcement(announcement)
        return jsonify({'id': announcement.id})

    def patch(self, id:int):
        announcement = get_announcement(id)
        announcement_data = validate(UpdateAnnouncement, request.json)
        for key, value in announcement_data.items():
            print(key, value)
            setattr(announcement, key, value)
            add_announcement(announcement)
        return jsonify({'id': announcement.id})

    def delete(self, id: int):
        announcement = get_announcement(id)
        self.session.delete(announcement)
        self.session.commit()
        return jsonify({"status":"announcemenet deleted"})

announcement_view = AnnouncementView.as_view("announcement_view")

app.add_url_rule( rule="/api/announcements/<int:id>", view_func=announcement_view,
                  methods=["GET", "PATCH", "DELETE"])
app.add_url_rule( rule="/api/announcements/", view_func=announcement_view, methods=["POST"])


if __name__ == '__main__':
    app.run()


