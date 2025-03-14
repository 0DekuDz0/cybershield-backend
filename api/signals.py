from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from api.models import Participant, Team,Stat


@receiver(post_save, sender=Participant)
def update_participant_stat(sender, instance, **kwargs):
    update_stat_model()

@receiver(post_save, sender=Team)
def update_team_stat(sender, instance, **kwargs):
    update_stat_model()

@receiver(post_delete, sender=Participant)
def update_participant_stat_on_delete(sender, instance, **kwargs):
    stat, _ = Stat.objects.get_or_create(id=1)  
    stat.refused_participants += 1
    stat.total_participants -= 1
    if instance.participant_status == 'Accepted':
        stat.accepted_participants -= 1

    stat.save()
    print('Participant deleted')


@receiver(post_delete, sender=Team)
def update_participant_stat_on_delete(sender, instance, **kwargs):
    stat, _ = Stat.objects.get_or_create(id=1)  
    stat.total_teams -= 1
    stat.save()
    print('Team deleted')


def update_stat_model():
    """Helper function to update the Stat model"""
    total_participants = Participant.objects.count()
    total_teams = Team.objects.count()
    accepted_participants = Participant.objects.filter(participant_status='Accepted').count()

    stat, _ = Stat.objects.get_or_create(id=1)
    stat.total_participants = total_participants
    stat.total_teams = total_teams
    stat.refused_participants = stat.refused_participants
    stat.accepted_participants = accepted_participants
    stat.all_participants += 1
    stat.all_teams += 1
    stat.save()