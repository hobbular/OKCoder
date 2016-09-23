from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your models here.

class PartnerManager(models.Manager):
    def create_partner(self, name, consent):
        p = self.create(
            name=name, reg_date=timezone.now(), consent=consent
            )
        return p

class Partner(models.Model):
    """
    Every individual who participates in the study gets to be a Partner.
    Tracks whether they've consented to the study and whether they've
    completed their post-study evaluation.
    """
    name = models.CharField(max_length=200)
    reg_date = models.DateTimeField('date registered')
    consent = models.BooleanField(default=False)
    eval_complete = models.BooleanField(default=False)

    objects = PartnerManager()

    def __str__(self):
        return self.name

class PartnershipManager(models.Manager):
    def create_partnership(self, name, p1, p2, b):
        ps = self.create(
            name=name, p1=p1, p2=p2, brief=b
            )
        return ps

class Partnership(models.Model):
    """
    Relates two partners to each other, carries all common characteristics
    (currently only the briefing status)
    """
    # setting related_name on p2 so that Django stops bitching about clashes
    # related_name = '+' means it doesn't try to generate another lookup
    p1 = models.ForeignKey(Partner, on_delete=models.CASCADE)
    p2 = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=200)
    brief = models.IntegerField(default=-1)
    complete = models.BooleanField(default=False)

    objects = PartnershipManager()

    def __str__(self):
        return self.name

class LevelLogManager(models.Manager):
    def create_levellog(self, p, num):
        log = self.create(
            partnership = get_object_or_404(Partnership, name=p),
            level = int(num),
            timestamp = timezone.now()
            )
        return log

class LevelLog(models.Model):
    """
    For logging when various levels are completed by a partnership
    """
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE)
    timestamp = models.DateTimeField('timestamp')
    level = models.IntegerField(default=0)

    objects = LevelLogManager()

    def __str__(self):
        return self.partnership.name+" ("+str(self.level)+"), "+str(self.timestamp)

class RunLogManager(models.Manager):
    def create_runlog(self, p, status, code):
        log = self.create(
            partnership = get_object_or_404(Partnership, name=p),
            status = int(status),
            code = code,
            timestamp = timezone.now()
            )
        return log

class RunLog(models.Model):
    """
    For logging more than just level completion, because this is a Real Program
    """
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE)
    timestamp = models.DateTimeField('timestamp')
    status = models.IntegerField(default=0)
    code = models.TextField()

    objects = RunLogManager()

    def __str__(self):
        return self.partnership.name+" ["+str(self.status)+"] "+str(self.timestamp)

class EvaluationManager(models.Manager):
    def create_evaluation(self, form):
        """
        form should be populated using results.POST
        """
        eval = self.create(
            evaluator = get_object_or_404(Partner, name=form['name']),
            partner = get_object_or_404(Partner, name=form['partner']),
            level = int(form['level']),
            overall = int(form['overall']),
            learned = int(form['learned']),
            workload = int(form['workload']),
            again = int(form['again']),
            comments = form['comments']
            )
        return eval

class Evaluation(models.Model):
    """
    Contains the post-study evaluation information. Currently allowing
    a deleted partner's eval to remain as long as the evaluator is not
    removed.
    """
    evaluator = models.ForeignKey(Partner, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, related_name='+')
    level = models.IntegerField(default=0)
    overall = models.IntegerField()
    learned = models.IntegerField()
    workload = models.IntegerField()
    again = models.IntegerField()
    comments = models.CharField(max_length=500)

    objects = EvaluationManager()

    def __str__(self):
        return self.evaluator.name

