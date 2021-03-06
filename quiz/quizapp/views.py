from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import *
from natijaapp.models import Foydalanuvchi


class IndexView(View):
    def get(self, request):
        quiz = Quiz.objects.all()
        return render(request, 'index.html', {'quiz':quiz})
class QuizView(View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(id=pk)
        savollar = Savol.objects.filter(quiz = quiz)
        return render(request, 'quiz.html', {'quiz':quiz, 'savollar':savollar})
class QuizDataView(View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(id=pk)
        savollar = Savol.objects.filter(quiz=quiz)
        questions = []
        for s in savollar:
            answers = []
            javoblar = Javob.objects.filter(savol=s)
            for j in javoblar:
                answers.append(j.matn)
            questions.append({str(s):answers})
        return JsonResponse({
            'data':questions,
            'time':quiz.davomiyligi,
        })
class QuizSaveView(View):
    def post(self, request, pk):
                if request:
                    questions = []
                    data = request.POST
                    data_ = dict(data.lists())

                    data_.pop('csrfmiddlewaretoken')

                    for k in data_.keys():
                        print('key: ', k)
                        question = Savol.objects.get(matn=k)
                        questions.append(question)

                    user = request.user
                    quiz = Quiz.objects.get(id=pk)

                    score = 0
                    marks = []
                    correct_answer = None

                    for q in questions:
                        a_selected = request.POST.get(q.matn)

                        if a_selected != "":
                            question_answers = Javob.objects.filter(savol=q)
                            for a in question_answers:
                                if a_selected == a.matn:
                                    if a.togri:
                                        score += 1
                                        correct_answer = a.matn
                                else:
                                    if a.togri:
                                        correct_answer = a.matn

                            marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
                        else:
                            marks.append({str(q): 'not answered'})

                    Foydalanuvchi.objects.create(quiz=quiz, user=user, baho=score)