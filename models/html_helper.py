

def icon_title(icon, title):
    return I(f' {str(title)}', _class=f'fa {str(icon)} fa-1x')


# iconos en https://fontawesome.com/v4.7.0/icons/
def grand_button(nombre, link, icono, **kwargs):
    """ nombre: 1 a 3 palabras"""
    lista = nombre.split()
    spanlist = []
    for i in lista:
        spanlist.append(SPAN(i.title()))
        spanlist.append(BR())
    result = DIV(spanlist)
    if 'vars' in kwargs:
        url = URL(link, vars=kwargs['vars'])
    else:
        url = URL(link)
    boton = A(TABLE(I(_class='fa ' + str(icono) + ' fa-3x'), result),
              _class="btn-square-blue",
              _href=url)
    return boton