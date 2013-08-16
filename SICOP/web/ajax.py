from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

@dajaxice_register
def multiplicar(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()