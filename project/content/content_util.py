from project import db
import project.models as models


# Get all schemas from models.py
user_schema = models.UserSchema()
video_schema = models.VideoSchema()


# User API helper function
def get_user(user_id, dump_schema=False):
    user = models.User.query.filter_by(id=user_id).first()
    return user_schema.dump(user) if dump_schema else user


def get_all_users(dump_schema=False):
    users = models.User.query.all()
    return [user_schema.dump(user) for user in users] if dump_schema else user


def add_user(args, dump_schema=False):
    new_user = models.User(name=args['name'])
    db.session.add(new_user)
    db.session.commit()
    return get_user(new_user.id, dump_schema=dump_schema)


# Video API helper function
def get_video(video_id, dump_schema=False):
    video = models.Video.query.filter_by(id=video_id).first()
    return video_schema.dump(video) if dump_schema else video


def get_all_videos(dump_schema=False):
    videos = models.Video.query.all()
    return [video_schema.dump(video) for video in videos] if dump_schema else video


def add_video(args, dump_schema=False):
    if models.Video.query.filter_by(youtube_id=args['youtube_id']).first():
        return {}
    new_video = models.Video(
        youtube_id=args['youtube_id'],
        title=args['title'],
        author=args['author'],
        url=args['url'],
        thumbnail_url=args['thumbnail_url'],
        progress=0,
        user_id=args['user_id'])
    db.session.add(new_video)
    db.session.commit()
    return get_video(new_video.id, dump_schema=dump_schema)
