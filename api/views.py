from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Participant,Team,Admin
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
import json
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .decorators import is_admin
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken


@csrf_exempt
@api_view(['GET']) 
@is_admin
def get_participants(request):
    try:
        if request.method == 'GET':
            participants = list(Participant.objects.values())  
            return Response({'participants': participants})
        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@api_view(['GET'])
@is_admin
def get_participant_by_id(request):
    try:
        if request.method == 'GET':
            participant_id = request.GET.get('participant_id')
            if not participant_id:
                return Response({'error': 'Missing participant_id'}, status=400)

            participant = get_object_or_404(Participant, participant_id=participant_id)
            participant = model_to_dict(participant)
            print(participant)
            return Response({'participant': participant})

        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@login_required
@csrf_exempt
@api_view(['GET'])
@is_admin
def get_participants_by_name(request):
    try:
        if request.method == 'GET':
            participant_name = request.GET.get('participant_name')
            if not participant_name:
                return Response({'error': 'Missing participant_name'}, status=400)

            participants = list(Participant.objects.filter(participant_name=participant_name).values())
            return Response({'participants': participants})

        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    


@login_required
@csrf_exempt
@api_view(['GET'])
@is_admin
def get_participant_by_email(request):
    try:
        if request.method == 'GET':
            participant_email = request.GET.get('participant_email')
            if not participant_email:
                return Response({'error': 'Missing participant_email'}, status=400)

            participant = get_object_or_404(Participant, participant_email=participant_email)
            participant = model_to_dict(participant)
            return Response({'participant': participant})

        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@api_view(['GET'])
@is_admin
def get_participants_by_status(request):
    try:
            if request.method == 'GET':
                participant_status = request.GET.get('get_participant_by_status')
                if not participant_status:
                    return Response({'error': 'Missing participant_status'}, status=400)

                participants = list(Participant.objects.filter(participant_status=participant_status).values())
                return Response({'participants': participants})

            return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@api_view(['GET'])
@is_admin
def get_participants_by_team(request):
    try: 
            if request.method == 'GET':
                team_id = request.GET.get('participant_team')
                if not team_id:
                    return Response({'error': 'Missing team_id'}, status=400)

                participants = list(Participant.objects.filter(participant_team=team_id).values())
                return Response({'participants': participants})

            return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['POST'])
def add_participant(request):
    try:
        data = json.loads(request.body)
        if request.method == 'POST':
            participant_name = request.data.get('participant_name')
            participant_email = request.data.get('participant_email')
            participant_phone = request.data.get('participant_phone')
            participant_dateOfBirth = request.data.get('participant_dateOfBirth')
            participant_skills = request.data.get('participant_skills')
            participant_linkedin = request.data.get('participant_linkedin')
            participant_github = request.data.get('participant_github')
            participant_portfolio = request.data.get('participant_portfolio')
            participant_haveParticipated = request.data.get('participant_haveParticipated')
            participant_previousExperience = request.data.get('participant_previousExperience')
            participant_status = request.data.get('participant_status')
            participant_team = request.data.get('participant_team')
            new_team = request.data.get('new_team')
            team_name = request.data.get('team_name')

            print("New team",new_team)

            # Vérifier les champs obligatoires
            required_fields = [
                participant_name, participant_email, participant_phone,
                participant_dateOfBirth, participant_skills, participant_linkedin,
                participant_github, participant_haveParticipated,new_team,team_name
            ]

            if any(field is None or field.strip() == "" for field in required_fields):
                return Response({'error': 'Missing required fields'}, status=400)

            participant = Participant(
                participant_name=participant_name,
                participant_email=participant_email,
                participant_phone=participant_phone,
                participant_dateOfBirth=participant_dateOfBirth,
                participant_skills=participant_skills,
                participant_linkedin=participant_linkedin,
                participant_github=participant_github,
                participant_portfolio=participant_portfolio,
                participant_haveParticipated=participant_haveParticipated,
                participant_previousExperience=participant_previousExperience,
                participant_status='Pending',
            )

            if new_team == 'True':
                print("********Creating new team")
                participant.save()  
                team = Team(team_name=team_name, team_leader=participant)
                team.save()
                participant.participant_team = team
                participant.save() 
            else:
                if team_name: 
                    team = get_object_or_404(Team, team_name=team_name)
                    participant.participant_team = team

            participant.save()  
            return Response({
                'response': {
                    'participant_id': participant.pk,
                    'participant_name': participant.participant_name,
                    'participant_email': participant.participant_email,
                    'team_id': participant.participant_team.team_id if participant.participant_team else None,
                    'team_name': participant.participant_team.team_name if participant.participant_team else None
                }
            }, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@api_view(['DELETE'])
@is_admin
def delete_participant(request):
    try:
        if request.method == 'DELETE': 
            participant_id = request.GET.get('participant_id')
            Participant.objects.filter(participant_id=participant_id).delete()
            return Response({'message': 'Participant deleted successfully'}, status=200)
        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@api_view(['PUT'])
@is_admin
def update_participant(request):
    try:
        if request.method == 'PUT':
            participant_id = request.GET.get('participant_id')
            participant_name = request.GET.get('participant_name')
            participant_email = request.GET.get('participant_email')
            participant_phone = request.GET.get('participant_phone')
            participant_dateOfBirth = request.GET.get('participant_dateOfBirth')
            participant_skills = request.GET.get('participant_skills')
            participant_linkedin = request.GET.get('participant_linkedin')
            participant_github = request.GET.get('participant_github')
            participant_portfolio = request.GET.get('participant_portfolio')
            participant_haveParticipated = request.GET.get('participant_haveParticipated')
            participant_previousExperience = request.GET.get('participant_previousExperience')
            participant_status = request.GET.get('participant_status')
            participant_team = request.GET.get('participant_team')

            if not participant_id:
                return Response({'error': 'Missing participant_id'}, status=400)
            
            if participant_team: 
                team = get_object_or_404(Team, team_id=participant_team) 

            participant = get_object_or_404(Participant, participant_id=participant_id)
            participant.participant_name = participant_name
            participant.participant_email = participant_email
            participant.participant_phone = participant_phone
            participant.participant_dateOfBirth = participant_dateOfBirth
            participant.participant_skills = participant_skills
            participant.participant_linkedin = participant_linkedin
            participant.participant_github = participant_github
            participant.participant_portfolio = participant_portfolio
            participant.participant_haveParticipated = participant_haveParticipated
            participant.participant_previousExperience = participant_previousExperience
            participant.participant_status = participant_status
            participant.participant_team = team

            participant.save()
            participant = model_to_dict(participant)
            return Response({'participant': participant},status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)



@csrf_exempt
@api_view(['POST'])
def add_team(request):
    try:
        if request.method == 'POST':
            team_name = request.POST.get('team_name')
            team_leader = request.POST.get('team_leader')
            
            if not team_name or not team_leader:
                return Response({'error': 'Missing required fields'}, status=400)

            if team_leader : 
                team_leader = get_object_or_404(Participant, participant_id=team_leader)

            team = Team(
                team_name=team_name,
                team_leader=team_leader
            )

            team.save()
            team = model_to_dict(team)
            return Response({'team': team}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@is_admin
def get_teams(request):
    try:
        if request.method == 'GET':
            teams = list(Team.objects.values())  
            return Response({'teams': teams})
        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@login_required
@api_view(['GET'])
@is_admin
def get_team_by_id(request):
    try:
        if request.method == 'GET':
            team_id = request.GET.get('team_id')
            if not team_id:
                return Response({'error': 'Missing team_id'}, status=400)

            team = get_object_or_404(Team, team_id=team_id)
            team = model_to_dict(team)
            return Response({'team': team})

        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@login_required
@api_view(['GET'])
@is_admin
def get_teams_by_name(request):
    try:
        if request.method == 'GET':
            team_name = request.GET.get('team_name')
            if not team_name:
                return Response({'error': 'Missing team_name'}, status=400)
            team = get_object_or_404(Team, team_name=team_name)
            team = model_to_dict(team)
            return Response({'team': team})

        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@csrf_exempt
@api_view(['DELETE'])
@is_admin
def delete_team(request):
    try:
        if request.method == 'DELETE': 
            team_id = request.GET.get('team_id')
            Team.objects.filter(team_id=team_id).delete()
            return Response({'message': 'Team deleted successfully'}, status=200)
        return Response({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['PUT'])
@is_admin
def update_team(request):
    try:
        if request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            team_id = data.get('team_id')
            team_name = data.get('team_name')
            team_leader = data.get('team_leader')
            team_project_name = data.get('team_project_name')
            team_project_description = data.get('team_project_description')
            team_project_links = data.get('team_project_links')

            if not team_id:
                return Response({'error': 'Missing team_id'}, status=400)
            
            if team_leader :
                team_leader = get_object_or_404(Participant, participant_id=team_leader)


            team = get_object_or_404(Team, team_id=team_id)
            team.team_name = team_name
            team.team_leader = team_leader
            team.team_project_name = team_project_name
            team.team_project_description = team_project_description
            team.team_project_links = team_project_links

            team.save()
            team = model_to_dict(team)
            return Response({'team': team},status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@csrf_exempt
@api_view(['POST'])
def login(request):
    try:
        if request.method == 'POST':
            email = request.data.get('admin_email') 
            password = request.data.get('admin_password')

            if not email or not password:
                return Response({'error': 'Missing required fields'}, status=400)
            
            admin = get_object_or_404(Admin, email=email)

            if not admin.check_password(password): 
                return Response({'error': 'Invalid password'}, status=401)

            refresh = RefreshToken.for_user(admin)
            response = JsonResponse({
                "user": model_to_dict(admin),
            })
            response.set_cookie(
                key='CyberShieldToken',
                value=str(refresh.access_token),
                httponly=True,
                max_age=timedelta(days=1),
                samesite='None',
                path='/',
                secure=True,
            )
            # print(response.cookies)

            return response
                    

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
@is_admin
def check_admin_auth(req):
    try:
        if req.method == 'GET':
            token = req.COOKIES.get('CyberShieldToken')

            if not token:
                return Response({'error': 'You are not authorized to access this page'}, status=403)
            access_token_obj = AccessToken(token)
            now = datetime.now().timestamp()
            if access_token_obj['exp']< now:
                return Response({'error': 'You are not authorized to access this page'}, status=403)
            admin = Admin.objects.get(id=access_token_obj['user_id'])
            if not admin:
                return Response({'error': 'You are not authorized to access this page'}, status=403)
            return Response({'message': 'You are authorized to access this page' , "authentication": True}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
