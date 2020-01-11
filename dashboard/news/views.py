from django.shortcuts import render,redirect
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from .models import Headline, UserProfile
from datetime import timedelta, timezone, datetime
import os
import shutil
# Create your views here.
def scrape(request):

    user_profile = UserProfile.objects.filter(user=request.user).first()
    user_profile.last_scrape = datetime.now(timezone.utc)
    user_profile.save()

    #create a session#
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    url = 'https://www.theonion.com/'
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content , "html.parser")
    posts = soup.find_all('div', {'class':'curation-module__item'})#return a list#

    for i in posts:
        link = i.find_all('section',{'class':'content-meta__headline__wrapper'})[1]
        image_source = i.find('img', {'class':'dv4r5q-2 iaqrWM'})['src']
        #print(link.text)
        #print(image_source)

        # stackoverflow solution
        
		media_root = '/Users/matthew/Downloads/dashboard/media_root'
		if not image_source.startswith(("data:image", "javascript")):
			local_filename = image_source.split('/')[-1].split("?")[0]
			r = session.get(image_source, stream=True, verify=False)
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
					f.write(chunk)

			current_image_absolute_path = os.path.abspath(local_filename)
			shutil.move(current_image_absolute_path, media_root)


		# end of stackoverflow

        new_headline = Headline()
        new_headline.title = link
        new_headline.url = link
        new_headline.image =local_filename
        new_headline.save()

    return redirect('/')

scrape()