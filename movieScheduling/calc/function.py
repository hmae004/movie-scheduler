import random
class MovieClass:
    def __init__(self, demand_score, cast_weight, success_rate,
                 time_running, feature, language,local_language):

        # defining characteristics of movie
        
        self.demand_score = demand_score
        self.cast_weight = cast_weight
        self.success_rate = success_rate
        self.priority = (demand_score + cast_weight + success_rate) / 2
        self.feature = feature
        self.language = language
        self.local_language = local_language

        # Determining priority based on success rate
        self.rate = (self.success_rate / 5) * 100
        if 20 < self.rate <= 50:
            self.priority /= 2
        if self.rate <= 20:
            self.priority = 0

        # determining priority based on time running
        self.time_running = time_running
        if 0 <= self.time_running <= 1:
            self.priority = self.priority
        elif 1 < self.time_running <= 2:
            self.priority *= 0.75
        elif 2 < self.time_running <= 3:
            self.priority *= 0.5
        elif 3 < self.time_running <= 4:
            self.priority *= 0.25
        else:
            self.priority = 0

        # determining feature based on features
        self.feature = feature
        if feature == 1:
            self.priority += 0.5
        elif feature == 2:
            self.priority += 0.5
        elif feature == 3:
            self.priority += 0.75
        else:
            self.priority = self.priority

        if language.lower() != local_language.lower():
            self.priority *= 0.25
        else:
            self.priority = self.priority





def display_table(schedule):
    myTable = PrettyTable(
        ['Screens', 'Slot1', 'Slot2', 'Slot3', 'Slot4', 'Slot5', 'Slot6'])
    for i in schedule:
        myTable.add_row([
            i, schedule[i]['Slot1'], schedule[i]['Slot2'],
            schedule[i]['Slot3'], schedule[i]['Slot4'], schedule[i]['Slot5'],
            schedule[i]['Slot6']
        ])
    print(myTable)



'''FIRST TIER: GENERATING NUMBER OF SHOWS PER MOVIE ACCORDING TO PRIORITY'''


def GenerateSlots(Details,Movie,number_of_screens, nslots):

  #sorting the {moviename:priority} dictionary
  d = (dict(sorted(Movie.items(), key=lambda item: item[1])))

  #inverting the {moviename:priority} dictionary to find movies with the same priority
  inverse = dict()
  for key in d:
      val = d[key]
      if val not in inverse:
          inverse[val] = [key]
      else:
          inverse[val].append(key)

  
  #sorting movies with the same priority. Movies in decreasing order of priority appeneded to list movies_f
  movies_f = list()
  for i in inverse:
      if len(inverse[i]) == 1:
          movies_f.append(inverse[i][0])
      else:
          compare = dict()
          for j in inverse[i]:
              compare[j] = (Details[j]['DemSco'], Details[j]['CastW'],Details[j]['SRate'], Details[j]['RunTime'])
          y = (dict(sorted(compare.items(), key=lambda item: item[1])))
          for i in y:
            movies_f.append(i)
  movies_f = movies_f[::-1]

  #determining percentage of showtimes per movie
  n = len(movies_f)
  assert isinstance(n, int) and n > 0
  temp = [x / sum(range(n + 1)) * 100 for x in range(1, n + 1)]
  temp = temp[::-1]
  #determing number in shows per movie, according to priority. Dictionary p_movie in the form {MovieName: NumberOfShows} is returned.
  p_movie = dict()
  j = 0
  for i in movies_f:
      p_movie[i] = round(temp[j] / 100 * (nslots * number_of_screens))
      j += 1

  p_movieList = list()
  for key in p_movie:
      p_movieList.append(key)

  total_no_showtimes = number_of_screens * nslots
  no_shows_alloted = sum(p_movie.values())
  excess_shows = no_shows_alloted - total_no_showtimes
  for i in range(len(p_movieList) - 1, -1, -1):
      if excess_shows > 0:
          if excess_shows > p_movie[p_movieList[i]]:
              t = p_movie[p_movieList[i]]
              p_movie[p_movieList[i]] = 0
              excess_shows -= t
          else:
              p_movie[p_movieList[i]] -= excess_shows
              excess_shows = 0
  return p_movie



'''SECOND TIER: MAIN SCHEDULING PROBLEM'''


def scheduling(number_of_screens, p_movie, l, u):

  Slots = ['Slot1', 'Slot2', 'Slot3', 'Slot4', 'Slot5', 'Slot6']

  Screens = list()
  for i in range(number_of_screens):
      screen = 'Screen' + str(i + 1)
      Screens.append(screen)

  schedule = dict()
  for i in range(number_of_screens):
      schedule[Screens[i]] = {
          'Slot1': '-',
          'Slot2': '-',
          'Slot3': '-',
          'Slot4': '-',
          'Slot5': '-',
          'Slot6': '-'
      }

  #Movie list generated where movies are arranged in decreasing order of number of shows
  p_movieList = list()
  for key in p_movie:
      p_movieList.append(key)

  #Prime slots determined depending on the number of slots per day
  prime_slots = list()
  if l == 2 and u == 5:
      prime_slots = ['Slot4', 'Slot5']
  if l == 2 and u == 6:
      prime_slots = ['Slot5', 'Slot6']
  if l == 1 and u == 6:
      prime_slots = ['Slot1', 'Slot5', 'Slot6']

  #High priority movies scheduled first according to number of prime showtimes
  number_of_prime_showtimes = number_of_screens * len(prime_slots)
  i = 0
  j = 0
  for key in p_movieList:
      while i < p_movie[key] and j != number_of_prime_showtimes:
          SlotName = random.choice(prime_slots)
          randomscreen = random.randint(0, number_of_screens - 1)
          ScreenName = Screens[randomscreen]
          if schedule[ScreenName][SlotName] == '-':
              schedule[ScreenName][SlotName] = key
              i += 1
              j += 1
          else:
              continue
      if i == p_movie[key]:
          del p_movie[key]
      else:
          p_movie[key] -= i
      i = 0
  i = 0

  #Other movies scheduled in remaining slot times
  for key in p_movie:
      while i < p_movie[key]:
          randomslot = random.randint(l - 1, u - 1)
          SlotName = Slots[randomslot]
          randomscreen = random.randint(0, number_of_screens - 1)
          ScreenName = Screens[randomscreen]
          if schedule[ScreenName][SlotName] == '-':
              schedule[ScreenName][SlotName] = key
              i += 1
          else:
              continue
      i = 0

  return schedule
