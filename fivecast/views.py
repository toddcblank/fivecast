# Create your views here.

import json
import itertools
import sys

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from fivecast.models import Feature, Discipline, Lane, Schedule, DisiplineWorkForFeature, WorkBooked


def clearSchedule(schedule):
    allWorkBooked = WorkBooked.objects.filter(schedule=schedule)
    map(lambda x: x.delete(), allWorkBooked)


def bookWork(nextLane, feature, schedule):
    disciplineWork = DisiplineWorkForFeature.objects.filter(feature=feature, discipline=nextLane.discipline)

    if disciplineWork is not None and len(disciplineWork) > 0:
        sprintsToBook = disciplineWork[0].sprints
        for _ in itertools.repeat(None, sprintsToBook):
            nextAvailableSprint = getNextAvailableSprintForLane(nextLane, schedule)
            work = WorkBooked(lane=nextLane, schedule=schedule, sprint=nextAvailableSprint, feature=feature)
            work.save()


def getNextAvailableSprintForLane(lane, schedule):
    nextAvailableSprints = WorkBooked.objects.filter(lane=lane, schedule=schedule).order_by('sprint').reverse()

    if len(nextAvailableSprints) == 0:
        return 1

    return nextAvailableSprints[0].sprint + 1


def findNextAvailableLane(swimLanesForDiscipline, schedule):
    bestLane = None
    bestAvailableSprint = sys.maxint
    for lane in swimLanesForDiscipline:
        nextAvailableSprint = getNextAvailableSprintForLane(lane, schedule)
        if nextAvailableSprint < bestAvailableSprint:
            bestAvailableSprint = nextAvailableSprint
            bestLane = lane

    return bestLane


def rescheduleWork(request, scheduleId):
    allFeatures = Feature.objects.all().exclude(priority=0)

    priorityList = sorted(allFeatures, key=lambda x: x.priority)
    allDisciplines = Discipline.objects.all()
    schedule = Schedule.objects.get(id=scheduleId)
    clearSchedule(schedule)

    for feature in priorityList:

        for discipline in allDisciplines:
            swimLanesForDiscipline = Lane.objects.filter(discipline=discipline, schedule=schedule)

            nextLane = findNextAvailableLane(swimLanesForDiscipline, schedule)

            bookWork(nextLane, feature, schedule)

    return redirect("/%s" % scheduleId)


def showSchedule(request, scheduleId):
    schedule = Schedule.objects.get(id=scheduleId)

    lanes = Lane.objects.filter(schedule=schedule)

    workByLanes = []
    for lane in lanes:
        laneWork = WorkBooked.objects.filter(schedule=schedule, lane=lane)
        sortedLaneWork = sorted(laneWork, key=lambda x: x.sprint)
        workByLanes.append(sortedLaneWork)

    model = {"workByLanes": workByLanes}

    return render(request, "schedule.html", model)


def showScheduleJson(request, scheduleId):
    schedule = Schedule.objects.get(id=scheduleId)
    workSchedule = WorkBooked.objects.filter(schedule=schedule)

    workDict = {x.id: x.asDict() for x in workSchedule}

    return HttpResponse(json.dumps(workDict),
                        content_type="application/json")


def createNewSchedule(scheduleId):
    pass


def addDisciplineLaneToSchedule(scheduleId, discipline):
    pass