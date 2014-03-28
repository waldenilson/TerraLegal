from django.http.response import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus.doctemplate import SimpleDocTemplate
import time
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer, Image, PageBreak
from reportlab.lib.units import inch, cm
from odslib import ODS
import os
import csv
from django.http import HttpResponseRedirect
from django.template.defaultfilters import length
from reportlab.platypus.tables import Table
from reportlab.lib import styles
import datetime
from sicop.admin import mes_do_ano_texto

def relatorio_base(request, lista, titulo):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+str(titulo).replace(' ', '_')+'.pdf"'

    p = canvas.Canvas(response)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
     
    p.drawString(30,750,titulo)
    p.drawString(500,750,"28/08/2013")
    p.drawString(30,730,'Usuario: '+str(request.user))
    p.drawString(30,715,'SRFA-02')
    
    x = 0;
    for obj in lista:
        p.drawString(50,650 - x,"N.: "+str(obj))
        x += 50
    
    p.drawString(500,100,"total")
    p.save()
     
    return response


def relatorio_pdf_base_header(response, titulo):
    response['Content-Disposition'] = 'attachment; filename='+titulo+'.pdf'
    return SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)

def relatorio_pdf_base_header_title(title):
    dados = []
    dados.append( (title,'') )
    return dados

def relatorio_pdf_base(response, doc, elements, dados):
    table = Table(dados, colWidths=350, rowHeights=35)
    elements.append(table)
    doc.build(elements) 
    return response

def relatorio_ods_base_header( nome_planilha, titulo_planilha, total_registro, ods):
    # sheet title
    sheet = ods.content.getSheet(0)
    sheet.setSheetName( nome_planilha )
    
    # title
    sheet.getCell(0, 0).setAlignHorizontal('center').stringValue( titulo_planilha ).setFontSize('20pt').setBold(True).setCellColor("#ccff99")
    sheet.getRow(0).setHeight('25pt')
    sheet.getColumn(0).setWidth('10cm')
    
    data_geracao = datetime.datetime.now()
    data_extenso = str(data_geracao.day)+' de '+mes_do_ano_texto(data_geracao.month)+" de "+str(data_geracao.year) 
        
    sheet.getCell(0,1).setAlignHorizontal('center').stringValue( 'Data: ' ).setFontSize('16pt').setBold(True)
    sheet.getCell(1,1).stringValue( str( data_extenso ) ).setFontSize('14pt')

    sheet.getCell(0,2).setAlignHorizontal('center').stringValue( 'Total: ' ).setFontSize('16pt').setBold(True)
    sheet.getCell(1,2).stringValue( str(total_registro) ).setFontSize('14pt')
                
    ods.content.mergeCells(0,0,7,1)
    ods.content.mergeCells(1,1,2,1)
    ods.content.mergeCells(1,2,2,1)
    
    return sheet

def relatorio_ods_base(ods, titulo):
    # generating response
    response = HttpResponse(mimetype=ods.mimetype.toString())
    response['Content-Disposition'] = 'attachment; filename='+str(titulo)+'".ods"'
    ods.save(response)    
    return response
    
def relatorio_csv_base(response, titulo):
    response['Content-Disposition'] = 'attachment; filename='+str(titulo)+'.csv'
    writer = csv.writer(response)
    return writer

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
