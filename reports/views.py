# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import json
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.frames import Frame
import time


cm = 2.54

class ReportsViewset(viewsets.ViewSet):
  permission_classes = (AllowAny,)

  def list(self, request):
    return JsonResponse({'GET': 'created'}, safe=False)


  def create(self, request):
    # Create the HttpResponse object with the appropriate PDF headers.
    content = json.loads(request.body)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    doc = SimpleDocTemplate(response, rightMargin=6.5, leftMargin=6.5, topMargin=15 * cm, bottomMargin=15 * cm)
    doc.author = "carlos"


    def drawFooter(canvas, doc):
        x = 330
        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(0.5)
        canvas.line(66, 78, A4[0] - 66, 78)
        canvas.setFont('Helvetica', 10)
        canvas.drawString(A4[0]-x, 65, "Generated by User")
        canvas.restoreState()


    doc.build(self._PDFElements(doc, content), onFirstPage=drawFooter)

    return response


  def _PDFElements(self, doc, content):
    time_now = time.strftime("%I:%M:%S:%p %m-%d-%Y", time.gmtime())

    elements = []

    content['report'].insert(0, ["kiloWatts/month", "Date"]) # table headers

    Hstyle = getSampleStyleSheet()
    Hstyle = Hstyle["BodyText"]
    Hstyle.alignment = TA_CENTER
    Hstyle.fontSize = 28
    Hstyle.spaceBefore = 20
    Hstyle.spaceAfter = 10

    data=content['report']
    I = Image('assets/images/ql-logo.jpg', 520, 475)
    I.drawHeight =  10*cm
    I.drawWidth = 40*cm
    H1 = Paragraph("Monthly Energy", Hstyle)
    H2 = Paragraph("Consumption Report", Hstyle)
    d = Drawing(800, 18)
    d.add(Line(0, 0, 570, 0))
    s = getSampleStyleSheet()
    s = s["Normal"]
    s.alignment = TA_CENTER
    date = Paragraph(time_now, s)
    page = "GENERATED BY User at " + time_now
    x = 128

    style = TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(1,1),(1,1),colors.black),
                           ('TEXTCOLOR',(0,0),(0,0),colors.blue),
                           ('ALIGN',(0,-1),(0,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(0,-1),colors.black),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ])
     
    s.wordWrap = 'LTR'
    s.fontSize = 14
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    if len(data2) < 2:
        data2.insert(1, ['no data', 'no data'])

    t=Table(data2, (50*cm,50*cm), [13*cm] * len(data2), style=style, spaceBefore=50, spaceAfter=100)
     
    elements.append(I)
    elements.append(H1)
    elements.append(H2)
    elements.append(d)
    elements.append(date)
    elements.append(t)
    return elements
