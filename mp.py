import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import re
import random
import json
from networkx.readwrite import json_graph

with open('1000_russkikh_poslovits_i_pogovorok.txt', 'r', encoding='utf-8') as f:
    file = f.readlines()
# загружаем json с графом
with open('data.json', 'r') as f:
    j = json.load(f)
graph = json_graph.node_link_graph(j)
len(graph.edges())

def find_sentense_with_a(posl):
  if '! ' in posl or '. ' in posl:
    return False
  else:
    for i in posl:
      if i in ':;–':
        return False
  return True

def split_into_sentences(texts):
  texts = texts.lstrip('   ').rstrip('\n')
  pattern = '\(.+\)'
  texts = re.sub(pattern, '', texts).replace('\xa0', '')
  return texts

# пропускаем ненужные теги
def pass_tag(word):
  result_tags = []
  list_all = []
  list_all.append(morph.parse(word)[0].tag.POS)
  list_all.append(morph.parse(word)[0].tag.animacy)
  list_all.append(morph.parse(word)[0].tag.gender)
  list_all.append(morph.parse(word)[0].tag.mood)
  list_all.append(morph.parse(word)[0].tag.number)
  list_all.append(morph.parse(word)[0].tag.person)
  list_all.append(morph.parse(word)[0].tag.tense)
  list_all.append(morph.parse(word)[0].tag.voice)
  for tag in list_all:
    if tag!= None:
      result_tags.append(tag)
  return ','.join(result_tags)

def put_tags(texts, return_POS = True):
  texts_lemmat = []

  if return_POS == True:
    for word in texts.split():
      pattern = '[^а-я\s]'
      word_without_punc = re.sub(pattern, '', word)
      texts_lemmat.append(morph.parse(word_without_punc)[0].tag.POS)
    return ' '.join(sorted(list(filter(None, texts_lemmat))))

  else:
    for word in texts.split():
      pattern = '[^а-я\s]'
      word_without_punc = re.sub(pattern, '', word)
      texts_lemmat.append(pass_tag(word_without_punc))
    return '|'.join(sorted(list(filter(None, texts_lemmat))))

def preproc(texts, return_POS):
  texts = texts.lower().lstrip('   ').rstrip('\n')
  pattern = '\(.+\)'
  texts = re.sub(pattern, '', texts)
  tags = put_tags(texts, return_POS)
  return (texts, tags)

  # список правильных пословиц
def find_right_poslov(file, graph):
  all_poslov = []
  for text in file:
      text = text.lower()
      text = split_into_sentences(text)
      if ', а ' in text and find_sentense_with_a(text) == True:
          two_parts = text.split(' а ')
          if two_parts[0] in graph.nodes() and len(list(graph.neighbors(two_parts[0]))) > 1:
              all_poslov.append(two_parts)
  return all_poslov

# ИТОГ !!!!!

def make_poslov(node, graph):
  poslv_2 = []
  while len(set(poslv_2)) < 2:
    seq = list(graph.neighbors(node[0]))
    random.shuffle(seq)
    finish_wordes = seq[:2] # первые два слова
    for finish_word in finish_wordes:
      sequence = list(graph.neighbors(finish_word))
      length = random.randint(1, 1)
      random.shuffle(sequence)
      if ' '.join(sequence[:length]) + ' a ' + finish_word == ' a '.join(node):
        pass
      else:
        poslv_2.append(' '.join(sequence[:length]) + ' a ' + finish_word)
  return  poslv_2[:2][0], poslv_2[:2][1], ' a '.join(node)

def three_poslov (file = file, graph = graph):
    all_poslov = find_right_poslov(file, graph)
    return make_poslov(random.choice(all_poslov), graph)
    # make_poslov(['везде скачут,', 'у нас плачут.'], graph)
