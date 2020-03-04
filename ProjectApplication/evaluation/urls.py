from django.urls import path

import evaluation.views

urlpatterns = [
    path('logged/proposal-evaluation/<int:id>/',
         evaluation.views.ProposalEvaluationDetail.as_view(),
         name='logged-proposal-evaluation-detail'),
    path('logged/proposal-evaluation/<int:id>/evaluation/',
         evaluation.views.ProposalEvaluationUpdate.as_view(),
         name='logged-proposal-evaluation-update'),
    path('logged/proposal-evaluation/add/',
         evaluation.views.ProposalEvaluationUpdate.as_view(),
         name='logged-proposal-evaluation-add'),
    path('logged/proposal-evaluation/<int:id>/comment/add/',
         evaluation.views.ProposalCommentAdd.as_view(),
         name='logged-proposal-evaluation-comment-add'),
    path('logged/evaluation/list/',
         evaluation.views.ProposalEvaluationList.as_view(),
         name='logged-evaluation-list'),
    path('logged/call-evaluation/add/',
         evaluation.views.CallEvaluationUpdate.as_view(),
         name='logged-call-evaluation-add'),
    path('logged/call-evaluation/<int:id>/update/',
         evaluation.views.CallEvaluationUpdate.as_view(),
         name='logged-call-evaluation-update'),
    path('logged/call-evaluation/<int:id>/',
         evaluation.views.CallEvaluationDetail.as_view(),
         name='logged-call-evaluation-detail'),
]
