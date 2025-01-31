from django.conf.urls import url
from apps.hamraz.views import (
    HamrazIndex,
    HamrazQaIndex,
    HamrazSubmit,
    HamrazFaqSingle,
    HamrazConversationSingle,
    QuestionStatus,
    QuestionScore,
    HamrazQuestionCategories,
    # HamrazQaSingle,

    QuestionManagerIndex,
    PickQuestion,
    ConfirmQuestion,
    GetQuestion,
    Workspace,
    WorkspaceFaq,
    WorkspaceStatistics,
    AnswerQuestion,
    RejectQuestion,
    RecordsQuestion,
    Question,
    CommentQuestion,
    FaqManagerQuestion,
    AcceptFaqQuestion,
    RemoveFaqQuestion,
)

urlpatterns = [
    url(r'^faq/$', HamrazIndex.as_view(), name='hamraz_faq_index'),
    url(r'^questions/$', HamrazQaIndex.as_view(), name='hamraz_qa_index'),
    url(r'^faq/(?P<faq_id>[\w\d-]+)$', HamrazFaqSingle.as_view(), name='hamraz_faq_single'),
    # url(r'^question/(?P<question_id>[0-9]+)$', HamrazQaSingle.as_view(), name='hamraz_qa_single'),
    url(r'^question/status/', QuestionStatus.as_view(), name='question_status'),
    url(r'^question/score/', QuestionScore.as_view(), name='question_score'),
    url(r'^questions/category/(?P<category_id>[\w\d-]+)$', HamrazQuestionCategories.as_view(), name='hamraz_qa_categories'),
    url(r'^submit/$', HamrazSubmit.as_view(), name='hamraz_submit'),
    url(r'^conversation/(?P<conversation_id>[\w\d-]+)$', HamrazConversationSingle.as_view(), name='hamraz_conversation_single'),

    url(r'^question_manager_index/$', QuestionManagerIndex.as_view(), name='question_manager_index'),
    url(r'^pick_question/$', PickQuestion.as_view(), name='pick_question'),
    url(r'^confirm_question/$', ConfirmQuestion.as_view(), name='confirm_question'),
    url(r'^get_question/$', GetQuestion.as_view(), name='get_question'),
    url(r'^workspace_question/$', Workspace.as_view(), name='workspace_question'),
    url(r'^workspace_faq/$', WorkspaceFaq.as_view(), name='workspace_faq'),
    url(r'^workspace_statistics/$', WorkspaceStatistics.as_view(), name='workspace_statistics'),
    url(r'^answer_question/(?P<question_id>[\w\d-]+)$', AnswerQuestion.as_view(), name='answer_question'),
    url(r'^reject_question/$', RejectQuestion.as_view(), name='reject_question'),
    url(r'^records_question/$', RecordsQuestion.as_view(), name='records_question'),
    url(r'^question/(?P<question_id>[\w\d-]+)$', Question.as_view(), name='one_question'),
    url(r'^comment_manager_question/$', CommentQuestion.as_view(), name='comment_manager_question'),
    url(r'^faq_manager_question/$', FaqManagerQuestion.as_view(), name='faq_manager_question'),
    url(r'^accept_faq_question/$', AcceptFaqQuestion.as_view(), name='accept_faq_question'),
    url(r'^remove_faq_question/$', RemoveFaqQuestion.as_view(), name='remove_faq_question'),
]
