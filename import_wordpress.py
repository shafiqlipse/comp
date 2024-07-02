import xml.etree.ElementTree as ET


import os
from django.utils.dateparse import parse_datetime

import os
import django


# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")
# Initialize Django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.contrib.auth.models import User
from django.conf import settings
application = get_wsgi_application()

from news.models import Post, Sport, Championship, Categories


def import_wordpress_posts(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for item in root.findall("./channel/item"):
        title = item.find("title").text
        content = item.find(
            "content:encoded",
            namespaces={"content": "http://purl.org/rss/1.0/modules/content/"},
        ).text
        pub_date_str = item.find("pubDate").text
        pub_date = parse_datetime(pub_date_str)

        # You might need to adjust these based on your WordPress export structure
        author_name = item.find(
            "dc:creator", namespaces={"dc": "http://purl.org/dc/elements/1.1/"}
        ).text
        author, _ = User.objects.get_or_create(username=author_name)

        # These fields might not be in your WordPress export, so we're setting them to None
        sport = None
        championship = None
        category = None

        # If you have category information in your XML, you could parse it like this:
        # category_name = item.find('category').text
        # category, _ = Categories.objects.get_or_create(name=category_name)

        Post.objects.create(
            title=title,
            content=content,
            pub_date=pub_date,
            author=author,
            sport=sport,
            championship=championship,
            category=category,
        )


if __name__ == "__main__":
    xml_file_path = "Posts-Export-2024-July-02-0357.xml"
    import_wordpress_posts(xml_file_path)
