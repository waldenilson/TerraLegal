from django.http.response import HttpResponse
from reportlab.platypus.doctemplate import SimpleDocTemplate
import time
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from django.utils.datetime_safe import date
from reportlab.pdfgen import canvas
import Canvas
from reportlab.lib import styles


def relatorio_base(request, lista):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="srfa02.pdf"'

    p = canvas.Canvas(response)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
     
    p.drawString(30,750,'Nome do Relatorio')
    p.drawString(500,750,"28/08/2013")
    p.drawString(30,730,'Usuario')
    p.drawString(30,715,'SRFA-02')
        
    p.drawString(50,650,"Coluna 01")
    p.drawString(200,650,"Coluna 02")
    p.drawString(350,650,"Coluna 03")
    
    p.drawString(500,100,"total")
    p.save()
     
    return response


def relatorio_documento_base(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="srfa02.pdf"'

    doc = SimpleDocTemplate(response, rightMargin=72,leftMargin=72, topMargin=72,bottomMargin=18)
    
    Story=[]
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
     
    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
     
     
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=12>%s</font>' % formatted_time
     
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
     
    # Create return address
    ptext = '<font size=12>%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))       
    for part in address_parts:
        ptext = '<font size=12>%s</font>' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))   
     
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
     
    ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
            You will receive %s issues at the excellent introductory price of $%s. Please respond by\
            %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName, 
                                                                                                    issueNum,
                                                                                                    subPrice,
                                                                                                    limitedDate,
                                                                                                    freeGift)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
     
     
    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size=12>Ima Sucker</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)
    
    return response
