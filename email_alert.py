
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
            'Sender': 'sender <sender@mail.com>',
            'To': 'anotheraccount@mail.com',
            'Subject': 'Hello World!',
        },
        enclosure=[
            PlainText('Hi!'),
        ]
    )
    '''

    # this is email with an HTML enclosure, not plaintext like above

    envelope = email(
        sender='sender <sender@gmail.com>',
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
                            <th>The following video is available in Brightcove:</th>
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
            Auth(username='nski@gmail.com', password='123233')
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
        auth=('nski@gmail.com','123223'),
    )

    # send envelope

    response = postman.send(envelope)
    print response.message
    print response.status_code
    return response.status_code


