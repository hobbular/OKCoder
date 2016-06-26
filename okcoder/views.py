from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Partner
import random, string

# Create your views here.

def index(request):
    return render(request, 'okcoder/index.html')

def init(request):
    args = {}
    a = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    b = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    args['id1'] = a
    args['id2'] = b
    return render(request, 'okcoder/init.html', args)

def create(request):
    user1, user2 = '', ''
    try:
        # create users for this session
        user1 = request.POST['name1']
        user2 = request.POST['name2']
        c1 = request.POST['consent1'] == "True"
        c2 = request.POST['consent2'] == "True"
    except KeyError:
        return render(
            request, 'okcoder/init.html', 
            {'error_message': "Please answer all questions!",
             'id1': user1, 'id2': user2}
            )
    else:
        b = random.randint(0,2)
        p1 = Partner.objects.create_partner(user1, c1, b)
        p2 = Partner.objects.create_partner(user2, c2, b)
        p1.save()
        p2.save()
        return HttpResponseRedirect(reverse('okcoder:results', args=(b,p1,p2)))

def results(request, b, p1, p2):
    args = {'p1': p1, 'p2': p2}
    # briefing status
    b = int(b)
    if b == 0:
        args['no_brief'] = 'hi'
    elif b == 1:
        args['min'] = b
    elif b == 2:
        args['full'] = b
    return render(request, 'okcoder/results.html', args)

def play(request, p1, p2):
    args = {'p1':p1,'p2':p2}
    return render(request, 'okcoder/play.html', args)
