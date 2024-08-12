# In signals.py file

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *

# rt based on your actual model location
from .models import Handball, HGroup


# create groups
@receiver(post_save, sender=Handball)
def create_groups_for_season(sender, instance, created, **kwargs):
    if created:
        # Define the number of groups based on the 'groups' field in the Season model
        num_groups = instance.number_of_groups

        for i in range(1, num_groups + 1):
            group_name = f"GROUP {chr(ord('A') + i - 1)}"
            HGroup.objects.create(name=group_name, competition=instance)


# set score to zero and begin th game
@receiver(pre_save, sender=HFixture)
def reset_scores_if_inplay(sender, instance, **kwargs):
    if instance.id:
        previous = HFixture.objects.get(id=instance.id)
        if previous.status == "Pending" and instance.status == "InPlay":
            instance.team1_score = 0
            instance.team2_score = 0


# update score with event
@receiver(post_save, sender=MatchEvent)
def update_fixture_score(sender, instance, created, **kwargs):
    if created and instance.event_type == "Goal":
        match = instance.match
        if instance.team == match.team1:
            match.team1_score = (match.team1_score or 0) + 1
        elif instance.team == match.team2:
            match.team2_score = (match.team2_score or 0) + 1
        match.save()
