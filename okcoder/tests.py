from django.test import TestCase

# Create your tests here.
from .models import Partner, Evaluation
from django.core.urlresolvers import reverse
from django.utils import timezone

class BriefingViewTests(TestCase):
    def test_no_briefing(self):
        """
        If the partners were selected for no briefing, the page should
        say 'All right, let's go!'
        """
        response = self.client.get(reverse('okcoder:results', args=(0,)))
        self.assertContains(response, "All right, let's go!")

    def test_min_briefing(self):
        """
        If the partners were selected for minimal briefing, the page should
        say 'Minimal briefing'
        """
        response = self.client.get(reverse('okcoder:results', args=(1,)))
        self.assertContains(response, "Minimal briefing")

    def test_full_briefing(self):
        """
        If the partners were selected for full briefing, the page should
        say 'Full briefing'
        """
        response = self.client.get(reverse('okcoder:results', args=(2,)))
        self.assertContains(response, "Full briefing")

class EvaluationTests(TestCase):
    def test_full_evaluation(self):
        p1 = Partner(name='p1',reg_date=timezone.now(),consent=True)
        p2 = Partner(name='p2',reg_date=timezone.now(),consent=True)
        e = Evaluation.objects.create_evaluation({
                'name':p1.name,'partner':p2.name,'level':'12',
                    })
