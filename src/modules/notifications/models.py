from src.app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    title = db.Column(db.String(128), unique=False, nullable=True)
    description = db.Column(db.String(256), unique=False, nullable=True)

    def __repr__(self):
        return f'Notification {self.name} - {self.id}'


class UserReadNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return f'UserReadNotification {self.name} - {self.id}'
