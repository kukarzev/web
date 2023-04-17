import os
#import ftfy
import pandas as pd
#from bs4 import BeautifulSoup
from shutil import copyfile
from datetime import date, timedelta
import random


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_random_resource(df):
    ind = random.randint(0,df.shape[0]-1)
    _title = df["title"].to_list()[ind]
    _url = df["url"].to_list()[ind]
    return _title, _url

        
if __name__=='__main__':
    _dt = []
    _title = []
    _preview = []
    _text = []
    _author = []
    _id = []

    _featured = pd.read_csv("featured.csv")
    _books = pd.read_csv("books.csv")
    _dictionaries = pd.read_csv("dictionaries.csv")
    _memes = pd.read_csv("memes.csv")
    _textbooks = pd.read_csv("textbooks.csv")
    
    start_date = date(2023, 4, 1)
    end_date = date(2023, 5, 1)

    for i,_date in enumerate(daterange(start_date, end_date)):

        the_book = get_random_resource(_books)
        the_dictionary = get_random_resource(_dictionaries)
        the_meme = get_random_resource(_memes)
        the_textbook = get_random_resource(_textbooks)
        
        the_title = "Materials and Schedule"
        the_preview = '''
It is going to be an awesome day! Click on the title to see the details.
        '''
        the_text = f'''
<h2>Your materials needed for today (download if you need to!):</h2>

<img class="size-medium wp-image-7 alignright" style="font-size: 1rem;" src="http://lanlibrary.local/wp-content/uploads/images/{random.choice(_featured.featured.to_list())}" width="200pt" alt="featured_image"/>
Read <a href="{the_book[1]}">{the_book[0]}.</a> Refer to the <a href="{the_dictionary[1]}">{the_dictionary[0]}</a> as needed. Submit two hand-written copies.

Start reading <a href="{the_textbook[1]}"> chapter {random.randint(0,10)} of the {the_textbook[0]} textbook.</a>

Check out <a href="{the_meme[1]}">{the_meme[0]}</a> (there will be a quiz).

<h2>Day Schedule</h2>
<dl>
<dt>8:00am - 8:30am</dt>
<dd>The Principal’s Morning Show - Instead of the regular morning announcements, the principal and some teachers will put on a skit or song based on acclamation.</dd>
</dl>

<dl>
<dt>8:30am - 9:30am</dt>
<dd>Nap Time - Since most high schoolers don't get enough sleep, this period is devoted to a good old-fashioned nap. Students can bring in their own pillows and blankets and catch up on some much-needed rest.</dd>
</dl>

<dl>
<dt>9:30am - 10:30am</dt>
<dd>Pajama Day Fashion Show - Students come to school in their favorite pajamas and show off their creative bedtime attire on a makeshift runway.</dd>
</dl>

<dl>
<dt>10:30am - 11:30am</dt>
<dd>Hot Dog Eating Contest - Who can eat the most hot dogs in one minute? Find out during this fun competition.</dd>
</dl>

<dl>
<dt>11:30am - 12:30pm</dt>
<dd>Dodgeball Tournament - Students split up into teams and battle it out in a heated game of dodgeball.</dd>
</dl>

<dl>
<dt>12:30pm - 1:30pm</dt>
<dd>Gourmet Lunch - The school cafeteria serves up a fancy meal complete with linen tablecloths and real silverware.</dd>
</dl>

<dl>
<dt>1:30pm - 2:30pm</dt>
<dd>Talent Show - Students showcase their unique talents, whether it be singing, dancing, or juggling.</dd>
</dl>

<dl>
<dt>2:30pm - 3:00pm</dt>
<dd>Snack Break - The school provides a variety of snacks to fuel students up for the final stretch of the day.</dd>
</dl>

<dl>
<dt>3:00pm - 4:00pm</dt>
<dd>Movie Time - The day ends with a screening of a classic comedy movie, like "The Breakfast Club" or "Ferris Bueller's Day Off".</dd>
</dl>

        '''

        # weekend
        if _date.weekday() in [5,6]:
            the_text = f"""
<img class="size-medium wp-image-7 alignright" style="font-size: 1rem;" src="http://lanlibrary.local/wp-content/uploads/images/{random.choice(_featured.featured.to_list())}" width="200pt" alt="featured_image"/>
<b>Chill, it's the weekend! Do your homework and sleep well.</b>
            """
            the_preview = the_text
        
        _dt.append(_date)
        _title.append(the_title)
        _preview.append(the_preview)
        _text.append(the_text)
        _author.append("admin")
        _id.append(f"{i}-asdf")
        
    df = pd.DataFrame({'date':_dt,
                       'title':_title,
                       'preview':_preview,
                       'text':_text,
                       'author':_author,
                       "id":_id
    })

    df.loc[:,['author','date','title','preview','text','id']].to_csv('schedule_april2.csv',index=False)
    print(df.head())
