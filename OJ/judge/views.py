from django.shortcuts import get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse
from judge.models import Problem,Solution,TestCase
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import ExtendedUser
from pathlib import Path
from django.conf import settings
import uuid
import subprocess

# Create your views here.
def parse(solvedProblems):
    solvedProblems = str(solvedProblems)
    solvedProblemIds = solvedProblems.split(',')
    solvedProblemList = []
    for id in solvedProblemIds:
        if id == '':
            break
        problem = Problem.objects.get(id=id)
        solvedProblemList.append(problem)
    return solvedProblemList

def displayProblemList(request):
    temp = loader.get_template('list.html')
    problems = Problem.objects.all()
    context = {
        'problems' : problems,
    }
    return HttpResponse(temp.render(context,request))

def displayProfile(request, id):
    user = get_object_or_404(User,id=id)
    customUser = ExtendedUser.objects.get(user=user)
    solvedProblemList = parse(customUser.solvedProblems)
    solutionsByUser = Solution.objects.filter(user=user)
    totProblems = Problem.objects.count()
    percent = len(solvedProblemList) / totProblems
    context = {
        'submissions': solutionsByUser,
        'name': user.username,
        'solved_problems': solvedProblemList,
        'percentage': (int(percent)) * 100,
        'id': user.id
    }
    temp = loader.get_template('profile.html')
    return HttpResponse(temp.render(context,request))

def run(language,code,pid,uid):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path,"wb") as code_file:
        for chunk in code.chunks():
            code_file.write(chunk)

    problem = get_object_or_404(Problem,id=pid)
    user = get_object_or_404(User,id=uid)
    extendeduser = get_object_or_404(ExtendedUser,user=user)
    tcs = TestCase.objects.filter(problem=problem)
    submission = Solution(user=user,problem=problem,code=code,tcspassed="")
    
    if language == "cpp":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(["g++", str(code_file_path), "-o", str(executable_path)])
        if compile_result.returncode == 0:
            failedtcs = 0
            for tc in tcs:
                with open(input_file_path, "w") as input_file:
                    input_file.write(tc.input)
                with open(output_file_path,"w") as output_file:
                    pass
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run([str(executable_path)],stdin=input_file,stdout=output_file,)
                with open(output_file_path,"r") as output_file:
                    expectedOutput = tc.output.splitlines()
                    actualOutput = output_file.read().splitlines()
                    if expectedOutput == actualOutput:
                        if submission.tcspassed == "":
                            submission.tcspassed += f'{tc.id}'
                        else:
                            submission.tcspassed += f',{tc.id}'
                    else:
                        failedtcs += 1
            if failedtcs:
                submission.verdict = 'Rejected'
            else:
                submission.verdict = 'Accepted'
                if str(problem.id) not in extendeduser.solvedProblems.split(','):
                    if extendeduser.solvedProblems == '':
                        extendeduser.solvedProblems += str(problem.id)
                    else:
                        extendeduser.solvedProblems += f',{problem.id}'
        else:
            submission.compilationError = True
            submission.verdict = 'Rejected'

    elif language == "c":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(["gcc", str(code_file_path), "-o", str(executable_path)])
        if compile_result.returncode == 0:
            failedtcs = 0
            for tc in tcs:
                with open(input_file_path, "w") as input_file:
                    input_file.write(tc.input)
                with open(output_file_path,"w") as output_file:
                    pass
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run([str(executable_path)],stdin=input_file,stdout=output_file,)
                with open(output_file_path,"r") as output_file:
                    expectedOutput = tc.output.splitlines()
                    actualOutput = output_file.read().splitlines()
                    if expectedOutput == actualOutput:
                        if submission.tcspassed == "":
                            submission.tcspassed += f'{tc.id}'
                        else:
                            submission.tcspassed += f',{tc.id}'
                    else:
                        failedtcs += 1
            if failedtcs:
                submission.verdict = 'Rejected'
            else:
                submission.verdict = 'Accepted'
                if str(problem.id) not in extendeduser.solvedProblems.split(','):
                    if extendeduser.solvedProblems == '':
                        extendeduser.solvedProblems += str(problem.id)
                    else:
                        extendeduser.solvedProblems += f',{problem.id}'
        else:
            submission.compilationError = True
            submission.verdict = 'Rejected'
    else:
        failedtcs = 0
        for tc in tcs:
            with open(input_file_path, "w") as input_file:
                    input_file.write(tc.input)
            with open(output_file_path,"w") as output_file:
                    pass
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(["python3", str(code_file_path)],stdin=input_file,stdout=output_file,)
            with open(output_file_path,"r") as output_file:
                expectedOutput = tc.output.splitlines()
                actualOutput = output_file.read().splitlines()
                if expectedOutput == actualOutput:
                    if submission.tcspassed == "":
                        submission.tcspassed += f'{tc.id}'
                    else:
                        submission.tcspassed += f',{tc.id}'
                else:
                    failedtcs += 1    
        if failedtcs:
            submission.verdict = 'Rejected'
        else:
            submission.verdict = 'Accepted'
            if str(problem.id) not in extendeduser.solvedProblems.split(','):
                if extendeduser.solvedProblems == '':
                    extendeduser.solvedProblems += str(problem.id)
                else:
                    extendeduser.solvedProblems += f',{problem.id}' 

    submission.save()
    extendeduser.save()
    return submission.id

def displayProblem(request,id):
    if request.method == 'GET':
        problem = get_object_or_404(Problem,id=id)
        context = {
            'problem': problem,
            'user': request.user
        }
        temp = loader.get_template('problem.html')
        return HttpResponse(temp.render(context,request))
    else:
        language = request.POST.get('language')
        code = request.FILES.get('code')
        sid = run(language,code,id,request.user.id)
        return redirect(f'/submissions/{sid}/')

def displaySubmission(request,sid):
    submission = get_object_or_404(Solution,id=sid)
    problem = submission.problem
    tcs = TestCase.objects.filter(problem=problem)
    passedTcList = []
    for id in submission.tcspassed.split(','): 
        if id == '':
            break
        else:
            passedTcList.append(get_object_or_404(TestCase,id=int(id)))
    with submission.code.open('rb') as f:
        text = f.read().decode('utf-8')
    passedTcList = set(passedTcList)
    context = {
        'tcs':tcs,
        'user': submission.user,
        'list':passedTcList,
        'text':text,
        'problem':submission.problem,
        'compilationError':submission.compilationError
    }
    temp = loader.get_template('submission.html')
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