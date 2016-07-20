
# this script uses Mailthon:
# http://mailthon.readthedocs.io/en/latest/quickstart.html#quickstart
# https://github.com/eugene-eeo/mailthon


from mailthon.envelope import Envelope
from mailthon.enclosure import PlainText

# for create postman instance
from mailthon.postman import Postman
from mailthon.middleware import TLS, Auth

from mailthon import postman as postman_

from mailthon import email

# db imports
from models import Base, Video
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine



engine = create_engine('sqlite:///notifications.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


# sometimes you need to debug the email server:
# http://stackoverflow.com/questions/17708141/connecting-to-gmail-from-python

def send_alert(alert_video_package):

    print alert_video_package

    title = alert_video_package["name"]
    bc_id = alert_video_package["videoID"]
    bc_desc = alert_video_package["description"]
    video_url = alert_video_package["url"]

    
    # this is an "envelope" that is an email
    '''
    envelope = Envelope(
        headers={
            'Sender': 'sender <linski@mail.com>',
            'To': 'genius@mail.com',
            'Subject': 'Hello World!',
        },
        enclosure=[
            PlainText('Hi!'),
        ]
    )
    '''

    # this is email with an HTML enclosure, not plaintext like above

    envelope = email(
        sender='sender <linski@gmail.com>',
        receivers=['dude@company.com', 'genius@gmail.com'],
        subject='Rio Olympics video alert',
        content="""\
                <html>
                <head>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
                </head>
                <body>
                <table class="table table-inverse">
                    <thead>
                        <tr>
                            <th>The following video is available in Gannett - USA TODAY Brightcove account:</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th scope="row">Title:</th>
                                <td>%s</td>
                        </tr>
                        <tr>
                            <th scope="row">Video ID:</th>
                                <td>%s</td>
                        </tr>
                        <tr>
                            <th scope="row">Description:</th>
                                <td>%s</td>
                        </tr>
                        <tr>
                            <th scope="row">Source File URL:</th>
                                <td>%s</td>
                        </tr>
                    </tbody>
                    </table>
                    </body>
                    </html> """ % (title, bc_id, bc_desc, video_url)
                          
    
    
    
    )

    # this is a "postman" configured for Gmail
    '''
    postman = Postman(
        host='mail.google.com',
        port=587,
        middlewares=[
            TLS(force=True),
            Auth(username='youremail@gmail.com', password='23123')
        ],
    )
    '''

    # https://support.google.com/a/answer/176600?hl=en
    # using postman function, simpler version of above function
    postman = postman_(
        #host='mail.google.com',
        host='smtp.gmail.com',
        port=587,
        force_tls=True,
        auth=('youremail@gmail.com', password='23123'),
    )

    # send envelope

    response = postman.send(envelope)
    print response.message
    print response.status_code

    # check for SMTP replay code of 250 == Requested mail action okay, completed
    if response.status_code == 250:
        video = Video(title = title, bc_id = bc_id, Google_server_response = response.message)
        session.add(video)
        session.commit()

    return response.status_code



