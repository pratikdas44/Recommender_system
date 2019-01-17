from django.shortcuts import render
from django.views.generic.edit import CreateView
from tutor.forms import TeacherFeedbackForm
from tutor.models import TeacherFeedback, Teacher
from django.urls.base import reverse_lazy, reverse
from django.http import HttpResponsePermanentRedirect
from tutor import MLRec
from rest_framework import viewsets
from rest_framework.response import Response
from tutor.serializers import TeacherFeedbackSerializer, TeacherSerializer


def sim_teacher(request):
    obs = Teacher.objects.all().order_by('TEACHER_NAME')
    return render(request, "sim.html", {"teachers": obs})

def sim_res(request):
    tid = request.GET["tid"]
    y1 = MLRec.get_similar(int(tid))
    return render(request, "sim_res.html", {"teachers": y1})


def home(request, pk):
    # ob = TeacherFeedback.objects.get(pk=pk)
    MLRec.training()
    y1 = MLRec.popularity_based_sug()
    y2 = MLRec.getRecByItemSim(int(pk))
    y3 = MLRec.get_rec_by_similar_users(int(pk))
    y4 = MLRec.getRecBySimUserItemSim(int(pk))
    # ob.PRED_HOUR=y
    # ob.save()
    return render(request, "home.html", {"popu": y1[:5], "simToLiked":y2[:5], "bySimUser":y3[:5], "bySimUser2":y4[:5]})

# Create your views here.
class TeacherFeedbackCreate(CreateView):
#     fields=["branch", "sem"]
    form_class=TeacherFeedbackForm
    model = TeacherFeedback
    def get_success_url(self):
        # return HttpResponsePermanentRedirect(reverse('done', kwargs={ 'insid':self.object.id}))
      # return reverse('done', {'insid': self.object.id})
      return reverse('done',args=(self.object.id,))
    # success_url = reverse_lazy('done')

class TeacherFeedbackViewSet(viewsets.ModelViewSet):
    queryset = TeacherFeedback.objects.all().order_by('-id')
    serializer_class = TeacherFeedbackSerializer
    def create(self, request, *args, **kwargs):
        super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)
        ob = TeacherFeedback.objects.latest('id')
        popu = MLRec.popularity_based_sug()
        return Response({"status": "Success", "Most Popular": popu, 'tmp': args})  # Your override
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('-id')
    serializer_class = TeacherSerializer
    # def create(self, request, *args, **kwargs):
    #     super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)
    #     ob = TeacherFeedback.objects.latest('id')
    #     y = MLRec.popularity_based_sug()
    #     return Response({"status": "Success", "Hours": y, 'tmp': args})  # Your override
