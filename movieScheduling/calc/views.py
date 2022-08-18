from django.shortcuts import render
from django.http import HttpResponse
from . import function
# Create your views here.

global D 
D=list()
D2 =list()
global I,I2
I = list()
I2 = list()
global S,S2
S= list()
S2 = list()
global I3
I3=dict()
global LocalLang,number_of_screens,SpecialDays
global schedule
 
def convert(d):
  dic = {}
  for i in d:
    i.pop('csrfmiddlewaretoken')
    #creates a list of values
    values = []
    for j in i:
      for k in i[j]:
         values.append(k)
    dic[values[0]] = {'DemSco': values[1], 'CastW': values[2], 'SRate': values[3], 'RunTime': values[4], 'Feature': values[5], 'Language': values[6]}
  priority={}
  object = function.MovieClass
  for key, values in dic.items():
    movie = object(int(values['DemSco']),int(values['CastW']),int(values['SRate']),int(values['RunTime']),int(values['Feature']),values['Language'],"Tamil")
    priority[key]=movie.priority
  return priority


def home(request):
  global I
  #[{'csrfmiddlewaretoken': ['pnftUYdlurx5O9Q2uEDhsoLd0Mgri1VMPMI1R6V4Fnii8q4pd1yG2OEeGYrH9DfQ'], 'nScreens': ['10'], 'LocalLang': ['Tamil'], 'SpecialDays': ['2']}]
  inp = dict(request.POST)
  print(request.POST)
  I.append(inp)
  print(I)
  return render(request,'home.html')


def first(request):
  global D
  dic=dict(request.POST)
  print(request.POST)
  D.append(dic)
  print(D) #D is a list of dictionaries(input)

  return render(request,'first.html')

def second(request):
  global S
  dic1=dict(request.POST)
  print(request.POST)
  S.append(dic1) 
  print(S) #D is a list of dictionaries(input)
  return render(request,'second.html')



def result(request):
  global D,D2
  global I,I2
  global S
  global S2
  global LocalLang
  global number_of_screens
  global SpecialDays
  SpecialDays=list()
  dic2 = dict(request.POST)
  print(request.POST)
  S.append(dic2)

  D.append(S[0])
  S.pop(0)
  I.append(D[0])
  D.pop(0)

#for nscreens,local_language and special_days
  for i in I:
    I2.append(i)
  print(I2)
  I2.pop(0)
  for i in I2:
    I3 = i
  for key,values in I3.items():
    SpecialDays = []
    if key == 'nScreens':
      number_of_screens = int(values[0])
    elif key == 'LocalLang':
      LocalLang = values[0]
    elif key=='SpecialDays':
      for i in values:
        SpecialDays.append(int(i))
 
    else:
      continue
  print(I3)
    
#for old movies
  for i in D:
    D2.append(i)
  olddic = dict()
  for i in D2:
    i.pop('csrfmiddlewaretoken')
    #creates a list of values
    oldvalues = []
    for j in i:
      for k in i[j]:
         oldvalues.append(k)
    olddic[oldvalues[0]] = {'DemSco': oldvalues[1], 'CastW': oldvalues[2], 'SRate': oldvalues[3], 'RunTime': oldvalues[4], 'Feature': oldvalues[5], 'Language': oldvalues[6]}
  oldpriority={}
  object = function.MovieClass
  for key, values in olddic.items():
    oldmovie = object(int(values['DemSco']),int(values['CastW']),int(values['SRate']),int(values['RunTime']),int(values['Feature']),values['Language'],LocalLang)
    oldpriority[key]=oldmovie.priority




#For new movies
  for i in S:
    S2.append(i)
  dic = {}
  for i in S2:
    i.pop('csrfmiddlewaretoken')
    #creates a list of values
    values = []
    for j in i:
      for k in i[j]:
         values.append(k)
    dic[values[0]] = {'DemSco': values[1], 'CastW': values[2], 'SRate': 5, 'RunTime': 0, 'Feature': values[3], 'Language': values[4]}
  priority={}
  object = function.MovieClass
  for key, values in dic.items():
    movie = object(int(values['DemSco']),int(values['CastW']),int(values['SRate']),int(values['RunTime']),int(values['Feature']),values['Language'],LocalLang)
    priority[key]=movie.priority


  #Making the schedule

  Days = ['0','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

  GenerateSlots= function.GenerateSlots
  scheduling = function.scheduling
  schedule = {}

  for i in range(1, 5):
    if i not in SpecialDays:
        p_movie = GenerateSlots(olddic,oldpriority,number_of_screens, 4)
        scd=scheduling(number_of_screens, p_movie, 2, 5)
    else:
        p_movie = GenerateSlots(olddic,oldpriority,number_of_screens, 6)
        scd=scheduling(number_of_screens, p_movie, 1, 6)
    
    schedule[Days[i]] =scd

  for i in range(5, 8):
    olddic.update(dic)
    oldpriority.update(priority)

    if i not in SpecialDays:
        if i == 5:
            p_movie = GenerateSlots(olddic,oldpriority,number_of_screens, 4)
            scd=scheduling(number_of_screens, p_movie, 2, 5)
        else:
            p_movie = GenerateSlots(olddic,oldpriority,number_of_screens, 5)
            scd=scheduling(number_of_screens, p_movie, 2, 6)
    else:
        p_movie = GenerateSlots(olddic,oldpriority,number_of_screens, 6)
        scd=scheduling(number_of_screens, p_movie, 1, 6)
    schedule[Days[i]]=scd

  print(schedule)
      



  return render(request,'result.html',{'schedule':schedule})
