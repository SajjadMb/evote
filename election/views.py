from .forms import ElectionForm, CandidateFormSet, NationalCodeForm
from .models import Election, Candidate, Voter,Vote
from evote import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.views.generic.base import TemplateView
import numpy as np
from account.models import ElectionUser


def newelectionView(request):
    username = None
    photo = None
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {}
            user = ElectionUser.objects.get(email=request.user.email)
            context['image'] = user.profile_photo
            context['fullname'] = user.full_name
            context['job'] = user.job
            form =ElectionForm()
            formset = CandidateFormSet()
            context['form'] = form
            context['formset'] = formset
            return render(request, "election/new_election_panel.html",context)

        else:
            context = {}
            user = ElectionUser.objects.get(email=request.user.email)
            context['image'] = user.profile_photo
            context['fullname'] = user.full_name
            context['job'] = user.job
            form = ElectionForm(request.POST,request.FILES)
            formset = CandidateFormSet(request.POST,request.FILES)
            context['formset'] = formset
            context['form'] = form
            if form.is_valid() & formset.is_valid():
                    # save election
                    elector = request.user
                    election_name = form.cleaned_data['election_name']
                    start_time = form.cleaned_data['start_date']
                    end_time = form.cleaned_data['end_date']
                    description = form.cleaned_data['election_des']
                    election_url =get_random_string(length=32)
                    election = Election(elector=elector,
                                        election_name=election_name,
                                        start_time=start_time,
                                        end_time=end_time,
                                        description=description,
                                        election_url=election_url)
                    election.save()

                    #save candidate
                    for form in formset:
                        firstname = form.cleaned_data['candidate_firstName']
                        lastname = form.cleaned_data['candidate_lastName']
                        email = form.cleaned_data['candidate_email']
                        des=form.cleaned_data['candidate_description']
                        pic=form.cleaned_data['candidate_photo']
                        f_election= election
                        c = Candidate(firstname=firstname,lastname=lastname,email=email,description=des,profile_photo=pic,f_election=f_election)
                        c.save()

                    #save voter
                    csv_file = request.FILES['election_voter']
                    file_data = csv_file.read().decode("utf-8")
                    lines = file_data.split('\n')
                    for line in lines:
                        fields = line.split(',')
                        if len(fields)==2:
                            email=fields[0]
                            national_code=fields[1]
                            f_election= election
                            v=Voter(email=email,national_code=national_code,f_election=f_election)
                            v.save()

                    #
                    subject = 'در انتخاب برگزیده ترین ها سهیم شوید'
                    message = 'http://127.0.0.1:8000/election/' + election_url+'/check_national_code'
                    from_email = settings.EMAIL_HOST_USER
                    to_list =Voter.objects.filter(f_election= election).values('email')
                    mylist=[]
                    for l in to_list:
                        mylist.append(l['email'])
                    send_mail(subject, message, from_email,mylist, fail_silently=True)

                    return redirect('electionpro:election_result')
            return render(request, "election/new_election_panel.html", context)
    else:
        return redirect('settings.LOGIN_URL')



def checkNationalCode(request, election_url=None):

        if request.method == 'GET':
            form = NationalCodeForm()
            return render(request, "election/vote_nationalcode.html", {'form': form})

        elif request.method == 'POST':
            form = NationalCodeForm(request.POST)
            if form.is_valid():
                election = Election.objects.get(election_url = election_url)
                if election:
                    voters = Voter.objects.filter(f_election=election.id)
                    national_number = form.cleaned_data['national_code']
                    for voter in voters:
                        if voter.national_code == national_number:
                            return redirect("election:submit_vote",election_url=election_url,national_number=national_number)

        return render(request, "election/vote_nationalcode.html", {'form': form, 'wrong_form':True})


def submitVote(request,election_url,national_number):
    if request.method == 'GET':
        election = Election.objects.get(election_url=election_url)
        candidate=Candidate.objects.filter(f_election=election)
        context={
            'obj':candidate,
        }
        return render(request, "election/vote_page.html",context)
    elif request.POST:
            choice_list=request.POST.getlist('candidate')
            choice=[]
            for l in choice_list:
                choice.append(l)
            voter=Voter.objects.get(national_code=national_number)
            v = Vote(f_voter=voter,choice=choice)
            v.save()
            return redirect("election:votedone")

class Votedone(TemplateView):
    template_name = 'election/Vote_Done.html'
