from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Athletics, AthleticsEvent, AthleticsResult, Medal
from .forms import AthleticsForm, AthleticsEventForm, AthleticsResultForm, MedalForm

# Athletic Views


def athletic_list_create_update(request, id=None):
    athletics = Athletics.objects.all()

    if id:
        athletic = get_object_or_404(Athletics, id=id)
    else:
        athletic = None

    if request.method == "POST":
        if id:
            form = AthleticsForm(request.POST, instance=athletic)
        else:
            form = AthleticsForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("athletics")
    else:
        if id:
            form = AthleticsForm(instance=athletic)
        else:
            form = AthleticsForm()

    context = {"athletics": athletics, "form": form, "athletic": athletic}
    return render(request, "athletics/athletics.html", context)


def athletic_detail(request, id):
    athletic = get_object_or_404(Athletics, id=id)
    return render(request, "athletics/athletic_detail.html", {"athletic": athletic})


def athletic_delete(request, id):
    athletic = get_object_or_404(Athletics, id=id)
    if request.method == "POST":
        athletic.delete()
        return redirect("athletic_list")
    return render(request, "athletics/delete.html", {"athletic": athletic})


# AthleticsEvent Views


def athletics_event_list(request):
    events = AthleticsEvent.objects.all()
    return render(request, "athletics_event_list.html", {"events": events})


def athletics_event_detail(request, id):
    event = get_object_or_404(AthleticsEvent, id=id)
    return render(request, "athletics_event_detail.html", {"event": event})


def athletics_event_create(request):
    if request.method == "POST":
        form = AthleticsEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("athletics_event_list")
    else:
        form = AthleticsEventForm()
    return render(request, "athletics_event_form.html", {"form": form})


def athletics_event_update(request, id):
    event = get_object_or_404(AthleticsEvent, id=id)
    if request.method == "POST":
        form = AthleticsEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("athletics_event_list")
    else:
        form = AthleticsEventForm(instance=event)
    return render(request, "athletics_event_form.html", {"form": form})


def athletics_event_delete(request, id):
    event = get_object_or_404(AthleticsEvent, id=id)
    if request.method == "POST":
        event.delete()
        return redirect("athletics_event_list")
    return render(request, "athletics_event_confirm_delete.html", {"event": event})


# AthleticsResult Views


def athletics_result_list(request):
    results = AthleticsResult.objects.all()
    return render(request, "athletics_result_list.html", {"results": results})


def athletics_result_detail(request, id):
    result = get_object_or_404(AthleticsResult, id=id)
    return render(request, "athletics_result_detail.html", {"result": result})


def athletics_result_create(request):
    if request.method == "POST":
        form = AthleticsResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("athletics_result_list")
    else:
        form = AthleticsResultForm()
    return render(request, "athletics_result_form.html", {"form": form})


def athletics_result_update(request, id):
    result = get_object_or_404(AthleticsResult, id=id)
    if request.method == "POST":
        form = AthleticsResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect("athletics_result_list")
    else:
        form = AthleticsResultForm(instance=result)
    return render(request, "athletics_result_form.html", {"form": form})


def athletics_result_delete(request, id):
    result = get_object_or_404(AthleticsResult, id=id)
    if request.method == "POST":
        result.delete()
        return redirect("athletics_result_list")
    return render(request, "athletics_result_confirm_delete.html", {"result": result})


# Medal Views


def medal_list(request):
    medals = Medal.objects.all()
    return render(request, "medal_list.html", {"medals": medals})


def medal_detail(request, id):
    medal = get_object_or_404(Medal, id=id)
    return render(request, "medal_detail.html", {"medal": medal})


def medal_create(request):
    if request.method == "POST":
        form = MedalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("medal_list")
    else:
        form = MedalForm()
    return render(request, "medal_form.html", {"form": form})


def medal_update(request, id):
    medal = get_object_or_404(Medal, id=id)
    if request.method == "POST":
        form = MedalForm(request.POST, instance=medal)
        if form.is_valid():
            form.save()
            return redirect("medal_list")
    else:
        form = MedalForm(instance=medal)
    return render(request, "medal_form.html", {"form": form})


def medal_delete(request, id):
    medal = get_object_or_404(Medal, id=id)
    if request.method == "POST":
        medal.delete()
        return redirect("medal_list")
    return render(request, "medal_confirm_delete.html", {"medal": medal})
