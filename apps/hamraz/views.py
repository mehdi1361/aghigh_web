from django.shortcuts import render, redirect
from django.urls import reverse

from apps.main.views import BaseViewClass
from django.conf import settings
import requests
from django.http import JsonResponse, HttpResponseNotFound


class HamrazIndex(BaseViewClass):
    def get(self, request):

        params = {}
        query_params = {}

        qa_point = request.GET.get('faq_point', None)
        qa_sort = request.GET.get('faq_sort', None)
        qa_order = request.GET.get('faq_order', None)
        qa_category = request.GET.get('faq_category', None)
        qa_sub_category = request.GET.get('faq_sub_category', None)

        if qa_point:
            point_data = qa_point.split(',')
            params['point_start'] = int(float(point_data[0]))
            params['point_end'] = int(float(point_data[1]))

        params['sort'] = qa_sort
        params['order'] = qa_order
        params['category'] = qa_category
        params['sub_category'] = qa_sub_category

        for key in params:
            if params[key] is not None and params[key] is not '':
                query_params[key] = params[key]

        base_categories_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_category/',
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, base_categories_res)

        faq_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/faq_questions/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, params)
        )
        self.is_auth_valid(request, faq_res)

        try:
            faq_res = faq_res.json()
        except:
            faq_res = []

        pagination_data = self.return_pagination(response=faq_res, page=request.GET.get('page', 1))

        context = {
            'faq_questions': faq_res,
            'categories': base_categories_res.json(),
            'pagination_data': pagination_data,
            'query_params': query_params
        }

        return render(request=request, context=context, template_name='apps/hamraz/faq_questions.html')


class HamrazQaIndex(BaseViewClass):

    def get(self, request):

        params = {}
        query_params = {}

        order = request.GET.get('order', None)
        category = request.GET.get('category', None)
        sub_category = request.GET.get('sub_category', None)

        params['order'] = order
        params['category'] = category
        params['sub_category'] = sub_category

        for key in params:
            if params[key] is not None and params[key] is not '':
                query_params[key] = params[key]

        base_categories_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_category/',
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, base_categories_res)

        que_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, params)
        )
        self.is_auth_valid(request, que_res)

        try:
            que_res = que_res.json()
        except:
            que_res = []

        pagination_data = self.return_pagination(response=que_res, page=request.GET.get('page', 1))

        context = {
            'my_questions': que_res,
            'categories': base_categories_res.json(),
            'pagination_data': pagination_data,
            'query_params': query_params
        }

        return render(request=request, context=context, template_name='apps/hamraz/qa_index.html')


class HamrazFaqSingle(BaseViewClass):
    def get(self, request, faq_id):
        faq_id = self.decode_id(faq_id)
        if not faq_id:
            return HttpResponseNotFound()

        faq_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/faq_questions/' + str(faq_id),
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, faq_res)

        context = {
            'faq_question': faq_res.json(),
        }

        return render(request=request, context=context, template_name='apps/hamraz/faq_single.html')


class QuestionStatus(BaseViewClass):
    def post(self, request):
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        point = request.POST.get('point', 0)
        status = request.POST.get('status', False)
        context = {
            'status': 404,
        }
        post_data = {
            "point": point
        }
        if question_id and status in ['solved', 'not_solved', 'disinterested']:
            qa_res = requests.post(
                url=settings.SERVER_FULL_URL + '/api/v1/questions/' + str(question_id) + '/' + status + '/',
                headers=self.get_http_header(request),
                data=post_data
            )
            self.is_auth_valid(request, qa_res)

            context = {
                'status': qa_res.status_code
            }
        return JsonResponse(context)


class QuestionScore(BaseViewClass):
    def post(self, request):
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        point = request.POST.get('point', 0)
        post_data = {
            "point": point,
            "question_id": question_id,
        }
        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions/score/',
            headers=self.get_http_header(request),
            data=post_data
        )
        self.is_auth_valid(request, qa_res)

        context = {
            'status': qa_res.status_code
        }
        return JsonResponse(context)


class RejectQuestion(BaseViewClass):
    def post(self, request):
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/reject/',
            headers=self.get_http_header(request),
            data={"question_id": question_id}
        )
        self.is_auth_valid(request, qa_res)

        context = {
            'statue_code': qa_res.status_code
        }
        return JsonResponse(context)


class RecordsQuestion(BaseViewClass):
    def get(self, request):

        params = {}
        query_params = {}

        question_id = request.GET.get('question_id', None)
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        params['question_id'] = question_id

        que_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/records/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, params)
        )
        self.is_auth_valid(request, que_res)

        try:
            que_res = que_res.json()
        except:
            que_res = []

        pagination_data = self.return_pagination(response=que_res, page=request.GET.get('page', 1))

        context = {
            'questions': que_res,
            'pagination_data': pagination_data,
            'query_params': query_params
        }

        return render(request=request, context=context, template_name='apps/hamraz/manager/student_records.html')


class HamrazSubmit(BaseViewClass):
    def get_categories(self, request):
        base_categories_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_category/',
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, base_categories_res)

        return base_categories_res.json()

    def cleaned_data(self, request):
        post_req = {
            'subject': request.POST.get('subject', ''),
            'body': request.POST.get('question_body', ''),
            'sub_category': request.POST.get('sub_category'),
            'category': request.POST.get('category'),
        }

        post_files = []
        for file_item in request.FILES.getlist('files[]'):
            post_files.append(
                ('files[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )

        return post_files, post_req

    def get(self, request):
        context = {
            'categories': self.get_categories(request),
        }

        return render(
            request=request,
            context=context,
            template_name='apps/hamraz/submit.html'
        )

    def post(self, request):
        post_files, post_req = self.cleaned_data(request)

        que_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions/',
            headers=self.get_http_header(request),
            data=post_req,
            files=post_files,
        )
        self.is_auth_valid(request, que_res)

        if que_res.status_code == 201:
            return redirect(reverse("hamraz_qa_index"))

        context = {
            'categories': self.get_categories(request),
        }

        return render(
            request=request,
            context=context,
            template_name='apps/hamraz/submit.html'
        )


class HamrazConversationSingle(BaseViewClass):
    def get(self, request, conversation_id):
        conversation_id = self.decode_id(conversation_id)
        if not conversation_id:
            return HttpResponseNotFound()

        que_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions/' + str(conversation_id),
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, que_res)

        context = {
            'question': que_res.json(),
            'point_range': range(0, 21),
        }

        return render(
            context=context,
            request=request,
            template_name='apps/hamraz/conversation_single.html'
        )

    def cleaned_data(self, request):
        post_req = {
            'body': request.POST.get('question_body', ''),
        }

        post_files = []
        for file_item in request.FILES.getlist('files[]'):
            post_files.append(
                ('files[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )

        return post_files, post_req

    def post(self, request, conversation_id):
        post_files, post_req = self.cleaned_data(request)
        conversation_id = self.decode_id(conversation_id)
        if not conversation_id:
            return HttpResponseNotFound()

        post_req['conversation_id'] = conversation_id

        que_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions/',
            headers=self.get_http_header(request),
            data=post_req,
            files=post_files,
        )
        self.is_auth_valid(request, que_res)

        questions_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions/' + str(post_req['conversation_id']),
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, que_res)

        context = {
            'question': questions_res.json(),
            'response': que_res.json(),
            'response_code': que_res.status_code,
            'point_range': range(0, 21),
        }

        return render(
            context=context,
            request=request,
            template_name='apps/hamraz/conversation_single.html'
        )


class HamrazQuestionCategories(BaseViewClass):
    def get(self, request, category_id):
        selected_category_id = int(category_id)

        if selected_category_id == 0:
            return []

        get_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_category/' + str(
                selected_category_id) + '/sub_categories/',
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)

        context = {
            'categories': get_res.json()
        }

        return JsonResponse(context)


class QuestionManagerIndex(BaseViewClass):
    def get(self, request):
        return render(
            context={},
            request=request,
            template_name='apps/hamraz/manager/question_manager_index.html'
        )


class PickQuestion(BaseViewClass):

    def get(self, request):
        role = request.user.userbox.role_select
        questions = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {'role': role}),
        )
        self.is_auth_valid(request, questions)

        try:
            questions = questions.json()
        except:
            questions = []

        pagination_data = self.return_pagination(response=questions, page=request.GET.get('page', 1))

        return render(
            context={
                'questions': questions,
                'role': role,
                'pagination_data': pagination_data,
            },
            request=request,
            template_name='apps/hamraz/manager/pick_question.html'
        )

    def post(self, request):
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        data = {
            'message': "error"
        }
        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/pick_question/',
            headers=self.get_http_header(request),
            json={
                "question_id": question_id,
            }
        )

        self.is_auth_valid(request, qa_res)
        if qa_res.status_code == 200:
            data["message"] = 'success'

        return JsonResponse(data)


class ConfirmQuestion(BaseViewClass):
    def get(self, request):
        base_categories_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_category/',
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, base_categories_res)

        try:
            categories = base_categories_res.json()
        except:
            categories = []

        questions = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {'role': "advisor"}),
        )
        self.is_auth_valid(request, questions)

        try:
            questions = questions.json()
        except:
            questions = []

        pagination_data = self.return_pagination(response=questions, page=request.GET.get('page', 1))

        return render(
            context={
                'categories': categories,
                'questions': questions,
                'pagination_data': pagination_data,
            },
            request=request,
            template_name='apps/hamraz/manager/confirm_question.html'
        )

    def post(self, request):
        data = {
            'message': "error"
        }
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/confirm/',
            headers=self.get_http_header(request),
            json={
                "question_id": question_id,
                "sub_category": request.POST.get('sub_category'),
                "category": request.POST.get('category'),
            }
        )
        self.is_auth_valid(request, qa_res)
        if qa_res.status_code == 200:
            data["message"] = 'success'

        return JsonResponse(data)


class CommentQuestion(BaseViewClass):
    def get(self, request):
        question_id = request.GET.get('question')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        comments = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_comment/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {'question_id': question_id}),
        )

        self.is_auth_valid(request, comments)

        try:
            comments = comments.json()
        except:
            comments = []

        pagination_data = self.return_pagination(response=comments, page=request.GET.get('page', 1))

        return render(
            context={
                'comments': comments,
                'pagination_data': pagination_data,
            },
            request=request,
            template_name='apps/hamraz/manager/comment_manager_question.html'
        )

    def post(self, request):
        data = {
            'message': "error"
        }
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id or not request.POST.get('body'):
            return HttpResponseNotFound()

        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_comment/',
            headers=self.get_http_header(request),
            data={
                "question": question_id,
                "body": request.POST.get('body'),
            }
        )

        self.is_auth_valid(request, qa_res)
        if qa_res.status_code == 201:
            data["message"] = 'success'

        return JsonResponse(data)


class FaqManagerQuestion(BaseViewClass):
    def get(self, request):
        base_categories_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_category/',
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, base_categories_res)

        faq_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/faq_questions/',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {})
        )
        self.is_auth_valid(request, faq_res)

        try:
            faq_res = faq_res.json()
        except:
            faq_res = []

        pagination_data = self.return_pagination(response=faq_res, page=request.GET.get('page', 1))

        context = {
            'faq_questions': faq_res,
            'categories': base_categories_res.json(),
            'pagination_data': pagination_data,
        }

        return render(request=request, context=context, template_name='apps/hamraz/manager/faq_manager_questions.html')

    def post(self, request):
        data = {
            'message': "error"
        }
        action = request.POST["action"]
        if action == "page_question":
            question_id = request.POST.get('question_id')
            question_id = self.decode_id(question_id)
            if not question_id or not request.POST.get('body'):
                return HttpResponseNotFound()

            qa_res = requests.post(
                url=settings.SERVER_FULL_URL + '/api/v1/faq_manager/',
                headers=self.get_http_header(request),
                data={
                    "question_id": question_id,
                    "question": request.POST.get('body'),
                    "subject": request.POST.get('subject'),
                    "answer": request.POST.get('answer'),
                    "action": 'page_question',
                }
            )
            self.is_auth_valid(request, qa_res)
            if qa_res.status_code == 201:
                data["message"] = 'success'
        else:
            qa_res = requests.post(
                url=settings.SERVER_FULL_URL + '/api/v1/faq_manager/',
                headers=self.get_http_header(request),
                data={
                    "question": request.POST.get('body'),
                    "subject": request.POST.get('subject'),
                    "answer": request.POST.get('answer'),
                    "sub_category": request.POST.get('sub_category'),
                    "action": 'page_top_expert',
                }
            )
            self.is_auth_valid(request, qa_res)
            if qa_res.status_code == 201:
                data["message"] = 'success'

        return JsonResponse(data)


class GetQuestion(BaseViewClass):
    def get(self, request):
        question_id = request.GET.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/' + str(question_id),
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, qa_res)

        return JsonResponse(qa_res.json())


class Question(BaseViewClass):
    def get(self, request, question_id):
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/' + str(question_id),
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, qa_res)

        return render(
            context={
                'question': qa_res.json(),
            },
            request=request,
            template_name='apps/hamraz/manager/question.html'
        )


class Workspace(BaseViewClass):
    def get(self, request):
        role = request.user.userbox.role_select
        questions = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/workspace',
            headers=self.get_http_header(request),
            params=self.add_pagination_param(request, {'role': role}),
        )
        self.is_auth_valid(request, questions)

        try:
            questions = questions.json()
        except:
            questions = []

        pagination_data = self.return_pagination(response=questions, page=request.GET.get('page', 1))

        context = {
            'questions': questions,
            'pagination_data': pagination_data,
        }

        if request.user.userbox.role_select == 'top_expert':
            context['top_expert'] = 'True'
        else:
            context['top_expert'] = 'False'

        return render(
            context=context,
            request=request,
            template_name='apps/hamraz/manager/workspace.html'
        )


class WorkspaceFaq(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/faq_manager/",
            headers=self.get_http_header(request)
        )
        try:
            faq_res = get_res.json()
        except:
            faq_res = []

        pagination_data = self.return_pagination(response=faq_res, page=request.GET.get('page', 1))

        context = {
            "faq_list": faq_res,
            "pagination_data": pagination_data,
        }

        return render(
            request=request,
            template_name='apps/hamraz/manager/workspace_faq.html',
            context=context
        )


class WorkspaceStatistics(BaseViewClass):
    def get(self, request):
        get_res = requests.get(
            url=settings.SERVER_FULL_URL + "/api/v1/questions_manager/statistics/",
            headers=self.get_http_header(request)
        )
        self.is_auth_valid(request, get_res)
        try:
            statistics_res = get_res.json()
        except:
            statistics_res = []

        context = {
            "statistics": statistics_res,
        }

        return render(
            request=request,
            template_name='apps/hamraz/manager/workspace_statistics.html',
            context=context
        )


class AcceptFaqQuestion(BaseViewClass):
    def post(self, request):
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/faq_manager/accept/',
            headers=self.get_http_header(request),
            data={"question_id": question_id}
        )
        self.is_auth_valid(request, qa_res)

        context = {
            'statue_code': qa_res.status_code
        }
        return JsonResponse(context)


class RemoveFaqQuestion(BaseViewClass):
    def post(self, request):
        question_id = request.POST.get('question_id')
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/faq_manager/remove/',
            headers=self.get_http_header(request),
            data={"question_id": question_id}
        )
        self.is_auth_valid(request, qa_res)

        context = {
            'statue_code': qa_res.status_code
        }
        return JsonResponse(context)


class AnswerQuestion(BaseViewClass):
    def get(self, request, question_id):
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        qa_res = requests.get(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/' + str(question_id),
            headers=self.get_http_header(request),
        )
        self.is_auth_valid(request, qa_res)

        return render(
            context={
                'question': qa_res.json(),
            },
            request=request,
            template_name='apps/hamraz/manager/answer_question.html'
        )

    @staticmethod
    def cleaned_data(request):
        post_req = {
            'body': request.POST.get('question_body', ''),
        }

        post_files = []
        for file_item in request.FILES.getlist('files[]'):
            post_files.append(
                ('files[]', (file_item.name, file_item.file.read(), file_item.content_type))
            )

        return post_files, post_req

    def post(self, request, question_id):
        post_files, post_req = self.cleaned_data(request)
        old_question_id = question_id
        question_id = self.decode_id(question_id)
        if not question_id:
            return HttpResponseNotFound()

        post_req['question_id'] = question_id

        que_res = requests.post(
            url=settings.SERVER_FULL_URL + '/api/v1/questions_manager/answer/',
            headers=self.get_http_header(request),
            data=post_req,
            files=post_files,
        )
        self.is_auth_valid(request, que_res)
        return redirect(reverse("answer_question", kwargs={"question_id": old_question_id}))
