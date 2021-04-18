from django.shortcuts import render, redirect
from django.views import generic
from election.models import Election, Candidate, Voter, Vote
from django.core.exceptions import ObjectDoesNotExist
from account.models import ElectionUser
from .forms import profileForm
from . import urls, forms


class ElectionHistory(generic.ListView):

    model = Election
    context_object_name = 'election_list'
    queryset = Election.objects.all()[:10]
    template_name = 'profile/history_panel.html'


    def get_context_data(self, **kwargs):
        context = super(ElectionHistory, self).get_context_data(**kwargs)
        user = ElectionUser.objects.get(email=self.request.user.email)
        context['image'] = user.profile_photo
        context['fullname'] = user.full_name
        context['job'] = user.job
        return context


class ProfilePanel(generic.FormView):
    template_name = 'profile/profile_panel.html'
    success_url = "electionpro:election_result"

    def get(self, request, *args, **kwargs):
        form = profileForm()
        context = {}
        user = ElectionUser.objects.get(email=self.request.user.email)
        context['image'] = user.profile_photo
        context['fullname'] = user.full_name
        context['job'] = user.job
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        user = ElectionUser.objects.get(email=self.request.user.email)
        form = profileForm(request.POST, request.FILES)
        context['image'] = user.profile_photo
        context['fullname'] = user.full_name
        context['job'] = user.job
        context['form'] = form
        if form.is_valid():
            user = ElectionUser.objects.get(email=self.request.user.email)
            full_name = form.cleaned_data['user_fullname']
            job = form.cleaned_data['user_job']
            profile_photo = form.cleaned_data['user_photo']
            if full_name != '':
                user.full_name = full_name
            if job != '':
                user.job = job
            if profile_photo:
                user.profile_photo = profile_photo
            user.save()
            print(user)
            return redirect(self.success_url)
        return render(request, self.template_name, context)


class ElectionResult(generic.TemplateView):
    template_name = 'profile/election_result.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = ElectionUser.objects.get(email=self.request.user.email)
        election = Election.objects.get(election_url=self.kwargs['election_url'])
        election_url = self.kwargs['election_url']
        data1 = Candidate.objects.filter(f_election=election.id).values('firstname')
        candidate = []
        for d in data1:
            candidate.append(d['firstname'])

        id = []
        data1 = Candidate.objects.filter(f_election=election.id).values('id')
        for d in data1:
            id.append(d['id'])

        print(id)

        data2 = Voter.objects.filter(f_election=election.id)
        allvote = []
        for v in data2:
            vote1 = Vote.objects.filter(f_voter=v.id).values('choice')
            if len(vote1) == 1:
                for v1 in vote1:
                    allvote.append(v1['choice'])

        finalvote = []
        for i in allvote:
            for j in range(len(i)):
                finalvote.append(i[j])

        print(finalvote)
        sum = len(finalvote)
        result = []
        for i in id:
            count = 0
            for f in finalvote:
                if f == str(i):
                    count = count + 1
            result.append(count)

        print(result)
        context['election'] = election
        context['data'] = {'x': candidate, 'y': result}
        context['image'] = user.profile_photo
        context['fullname'] = user.full_name
        context['job'] = user.job
        context['sum'] = sum
        context['election_url'] = election_url
        return render(request, self.template_name, context)


class LastElectionResult(generic.TemplateView):
    template_name = 'profile/election_result.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user = ElectionUser.objects.get(email=self.request.user.email)
        data1 = data2 = []
        try:
            election = Election.objects.filter(elector=user.id).order_by('end_time')[0]
            election_url = "d@?2388dvn#@#%&867jfdhhdf"
            data1 = Candidate.objects.filter(f_election=election.id).values('firstname')
            candidate = []
            for d in data1:
                candidate.append(d['firstname'])

            id = []
            data1 = Candidate.objects.filter(f_election=election.id).values('id')
            for d in data1:
                id.append(d['id'])

            print(id)

            data2 = Voter.objects.filter(f_election=election.id)
            allvote = []
            for v in data2:
                vote1 = Vote.objects.filter(f_voter=v.id).values('choice')
                if len(vote1) == 1:
                    for v1 in vote1:
                        allvote.append(v1['choice'])

            finalvote = []
            for i in allvote:
                for j in range(len(i)):
                    finalvote.append(i[j])

            print(finalvote)
            sum = len(finalvote)
            print(sum)
            result = []
            for i in id:
                count = 0
                for f in finalvote:
                    if f == str(i):
                        count = count + 1
                result.append(count)

        except ObjectDoesNotExist:
            pass

        context['data'] = {'x': candidate, 'y': result}
        context['image'] = user.profile_photo
        print(context['image'])
        context['fullname'] = user.full_name
        context['job'] = user.job
        context['sum'] = sum
        context['election_url'] = election_url
        return render(request, self.template_name, context)
