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
DATA2 = """By John Timmer | Last updated March 19, 2010 6:38 AM\nEarlier this year, Amazon found itself in a showdown over e-book pricing with publisher Macmillan, which wanted the ability to set pricing for its works. Amazon initially pulled all of Macmillan's titles off its virtual shelves but, a few days later, conceded there was little it could do \u2014Macmillan's works went back on sale, and Amazon apparently gave up on trying to force its prices on the company. Despite that rousing lack of success, reports are now indicating that several other publishers may get the same treatment, as Amazon is threatening to stop selling their works as well.\nIndications of an ongoing fight between Amazon and book publishers were apparent almost as soon as the Macmillan matter was settled . Amazon had been purchasing e-books from publishers at a wholesale rate, which allowed it to set the retail prices; rumor had it that the company was selling works at a loss in order to push Kindle sales. Publishers, which have an obvious interest in keeping prices for their work higher, were certainly not pleased with this approach.\nThe impending entry of Apple into the e-book field seems to have brought matters to a head. Apple apparently offered publishers an agency model, in which they get to set prices for their works and simply provide Apple with its (apparently standard) 30 percent cut. In essence, Apple did to Amazon what Amazon had done to it in the music business, where the labels have now been granted the ability to set their own prices by both companies after Amazon pioneered that deal.\nBoth The New York Times and Publisher's Marketplace ( paywall-free excerpt available ) now indicate that Amazon has accepted the agency model, but is seeking to burden it with terms that the publishers are not anxious to go along with. But, should they refuse, the retailer is threatening to give them the Macmillan treatment and stop selling their books.\nFor starters, Amazon wants to lock the publishers into three-year contracts. With several new Kindle competitors either released or very close to market, the e-book economy is likely to experience a time of significant flux, so the publishers would rather reserve the right to keep their options open to adapt to any changes that occur.\nThe other sticking point appears to be a price lock-in: both Apple and Amazon are looking for contracts in which both are guaranteed the lowest price being offered. That would eliminate the ability of publishers to favor one or the other e-book store by offering it better prices. Again, the publishers have probably learned from the record labels' experience that wielding this sort of favoritism can be an extremely powerful lever, and are unlikely to be happy about giving it up.\nThe surprise, however, is that Amazon is even bothering to try this with the major publishers after its failure to bring Macmillan to heel. One of its weaknesses here is the success of its programs for affiliates and used books; even if Amazon pulls its own sales of a major work, it's often easy to use the company's Web interface to pick it up used or from a retailer that uses Amazon's storefront.\nAs The Times points out, the threat is likely to carry a lot more weight with smaller publishers, who don't have a large presence in the retail market, meaning Amazon is their primary outlet for\u00a0Web\u00a0sales. As usual, the little guys are most likely to be trampled as the retailing and publishing giants scuffle.\nUser comments\nDon't Miss : Promos & Insight\n-1\ncenturies\n"""
lin="Mary had a little lamb. Is it really a lost cause."

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
            respuesta = '('
            l = tk.tokenize(data)
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
            return render_to_response('index.html', RequestContext(request,{'respuesta':respuesta, 'get_form': ''}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'index.html', {'respuesta': 'nada'})