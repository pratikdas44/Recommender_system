from django.shortcuts import render
from django.views.generic.edit import CreateView
from rspeed.forms import ReadSpeedForm
from rspeed.models import ReadSpeed
from django.urls.base import reverse_lazy, reverse
from django.http import HttpResponsePermanentRedirect
from rspeed import ML
from rest_framework import viewsets
from rest_framework.response import Response
from rspeed.serializers import ReadSpeedSerializer

def home(request, pk):
    ob = ReadSpeed.objects.get(pk=pk)
    y = ML.pred(ob)
    return render(request, "home.html", {"insid": y})

# Create your views here.
class ReadSpeedCreate(CreateView):
#     fields=["branch", "sem"]
    form_class=ReadSpeedForm
    model = ReadSpeed
    def get_success_url(self):
        # return HttpResponsePermanentRedirect(reverse('done', kwargs={ 'insid':self.object.id}))
      # return reverse('done', {'insid': self.object.id})
      return reverse('done',args=(self.object.id,))
    # success_url = reverse_lazy('done')

class ReadSpeedViewSet(viewsets.ModelViewSet):
    queryset = ReadSpeed.objects.all().order_by('-id')
    serializer_class = ReadSpeedSerializer
    def create(self, request, *args, **kwargs):
        super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)
        ob = ReadSpeed.objects.latest('id')
        # print("*"*100)
        # print(pk)
        # ob = ReadSpeed.objects.get(pk=pk)
        y = ML.pred(ob)
        return Response({"status": "Success", "Hours": y})  # Your override
