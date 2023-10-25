from django.shortcuts import render
from .models import Words, Sentences
from pymorphy2 import MorphAnalyzer
m = MorphAnalyzer()
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

def search_func(search_first):
    if search_first[0]!='"' and search_first[-1]!='"':
        res = []
        search = search_first.split()
        text_id = 1
        while text_id <= Words.objects.aggregate(Max('nmb_text'))['nmb_text__max']:
            df = Words.objects.filter(nmb_text=text_id)
            sent_ind = 1
            all = []
            spis = {}
            while sent_ind <= df.aggregate(Max('nmb_text'))['nmb_text__max']:
                srch_i = 0
                words = df.filter(nmb_sent=sent_ind).values_list('word', flat=True)
                tags = df.filter(nmb_sent=sent_ind).values_list('pos', flat=True)
                lemmas = df.filter(nmb_sent=sent_ind).values_list('lemma', flat=True)
                word_i = 0
                spis_n = []
                while word_i<len(words) and srch_i<len(search):
                    if search[srch_i][0]=='"' and search[srch_i][-1]=='"':
                        if '+' in search[srch_i]:
                            d = search[srch_i].split('+')
                            if d[0]==words[word_i] and d[1]==tags[word_i]:
                                spis_n.append(words[word_i])
                                srch_i+=1
                            else:
                                word_i -=len(spis_n)
                                srch_i = 0
                                spis_n = []
                        elif words[word_i] == search[srch_i]:
                            spis_n.append(words[word_i])
                            srch_i+=1
                        elif tags[word_i] == search[srch_i]:
                            spis_n.append(words[word_i])
                            srch_i+=1
                        else:
                            word_i -=len(spis_n)
                            srch_i = 0
                            spis_n = []
                    elif search[srch_i][0]!='"' and search[srch_i][-1]!='"':
                        lem = m.parse(search[srch_i])[0].normal_form
                        if '+' in search[srch_i]:
                            d = search[srch_i].split('+')
                            if m.parse(d[0])[0].normal_form==lemmas[word_i] and d[1]==tags[word_i]:
                                # spis_n.append(lemmas[word_i])
                                spis_n.append(words[word_i])
                                srch_i+=1
                            else:
                                word_i -=len(spis_n)
                                srch_i = 0
                                spis_n = []
                        elif lemmas[word_i] == lem:
                            # spis_n.append(lemmas[word_i])
                            spis_n.append(words[word_i])
                            srch_i+=1
                        elif tags[word_i] == search[srch_i]:
                            spis_n.append(words[word_i])
                            srch_i+=1
                        else:
                            word_i -=len(spis_n)
                            srch_i = 0
                            spis_n = []
                    if spis_n!=[] and len(search) == len(spis_n):
                        if sent_ind not in spis.keys():
                            spis[sent_ind] = []
                            spis[sent_ind].append(' '.join(spis_n))
                        else:
                            spis[sent_ind].append(' '.join(spis_n))
                        srch_i = 0
                        word_i -=len(spis_n)
                        word_i += 1
                        spis_n = []
                    word_i+=1
                sent_ind+=1   
            all = [[spis[k], Sentences.objects.filter(nmb_text=text_id).filter(nmb_sent=k).values_list('sentence', flat=True)[0]] for k in spis.keys()]
            if all != []:
                res.append([all, Sentences.objects.filter(nmb_text=text_id).values_list('author', flat=True)[0], Sentences.objects.filter(nmb_text=text_id).values_list('title', flat=True)[0]])
            text_id+=1
            spis = {}

    elif search_first[0]=='"' and search_first[-1]=='"':
        res = []
        search = (search_first[1:-1]).split()
        text_id = 1
        while text_id <= Words.objects.aggregate(Max('nmb_text')).get('nmb_text__max'):
            df = Words.objects.filter(nmb_text=text_id)
            sent_ind = 0
            all = []
            spis = {}
            while sent_ind <= df.aggregate(Max('nmb_text')).get('nmb_text__max'):
                srch_i = 0
                words = df.filter(nmb_sent=sent_ind).values_list('word', flat=True)
                tags = df.filter(nmb_sent=sent_ind).values_list('pos', flat=True)
                lemmas = df.filter(nmb_sent=sent_ind).values_list('lemma', flat=True)
                word_i = 0
                spis_n = []
                while word_i<len(words) and srch_i<len(search):
                    if '+' in search[srch_i]:
                        dat = search[srch_i].split('+')
                        if dat[0]==words[word_i] and dat[1]==tags[word_i]:
                            spis_n.append(words[word_i])
                            srch_i+=1
                        else:
                            word_i -=len(spis_n)
                            srch_i = 0
                            spis_n = []
                    elif words[word_i] == search[srch_i]:
                        spis_n.append(words[word_i])
                        srch_i+=1
                    elif tags[word_i] == search[srch_i]:
                        spis_n.append(words[word_i])
                        srch_i+=1
                    else:
                        word_i -=len(spis_n)
                        srch_i = 0
                        spis_n = []
                    if spis_n!=[] and len(search) == len(spis_n):
                        if sent_ind not in spis.keys():
                            spis[sent_ind] = []
                            spis[sent_ind].append(' '.join(spis_n))
                        else:
                            spis[sent_ind].append(' '.join(spis_n))
                        srch_i = 0
                        word_i -=len(spis_n)
                        word_i += 1
                        spis_n = []
                    word_i+=1
                sent_ind+=1
            all = [[spis[k], Sentences.objects.filter(nmb_text=text_id).filter(nmb_sent=k).values_list('sentence', flat=True)[0]] for k in spis.keys()]
            if all != []:
                res.append([all, Sentences.objects.filter(nmb_text=text_id).values_list('author', flat=True)[0], Sentences.objects.filter(nmb_text=text_id).values_list('title', flat=True)[0]])
            text_id+=1
            spis = {}
    return res

def search(request):
    context = {}
    if request.method == 'POST':
        cache.delete('my_data')
        query = request.POST.get('query')
        sentences_res = search_func(query)
        sentences = Paginator(sentences_res, 10)
        cache.set('my_data', [sentences, query], 60*30)
        page = request.GET.get('page')
        context['all_sentences'] = sentences.get_page(page)
        context['query'] = query
        try:
            items_page = sentences.page(page)
        except PageNotAnInteger:
            items_page = sentences.page(1)
        except EmptyPage:
            items_page = sentences.page(sentences.num_pages)

        context['items_page'] = items_page
    elif request.method == 'GET':       
        if request.GET.get('page'):
            sentences = cache.get('my_data')[0]
            query = cache.get('my_data')[1]
            page = request.GET.get('page')
            context['all_sentences'] = sentences.get_page(page)
            context['query'] = query
            try:
                items_page = sentences.page(page)
            except PageNotAnInteger:
                items_page = sentences.page(1)
            except EmptyPage:
                items_page = sentences.page(sentences.num_pages)
            context['items_page'] = items_page
        else:
            context['query'] = None
            cache.delete('my_data')
    return render(request, 'search_results.html', context=context)