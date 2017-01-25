from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Partner, Partnership, Evaluation, LevelLog, RunLog, CompletionCode
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
            {'error_message': "Both partners must select a consent option!",
             'id1': user1, 'id2': user2}
            )
    else:
        b = random.randint(0,2)
        n = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        p1 = Partner.objects.create_partner(user1, c1)
        p2 = Partner.objects.create_partner(user2, c2)
        p1.save()
        p2.save()
        ps = Partnership.objects.create_partnership(n,p1,p2,b)
        ps.save()
        return HttpResponseRedirect(reverse('okcoder:results', args=(b,ps)))

def results(request, b, ps):
    args = {'ps': ps}
    # briefing status
    b = int(b)
    if b == 0:
        args['no_brief'] = 'hi'
    elif b == 1:
        args['min'] = b
    elif b == 2:
        args['full'] = b
    return render(request, 'okcoder/results.html', args)

def play(request, ps):
    ps = get_object_or_404(Partnership, name=ps)
    level = request.GET.get('level','1')
    log = LevelLog.objects.create_levellog(ps.name, level)
    log.save()
    return render(request, 'okcoder/play.html', {'ps':ps})

def log(request):
    """ This is for logging actions within the blockly-game interface.
        It is called by jQuery code in maze.js every time the user pushes
        the Run button, so we can see how they're doing.
    """
    try:
        code = request.POST['usercode']
        status = request.POST['status']
        ps = get_object_or_404(Partnership, name=request.POST['ps'])
        runlog = RunLog.objects.create_runlog(ps.name, status, code)
        runlog.save()
    except KeyError:
        return HttpResponse('y')
    else:
        return HttpResponse('x')

def eval(request, ps):
    ps = get_object_or_404(Partnership, name=ps)
    logs = LevelLog.objects.filter(partnership=ps).order_by('level')
    if logs[0].level > 0:
        # we haven't done a completion log yet so let's do that
        log = LevelLog.objects.create_levellog(ps.name, 0)
        log.save()
    if not ps.p1.eval_complete:
        p1 = ps.p1
        p2 = ps.p2
    elif not ps.p2.eval_complete:
        p1 = ps.p2
        p2 = ps.p1
    else:
        # TODO: done evaluating, move along to thank you page
        return HttpResponseRedirect(reverse('okcoder:complete', args=(ps,)))
    return render(request, 'okcoder/eval.html', {'ps':ps, 'p1':p1, 'p2':p2, 'lev':logs[len(logs)-1].level})

def evaluate(request, ps):
    ps = get_object_or_404(Partnership, name=ps)
    logs = LevelLog.objects.filter(partnership=ps).order_by('level')
    try:
        eval = Evaluation.objects.create_evaluation(request.POST)
        eval.save()
        if not ps.p1.eval_complete and eval.evaluator.name == ps.p1.name:
            evaluator = ps.p1
        elif not ps.p2.eval_complete and eval.evaluator.name == ps.p2.name:
            evaluator = ps.p2
        evaluator.eval_complete = True
        evaluator.save()
    except:
        if not ps.p1.eval_complete:
            p1 = ps.p1
            p2 = ps.p2
        else:
            p1 = ps.p2
            p2 = ps.p1
        return render(request, 'okcoder/eval.html',
                      {
                'ps':ps, 'p1':p1, 'p2':p2,
                'lev':logs[len(logs)-1].level,
                'error_message': "Something went wrong, please try again!"
                })
    return HttpResponseRedirect(reverse('okcoder:eval', args=(ps,)))

def complete(request, ps):
    n = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    code = CompletionCode.objects.create_code(n)
    code.save()
    ps = get_object_or_404(Partnership, name=ps)
    ps.complete = True
    ps.save()
    return render(request, 'okcoder/complete.html', args=n)
