from django.test import TestCase
from api.models import Stat

admin = Stat.objects.create(total_participants=3 , total_teams=1, refused_participants=0, accepted_participants=2)
print(f"Stat object created with total_participants: {admin.total_participants}, total_teams: {admin.total_teams}, refused_participants: {admin.refused_participants}, accepted_participants: {admin.accepted_participants}")