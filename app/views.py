from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import os

def download_excel(request):

    excel_file_path = os.path.join(settings.STATIC_ROOT, 'your_excel_file.xlsx')


    with open(excel_file_path, 'rb') as excel_file:

        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename="your_excel_file.xlsx"'

        return response

class Home(View):
    def get(self,request,*args, **kwargs):
        return render(request,"home.html")
    
