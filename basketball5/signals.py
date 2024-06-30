# In signals.py file

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *

# rt based on your actual model location
from .models import Basketball5, B5Group, B5Fixture


@receiver(post_save, sender=Basketball5)
def create_groups_for_season(sender, instance, created, **kwargs):
    if created:
        # Define the number of groups based on the 'groups' field in the Season model
        num_groups = instance.number_of_groups

        for i in range(1, num_groups + 1):
            group_name = f"GROUP {chr(ord('A') + i - 1)}"
            B5Group.objects.create(name=group_name, competition=instance)


from django.db.models.signals import post_save
from django.dispatch import receiver


# set score to zero and begin th game
@receiver(pre_save, sender=B5Fixture)
def reset_scores_if_inplay(sender, instance, **kwargs):
    if instance.id:
        previous = B5Fixture.objects.get(id=instance.id)
        if previous.status == "Pending" and instance.status == "InPlay":
            instance.team1_score = 0
            instance.team2_score = 0


# update score with event
@receiver(post_save, sender=MatchEvent)
def update_fixture_score(sender, instance, created, **kwargs):
    if created and instance.event_type in ["1-Pointer", "2-Pointer", "3-Pointer"]:
        match = instance.match
        points = 0

        if instance.event_type == "1-Pointer":
            points = 1
        elif instance.event_type == "2-Pointer":
            points = 2
        elif instance.event_type == "3-Pointer":
            points = 3

        if instance.team == match.team1:
            match.team1_score = (match.team1_score or 0) + points
        elif instance.team == match.team2:
            match.team2_score = (match.team2_score or 0) + points
        match.save()


# @receiver(post_save, sender=Fixture)
# def update_standings(sender, instance, **kwargs):
#     team1_standings, _ = Standings.objects.get_or_create(team=instance.team1)
#     team2_standings, _ = Standings.objects.get_or_create(team=instance.team2)

#     team1_standings.update_standings(instance)
#     team2_standings.update_standings(instance)


# def update_standings(standings, match, is_team1):
#     if is_team1:
#         goals_for = match.team1_score
#         goals_against = match.team2_score
#         if match.team1_score > match.team2_score:
#             standings.wins += 1
#             standings.points += 3
#         elif match.team1_score < match.team2_score:
#             standings.losses += 1
#         else:
#             standings.draws += 1
#             standings.points += 1
#     else:
#         goals_for = match.team2_score
#         goals_against = match.team1_score
#         if match.team2_score > match.team1_score:
#             standings.wins += 1
#             standings.points += 3
#         elif match.team2_score < match.team1_score:
#             standings.losses += 1
#         else:
#             standings.draws += 1
#             standings.points += 1

#     standings.goals_for += goals_for
#     standings.goals_against += goals_against
#     standings.goal_difference = standings.goals_for - standings.goals_against
#     standings.save()
