from django.urls import path
import judge.views

urlpatterns = [
    path('problems/',judge.views.displayProblemList,name='problem-list'),
    path('user/<int:id>/',judge.views.displayProfile,name='profile'),
    path('problems/<int:id>/',judge.views.displayProblem,name='problem'),
    path('problems/<int:id>/submissions/',judge.views.displayAllSubmissions,name='All-Submissions'),
    path('problems/<int:pid>/submissions/user/<int:uid>/',judge.views.displayMySubmissions,name='My-Submissions'),
    path('submissions/<int:sid>/',judge.views.displaySubmission,name='Submission')
]