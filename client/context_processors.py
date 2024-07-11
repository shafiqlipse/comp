from football.models import Football
from netball.models import Fixture,  Netball
from basketball3.models import Basketball3
from handball.models import Handball
from volleyball.models import Volleyball


def football_tournaments(request):
    ftourns = Football.objects.all()
    return {"ftourns": ftourns}


def netball_tournaments(request):
    ntourns = Netball.objects.all()
    return {"ntourns": ntourns}


def basketball3_tournaments(request):
    b3tourns = Basketball3.objects.all()
    return {"b3tourns": b3tourns}


def handball_tournaments(request):
    htourns = Handball.objects.all()
    return {"htourns": htourns}


def volleyball_tournaments(request):
    vtourns = Volleyball.objects.all()
    return {"vtourns": vtourns}


def top_fixtures(request):
    fixtures = Fixture.objects.filter(status="InPlay").order_by("-date")
    return {"top_fixtures": fixtures}
