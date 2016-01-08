from django.shortcuts import render
from django.shortcuts import render_to_response, render
from django.template import RequestContext
import sys
import json
sys.path.append('.../myfreeling/APIs/python')
import freeling
import codecs
import re
import time
from datetime import date
from .forms import NameForm


## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local";

DATA = FREELINGDIR+"/share/freeling/";
LANG="es";

freeling.util_init_locale("default");

# create language analyzer
#la=freeling.lang_ident(DATA+"common/lang_ident/ident.dat");

# create options set for maco analyzer. Default values are Ok, except for data files.
op= freeling.maco_options("es");
op.set_active_modules(0,1,1,1,1,1,1,1,1,1);
op.set_data_files("",DATA+LANG+"/locucions.dat", DATA+LANG+"/quantities.dat",
                  DATA+LANG+"/afixos.dat", DATA+LANG+"/probabilitats.dat",
                  DATA+LANG+"/dicc.src", DATA+LANG+"/np.dat",
                  DATA+"common/punct.dat");

# create analyzers
tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
sp=freeling.splitter(DATA+LANG+"/splitter.dat");
mf=freeling.maco(op);

#tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",1,2);
#sen=freeling.senses(DATA+LANG+"/senses.dat");

parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
dep=freeling.dep_txala(DATA+LANG+"/dep/dependences.dat", parser.get_start_symbol());

DATA = "El gato come pescado y bebe agua."

res=''



# Create your views here.

def index(request):
    """Renders the index page"""
    get_form = ''
    get_lemma = ''
    get_tag = ''
    get_senses_string = ''
    respuesta = '('
    l = tk.tokenize(DATA)
    ls = sp.split(l,0)
    # Analisis morfologico
    ls = mf.analyze(ls)

    for s in ls :
       ws = s.get_words();
       for w in ws :
          get_form += w.get_form()+" "
          respuesta +=("("+w.get_form()+" ("+w.get_tag()+")) ")
          # get_lemma += w.get_lemma()+" "
          # get_tag += w.get_tag() + " "
          #get_senses_string += w.get_senses_string() + " "
    respuesta +=")"
    # return render_to_response('index.html',{'get_form': get_form,'get_lemma':get_lemma,'get_tag':get_tag,
    #                                         'get_senses_string': get_senses_string})
    return render_to_response('index.html',{'respuesta':respuesta, 'get_form': get_form})


def get_name(request):
     # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            print('OK')
            data = form.cleaned_data['textInput']
            get_form = ''
            get_lemma=''
            respuesta = '('
            l = tk.tokenize(data)
            ls = sp.split(l,0)
            palabras = 0
            # Analisis morfologico
            ls = mf.analyze(ls)
            for s in ls :
               ws = s.get_words();
               for w in ws :
                  get_form += w.get_form()+" "
                  respuesta +=("("+w.get_form()+" ("+w.get_tag()+")) ")
                  get_lemma += w.get_lemma()+" "
                  # get_tag += w.get_tag() + " "
                  #get_senses_string += w.get_senses_string() + " "
                  palabras+=1
            respuesta +=")"
            return render_to_response('index.html', RequestContext(request,{'respuesta':respuesta, 'get_form': get_form
                                                                            , 'palabras':(palabras-1), 'get_lemma': get_lemma}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'index.html', {'respuesta': 'EXCEPCION'})