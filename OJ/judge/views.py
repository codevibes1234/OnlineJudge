from django.shortcuts import get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse
from judge.models import Problem,Solution
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import ExtendedUser

# Create your views here.
def parse(solvedProblems):
    solvedProblems = str(solvedProblems)
    solvedProblemIds = solvedProblems.split(',')
    print(solvedProblemIds)
    solvedProblemList = []
    for id in solvedProblemIds:
        if id == '':
            break
        problem = Problem.objects.filter(id=id)
        solvedProblemList.append(problem)
    return solvedProblemList

def displayProblemList(request):
    temp = loader.get_template('list.html')
    problems = Problem.objects.all()
    context = {
        'problems' : problems,
    }
    return HttpResponse(temp.render(context,request))

@login_required
def displayProfile(request, id):
    user = get_object_or_404(User,id=id)
    if request.user == user:
        customUser = ExtendedUser.objects.get(user=user)
        solvedProblemList = parse(customUser.solvedProblems)
        solutionsByUser = Solution.objects.filter(user=user)
        totProblems = Problem.objects.count()
        percent = len(solvedProblemList) / totProblems
        context = {
            'submissions': solutionsByUser,
            'name': user.username,
            'solved_problems': solvedProblemList,
            'percentage': (int(percent)) * 100
        }
        temp = loader.get_template('profile.html')
        return HttpResponse(temp.render(context,request))
    else:
        messages.error(request,'You can\'t access this page')
        return redirect(f'/problems')
  
def displayProblem(request,id):
    problem = get_object_or_404(Problem,id=id)
    context = {
        'problem': problem,
        'user': request.user
    }
    temp = loader.get_template('problem.html')
    return HttpResponse(temp.render(context,request))

def displayAllSubmissions(request,id):
    problem = get_object_or_404(Problem,id=id)
    submissions = Solution.objects.filter(problem=problem)
    context = {
        'problem': problem,
        'submissions': submissions,
        'user': request.user
    }
    temp = loader.get_template('problem.html')
    return HttpResponse(temp.render(context,request))

@login_required
def displayMySubmissions(request,uid,pid):
    user = get_object_or_404(User,id=uid)
    if request.user == user:
        problem = get_object_or_404(Problem,id=pid)
        submissions = Solution.objects.filter(problem=problem,user=user)
        context = {
            'problem': problem,
            'submissions': submissions,
            'user': user
        }
        temp = loader.get_template('problem.html')
        return HttpResponse(temp.render(context,request))
    else:
        messages.error(request,'You can\'t access this page')
        return redirect('/problems')