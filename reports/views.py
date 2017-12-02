# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from rest_framework_jwt.settings import api_settings
import json
from django.core.serializers.json import DjangoJSONEncoder
import reportlab
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.platypus.tables import Table
from reportlab.graphics.shapes import Line, Drawing

cm = 2.54

# Create your views here.

class ReportsViewset(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
      return JsonResponse({'GET': 'created'}, safe=False)

    def create(self, request):
      # Create the HttpResponse object with the appropriate PDF headers.
      content  = json.loads(request.body)
      print(content['report'])
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

      elements = []

      content['report'].insert(0, ["kiloWatts/month", "date"])

      doc = SimpleDocTemplate(response, rightMargin=6.5, leftMargin=6.5, topMargin=15 * cm, bottomMargin=15 * cm)

      data=content['report']
      I = Image('assets/images/ql-logo.jpg', 500, 500)
      table = Table(data, colWidths=130, rowHeights=30)
      I.drawHeight =  15*cm
      I.drawWidth = 40*cm
      d = Drawing(800, 1)
      d.add(Line(0, 0, 570, 0))
      elements.append(I)
      elements.append(d)
      elements.append(table)
      doc.build(elements) 
      return response



