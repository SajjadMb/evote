from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.views.generic.base import TemplateView


def ContactUsView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "pages/contactus.html", {'form': form})


class successView(TemplateView):
    template_name = 'pages/Success_contact.html'


class AboutUs(TemplateView):
    template_name = 'pages/about.html'


class FAQ(TemplateView):
    template_name = 'pages/faq.html'


class HomePage(TemplateView):
    template_name='pages/homepage.html'

#def custom_404(request):
# return render(request, "pages/404.html", {}, status=404)