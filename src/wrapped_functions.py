from urllib.request import urlopen
import mechanize
import re
import numpy as np
from collections import Counter
import time
import string
from unidecode import unidecode

#scrape data from ao3
def openLink(link, user, pwd):
  isOpen = False
  while not isOpen:
    try:
      br = mechanize.Browser()
      br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
      br.open(link)

      br.select_form(id = "new_user_session_small")
      br["user[login]"] = user
      br["user[password]"] = pwd

      response = br.submit()
      isOpen = True
    except:
      print("Too many request, waiting for a bit and retry it...")
      time.sleep(120)

  myfile = response.get_data()

  br.close()
  time.sleep(2)

  return myfile

def findTop(a, nb):
  a = list(np.concatenate(a).flat)
  c= Counter(a)
  if len(a)> nb:
    return c.most_common(nb)
  else:
    return c.most_common()

def findTopAuthor(a, nb):
  a = list(np.concatenate(a).flat)
  a = list(filter(lambda x:x.lower() != 'anonymous' and x != "orphan_account", a))
  c= Counter(a)
  if len(a)> nb:
    return c.most_common(nb)
  else:
    return c.most_common()

def findTopTags(a, nb):
  a = list(np.concatenate(a).flat)
  a = list(filter(lambda x:x != 'AO3 Tags - Freeform', a))
  c= Counter(a)
  if len(a)> nb:
    return c.most_common(nb)
  else:
    return c.most_common()

### Different comments
def commentRating(favR):
  if favR == 'Explicit':
    com = "no judging."
  elif favR == 'Mature':
    com = "good for you!"
  elif favR == 'Teen And Up Audiences':
    com = "Jesus is proud."
  elif favR == 'General Audiences':
    com = "very vanilla of you."
  elif favR == 'Not Rated':
    com = "how???"
  else:
    com = "I'm not sure what to say."
  return com

def commentWords(wordsTot):
  if wordsTot < 50000:
    com= "Not much of a reader, are you?"
  elif wordsTot < 120000:
    com= "That's equivalent to a whole novel!"
  elif wordsTot < 250000:
    com= "That's almost Crime and Punishment!"
  elif wordsTot < 320000:
    com= "Look at that, that could be a A Song of Ice and Fire book!"
  elif wordsTot < 450000:
    com= "You've almost finished the Earthsea series!"
  elif wordsTot < 600000:
    com= "That's almost the equivalent of the Lord of the Ring series!"
  elif wordsTot < 1000000:
    com= "That's almost the equivalent of the first three Stormlight Archive books!"
  elif wordsTot < 1800000:
    com= "That's almost the equivalent of the Song of Ice & Fire series!"
  elif wordsTot < 4400000:
    com= "That's almost the equivalent of the Wheel of Time!"
  elif wordsTot < 14000000:
    com= "That's more than the Wheel of Time!"
  else:
    com= "Wow, that's more than the Wandering Inn!"
  return com

def commentLength(l):
  if l < 5000:
    com = "You're more of a short story kind of person."
  elif l < 50000:
    com = "Not bad, that's the average length of a novellas!"
  elif l < 100000:
    com = "That's basically the length of one of the Golden Compass!"
  elif l < 200000:
    com = "Good job, you've bascially read the Iliad!"
  else:
    com = "Wow... this one is longer than your average novel!"
  return com

def commentTrope(trope):
  if trope == 'Alternate Universe':
     com = "Let's escape canon for a second."
  elif trope == 'Fluff':
    com = "We all need our daily dose of sugar."
  elif trope == 'Angst':
    com = "...Are you okay friend?"
  elif trope == 'Sexual Content' or trope == 'Sex' or trope =='Smut' or trope == 'Anal Sex':
    com = "Bonk??"
  elif trope == 'Hurt/Comfort':
    com = "... emphasis on /Comfort/."
  elif trope == 'Humor' or trope == 'Crack':
     com = "Better laugh than cry, right?"
  elif trope == 'Established Relationship':
     com = "Ah yes, we love the domesticity."
  elif trope == 'One Shot':
     com = "Make it short!"
  elif trope == 'Slow burn' or trope =='Pining':
     com = "Nothing like this delicious torture."
  elif trope == 'Happy Ending' or trope =='Angst with a Happy Ending':
     com = "We all need the happy ending."
  elif trope == 'Plot What Plot/Porn Without Plot':
     com = "Who needs plot?"
  elif trope == 'Fluff and Angst' or trope == "Fluff and Smut":
     com = "Because why not both?"
  elif trope == 'Enemies to Lovers':
    com = "Ohhh you wanna kiss me\nso bad."
  elif trope == 'Alternate Universe - College/University' or trope =="University" or trope =="Canon Compliant":
    com = "An entire world of fiction,\nand this is where you go."
  elif trope == 'Alpha/Beta/Omega Dynamics':
     com = "There are two wolves inside you, \nand they like it there."
  else:
    com = "Never gets old."
  return com

def splitString(a, maxl):
  i = maxl
  letter = a[i]
  while letter != ' ' or i == 0:
    i = i-1
    letter= a[i]
  if i== 0:
    a = a[:maxl-2] + "..\n" + a[maxl-2:]
  else:
    a = a[:i] + "\n" + a[i:]
  if len(a) > 2*maxl:
    i = 2*maxl
    letter = a[i]
    while letter != ' ' or i == maxl:
      i = i-1
      letter= a[i]
    if i == maxl:
      a = a[:2*maxl-2] + "..\n" + a[2*maxl-2:]
    else:
      a = a[:i] + "\n" + a[i:]
  return a

def displayNum(n):
  return f'{n:,}'

def toEnglish(a):
  a = unidecode(a)
  return a

def splitFandom(a):

  return(a.replace(' | ', ' |\n', 1))

def splitShip(ship):
  try:
    i = ship.index('/')
  except:
    i = ship.index('&')
  return toEnglish(ship[:i+1]) + '\n' + toEnglish(ship[i+1:])

def splitAU(AU):
  i = AU.index('-')
  return AU[:i+1] + '\n' + AU[i+1:]