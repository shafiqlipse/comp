from football.models import Football
from netball.models import NFixture, Netball
from basketball3.models import Basketball3
from basketball5.models import Basketball5
from handball.models import Handball
from volleyball.models import Volleyball
from rugby7s.models import Rugby7s
from rugby15s.models import Rugby15s


def football_tournaments(request):
    ftourns = Football.objects.all()
    return {"ftourns": ftourns}


def netball_tournaments(request):
    ntourns = Netball.objects.all()
    return {"ntourns": ntourns}


def basketball3_tournaments(request):
    b3tourns = Basketball3.objects.all()
    return {"b3tourns": b3tourns}


def basketball5_tournaments(request):
    b5tourns = Basketball5.objects.all()
    return {"b5tourns": b5tourns}


def handball_tournaments(request):
    htourns = Handball.objects.all()
    return {"htourns": htourns}


def volleyball_tournaments(request):
    vtourns = Volleyball.objects.all()
    return {"vtourns": vtourns}

def rugby7s_tournaments(request):
    r7tourns = Rugby7s.objects.all()
    return {"r7tourns": r7tourns}

def rugby15s_tournaments(request):
    r15tourns = Rugby15s.objects.all()
    return {"r15tourns": r15tourns}


from datetime import date


def top_fixtures(request):
    today = date.today()
    fixtures = NFixture.objects.filter(date=today).order_by("-date")
    return {"top_fixtures": fixtures}
