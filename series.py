# -*- coding: utf-8 -*- 

# Los directorios donde se encuentran las series
directorios = \
r'''
D:\Series
'''.split('\n')

# Directorio donde vas a alojar la web
web_path = ''

# Traducción para algunos géneros
gen = {
    'Crime':        u'Crimen',
    'Action':       u'Acción',
    'Drama':        u'Drama',
    'Comedy':       u'Comedia',
    'Adventure':    u'Aventuras',
    'Thriller':     u'Thriller'
}


##############################################################################
'                                   HTML                                      '
##############################################################################
html_header = u'''<!DOCTYPE html><html lang="es"><head>
    <meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge">    <meta name="viewport" content="width=device-width, initial-scale=1"> <meta name="description" content=""><meta name="author" content=""><link rel="icon" href="favicon.ico"><title>Series</title>
    <link href="css/bootstrap.min.css" rel="stylesheet"><link href="css/jumbotron-narrow.css" rel="stylesheet">
  </head><body>
  <h1 class="header" align="center">Series<br></h1><div>'''

html_serie_row = '''<div class="row">'''
html_serie = u'''
                <!--- Serie --->
                <div class="col-xs-4">
                    <div class="row">
                        <div class="col-xs-4"><img src="{img}" alt="{titulo}" class="img-thumbnail"></div>
                        <div class="col-xs-8" align="left">
                            <h2>{titulo} ({anyo})</h2>
                            <ul>
                                <li><b>Genero</b>: {genero}</li>
                                <li><b>Temporadas</b>: {temporadas}</li>
                                <li><b>Mas info</b>: {masinfo}</li>
                            </ul><br>
                            <p><a class="btn btn-info" data-toggle='collapse' data-target="#{toggle}" aria-expanded="false" aria-controls="{toggle}">Ver capítulos</a></p>
                            <div class="collapse" id="{toggle}">
                              <div class="well">
                                {enlaces}
                              </div>
                            </div>
                        </div>
                    </div>
                </div>
'''
html_serie_finrow = '''</div>'''

html_season = u'''<a href='#'>%s</a>'''

html_footer = u'''<footer class="footer"></footer></div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body></html>'''


def series_links(d):
    ''' 
    Devuelve una lista de links a los capítulos de una temporada 
        de una serie concreta.

    Buscamos patrones comunes:
        1x01, S01E03, 101...
    '''
    path = d[u'path']
    patterns = [ \
        # Del tipo: 1x01, 12x24
        '(\d{1,2}x\d\d)', 
        
        # S01E01, S12E24
        '(S\d\dE\d\d)', 
        
        # 101, 1224
        '(\d{3,4})']
    patterns = [re.compile(regex) for regex in patterns]

    capitulos = []
    for temporada in [x for x in ls(path) if not '.' in x]:
        for capitulo in ls('%s/%s' %(path,temporada)):
            print capitulo
            # 1x03
            p = re.search(patterns[0], capitulo)
            if p and len(p.groups()):
                cap = p.groups()[0]
                capitulos.append( (cap, u'%s/%s/%s' % (utf(path), utf(temporada) , utf(capitulo) )) )
                print cap
                continue

            # S01E03
            p = re.search(patterns[1], capitulo)
            if p and len(p.groups()):
                cap = p.groups()[0]
                cap = u'%s%sx%s%s' % (cap[1] if cap[1]!=0 else '', cap[2], cap[4], cap[5])
                capitulos.append( ( cap, u'%s/%s/%s' % (utf(path), utf(temporada) , utf(capitulo))  ))
                print cap
                continue

            # 103
            p = re.search(patterns[2], capitulo)
            if p and len(p.groups()):
                cap = p.groups()[0]
                if len(cap)==3:  cap = u'%sx%s%s'   % (cap[0], cap[1], cap[2])
                else:            cap = u'%s%sx%s%s' % (cap[0], cap[1], cap[2], cap[3])
                capitulos.append( ( cap, u'%s/%s/%s' % (utf(path), utf(temporada) , utf(capitulo) )))
                print cap
                continue

            # Si tiene algun numero lo añado
            if re.search('\d', capitulo): 
                capitulos.append( ( capitulo, u'%s/%s/%s' % (path, temporada, capitulo) )  )
    return capitulos
                
                    

def serie_HTML(d, download=False):
    ''' Devuelve el HTML para una determinada serie '''

    return html_serie.format(
        img         = d[u'img'] if not download else 'imgs/%s.jpg' % download_image(d), 
        titulo      = d[u'name'].decode('utf-8', 'replace'), 
        anyo        = d[u'year'], 
        genero      = gen[d[u'maingenre']],
        temporadas  = u' '.join( [html_season % idx for idx in xrange(1,d[u'seasons']+1)]),
        masinfo     = u'',
        toggle      = d[u'name'].decode('utf-8', 'replace').split(' ')[0],
        enlaces     = u'\n'.join( [(u'<a href="file:///%s">%s</a>' % (cap[1],cap[0])) for cap in series_links(d)])
        )

##############################################################################
'                             Funciones aux                                   '
##############################################################################
def read(pathFNAME):
    '''
        Abre un fichero, lo lee y devuelve un diccionario.
    '''
    with open(pathFNAME, 'r', 'utf-8') as fn:
        return eval(fn.read())


def paths_de_las_series(orden=lambda (p,d): d[u'name']):
    '''
        Buscamos por todos los directorios y nos guardamos dónde están las
            series de forma ordenada.
    '''
    paths = []
    for pathBase in [d for d in directorios if d]:
        for path in ls(pathBase):
            if not '.' in path:
                if 'info.json' in ls('%s/%s'%(pathBase, path)):
                    # Save the path
                    camino = '%s/%s' % (pathBase, path)
                    inform = read('%s/info.json' % (camino))
                    inform[u'path'] = camino
                    paths.append((camino, inform))
                    
    return sorted(paths, key=orden)

''' Convierte una string en utf-8 '''
utf = lambda x: x.decode('utf-8', 'replace')

def urlify(name):
    '''
        Devuelve una string como si fuera una URL
    '''
    name = name#.decode('utf-8', 'replace')
    for l, ll in zip(u'áàéèíìóòúù:',u'aaeeiioouu_'):
        name = name.replace(l,ll)
    return (name.encode('ASCII', 'replace')).replace(' ', '-')


def download_image(d):
    '''
        Descarga la imagen de la serie
    '''
    # Nombre del fichero
    fName = urlify(d[u'name'])
    
    # Comprueba si ya está descargada
    if ('%s.jpg' % fName) in ls('%s/imgs/' % web_path):
        pass
    else:
        call("wget %s -O %s.jpg" % (d[u'poster'][u'large'], fName) )
        sleep(2)
        mv('%s.jpg' % fName, '%s/imgs/%s.jpg' % (web_path, fName))
    return fName
    
##############################################################################
'                               Main code                                     '
##############################################################################
if __name__=='__main__':
    '''
        Código principal
    '''
    from shutil import move as mv
    from os import listdir as ls
    from time import sleep
    from subprocess import call
    
    import re
    
    import codecs
    open = codecs.open

    ''' Creamos el HTML '''
    html =  html_header
    ps = paths_de_las_series()
    la, lb, lc = len(ps[0::3]), len(ps[1::3]), len(ps[2::3])
    for a, b, c in zip( ps[0::3] , \
                        ps[1::3] + ([0] if la>lb else []),  \
                        ps[2::3] + ([0] if la>lc else [])):
        html += html_serie_row
        html += serie_HTML(a[1]) if a else ''
        html += serie_HTML(b[1]) if b else ''
        html += serie_HTML(c[1]) if c else ''
        html += html_serie_finrow
        
        
    html += html_footer

    ''' Guardamos el HTML '''
    location = r'%s/index.html' % web_path
    with open(location, 'w', 'utf-8') as f:
        f.write(html)
  
