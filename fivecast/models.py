import sys

from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=36, default="Some Schedule")

    def __str__(self):
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=36)

    def __str__(self):
        return self.name

# Create your models here.
class Feature(models.Model):
    #dependantFeatures = models.ManyToManyField(Feature, blank=True, null=True)
    assignedSprint = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=128)
    priority = models.IntegerField(default=sys.maxint)

    def asDict(self):
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority
        }

    def __str__(self):
        return self.description


class DisiplineWorkForFeature(models.Model):
    feature = models.ForeignKey(Feature)
    discipline = models.ForeignKey(Discipline)
    unique_together = ("feature", "discipline")
    sprints = models.IntegerField(default=0)

    def __str__(self):
        return '%s sprints for %s for %s' % (self.sprints, self.discipline, self.feature)


class Lane(models.Model):
    schedule = models.ForeignKey(Schedule)
    discipline = models.ForeignKey(Discipline)
    sprintStart = models.IntegerField(default=0)
    sprintEnd = models.IntegerField(default=sys.maxint)

    def asDict(self):
        return {
            "id": self.id,
            "discipline": self.discipline.__str__(),
        }

    def __str__(self):
        return '%s (%d)' % (self.discipline, self.id)


class WorkBooked(models.Model):
    lane = models.ForeignKey(Lane)
    schedule = models.ForeignKey(Schedule)
    feature = models.ForeignKey(Feature)
    sprint = models.IntegerField()
    unique_together = ("lane", "schedule", "sprint")

    def __str__(self):
        return '%s for sprint %d booked for %s' % (self.lane, self.sprint, self.feature.description)

    def asDict(self):
        return {
            "id": self.id,
            "lane": self.lane.asDict(),
            "feature": self.feature.asDict(),
            "sprint": self.sprint
        }

