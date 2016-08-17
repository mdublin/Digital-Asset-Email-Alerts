
This script uses the Mailthon package to send email alerts — in this case configured to work with Gmail — to send email alerts that are trigged when assets with specific metatags appear in a digital asset CMS or MAM system. 

The CMS or MAM can be pinged any which way; in this particular example, we're using an mrss API feed, but the method isn't important. As long as you have a simple database setup to handle the deduplication functionality, and parse your CMS/MAM query results efficiently, you can use the `email_alert.py` script to be triggered to send a nicely formatted email alert (styled with Bootstrap) to any number of recipients.

To deploy:

1. Create a virtualenv package via `$ virtualenv env`
2. Install the dependencies via `$ pip install -r requirements.txt`
3. Make sure you have sqlite3 installed
4. If you're running this via cron job, which is how it typically would be implemented, make sure that you provide the right URI to your .db file. Depending upon where you create your cron job via `$ crontab -e` you need to make sure the create_engine URI is correct. For example, if you create a cron job in your home directory, which is one directory above the projectfile, you need to amened the URI so something like `sqlite3:///projectdirectory/notifications.db` instead of just `sqlite3:///notifications.db`
5. To run: `$ python BC_CMS_SEARCH.py`


