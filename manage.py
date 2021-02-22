from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_app, db
from api.database.models import Report
from tests import db_drop_everything

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

# manage migrations
manager.add_command('db', MigrateCommand)


@manager.command
def routes():
    print(app.url_map)


@manager.command
def db_seed():
    db_drop_everything(db)
    db.create_all()

    # seed anything here we might need
    report = Report(name='Phil', lat=33.39, long=-104.52, description='Saw some stuff', event_type='sighting', image='image.jpeg')
    report2 = Report(name='Austin', lat=40.759372, long=-111.900795, description='talked to some greys', event_type='contact', image='image.jpeg')
    db.session.add(report)
    db.session.add(report2)

    db.session.commit()
    print(f'obj count: {len(db.session.query(Report).all())}')


if __name__ == "__main__":
    manager.run()
