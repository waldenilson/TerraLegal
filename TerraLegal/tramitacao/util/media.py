from django.views.static import serve
from django.contrib.auth.decorators import permission_required

@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def download(request, path, document_root):
    return serve(request, path, document_root)
