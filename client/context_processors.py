from football.models import *
from netball.models import *
from basketball3.models import *
from basketball5.models import *
from handball.models import *
from volleyball.models import *
from rugby7s.models import *
from rugby15s.models import *
from hockey.models import *


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


def hockey_tournaments(request):
    hotourns = Hockey.objects.all()
    return {"hotourns": hotourns}


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
    fot_fixtures = Fixture.objects.filter(date=today).order_by("-date")
    return {"fot_fixtures": fot_fixtures}


def top_nfixtures(request):
    today = date.today()
    net_fixtures = NFixture.objects.filter(date=today).order_by("-date")
    return {"net_fixtures": net_fixtures}


def top_hofixtures(request):
    today = date.today()
    hot_fixtures = HoFixture.objects.filter(date=today).order_by("-date")
    return {"hot_fixtures": hot_fixtures}


def top_vfixtures(request):
    today = date.today()
    vol_fixtures = VFixture.objects.filter(date=today).order_by("-date")
    return {"vol_fixtures": vol_fixtures}


def top_hfixtures(request):
    today = date.today()
    han_fixtures = HFixture.objects.filter(date=today).order_by("-date")
    return {"han_fixtures": han_fixtures}


def top_bfixtures(request):
    today = date.today()
    bas5_fixtures = B5Fixture.objects.filter(date=today).order_by("-date")
    return {"bas5_fixtures": bas5_fixtures}


def top_b3fixtures(request):
    today = date.today()
    b3fixtures = B3Fixture.objects.filter(date=today).order_by("-date")
    return {"b3fixtures": b3fixtures}
