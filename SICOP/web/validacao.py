from django.contrib import messages

def validacao_form_peca_tecnica(request_form):
    warning = True
    if request_form.POST['tbcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione um Contrato')
        warning = False
    if request_form.POST['nrentrega'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da entrega')
        warning = False
    if request_form.POST['nrcpfrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um CPF valido para o requerente')
        warning = False
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do requerente maior que 4 letras')
        warning = False
    if request_form.POST['nrarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da area')
        warning = False
    if request_form.POST['nrperimetro'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do perimetro')
        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione uma Gleba') 
        warning = False
    return warning