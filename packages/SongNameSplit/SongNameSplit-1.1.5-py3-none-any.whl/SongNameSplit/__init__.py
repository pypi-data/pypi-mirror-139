from os import pipe
class NonStandardSongTitle(Exception):
    pass

class InternetConnectionError(Exception):
    pass



def junkRmv(inputName):

    print("----- SongNameSplit v 1.1.3 -----")

    fname = list(inputName)
    songname = ''
    hyphc = 0

    print("Running basic logic tests...")

    for i in range(len(fname)):


        if fname[i] == '(' or fname[i] == '{' or fname[i] == '|' or fname[i] == '[':
            break

        if fname[i] == '-':
            hyphc += 1

        if fname[i] == '-' and hyphc == 2:
            break
        
        songname += str(fname[i])

    print("Done. Moving on.")    
    
    return songname


def artist_match_check(query, runNum):

  from googlesearch import search
  from bs4 import BeautifulSoup
  import requests
  import string


  blacklist = [
      '[document]',
      'noscript',
      'header',
      'html',
      'meta',
      'head', 
      'input',
      'script',
      'style'
  ]

  artistC = 0

  aprvList = ["singer", "creator", "artist", "sing", "sings", "singing", "band"]

  bNum = 0

  print("---")

  for j in search(query, num = runNum, stop = runNum, pause = 2):

      bNum += 1

      res = requests.get(j)
      html_page = res.content
      soup = BeautifulSoup(html_page, 'html.parser')
      text = soup.find_all(text=True)

      output = ''


      for t in text:

        if t.parent.name not in blacklist:
            output += '{} '.format(t)

      print("Working on it... ", bNum, "/", runNum)
      outL = output.split()

      for word in outL:
        for apC in aprvList:

          if (word.lower()).translate(str.maketrans('', '', string.punctuation)) == (apC.lower()).translate(str.maketrans('', '', string.punctuation)):
            artistC += 1
  print("---")
  return artistC


def namesplit(inpTitle):

    songtitle = junkRmv(inpTitle)

    songL = songtitle.split()

    ftlist = ['ft', 'ft.', 'feat', 'feat.', 'featuring', 'featuring.', 'Ft', 'Ft.', 'Feat', 'Feat.', 'Featuring', 'Featuring.', 'FEAT', 'FT', 'FEAT.', 'FT.', 'FEATURING', 'FEATURING.']

    print("Starting Level 2 tests")

    if '|' in songL and '-' in songL:


        prt1 = songL[:songL.index('-')]
        prt2 = songL[songL.index('|')+1:]

        p1j = ' '.join(prt1)
        p2j = ' '.join(prt2)

        for feat in ftlist:
          if feat in songL:
            prt2 = songL[songL.index('-')+1:songL.index(feat)]
            p2j = ' '.join(prt2)
            break

        print("Valid Test Found")

    elif '-' in songL:

        prt1 = songL[:songL.index('-')]
        prt2 = songL[songL.index('-')+1:]

        p1j = ' '.join(prt1)
        p2j = ' '.join(prt2)

        for feat in ftlist:
          if feat in songL:
            prt2 = songL[songL.index('-')+1:songL.index(feat)]
            p2j = ' '.join(prt2)
            break

        print("Valid Test Found")

    elif '~' in songL:

        prt1 = songL[:songL.index('~')]
        prt2 = songL[songL.index('~')+1:]

        p1j = ' '.join(prt1)
        p2j = ' '.join(prt2)

        for feat in ftlist:
          if feat in songL:
            prt2 = songL[songL.index('~')+1:songL.index(feat)]
            p2j = ' '.join(prt2)
            break

        print("Valid Test Found")

    elif '|' in songL:

        prt1 = songL[:songL.index('|')]
        prt2 = songL[songL.index('|')+1:]

        p1j = ' '.join(prt1)
        p2j = ' '.join(prt2)

        for feat in ftlist:
          if feat in songL:
            prt2 = songL[songL.index('|')+1:songL.index(feat)]
            p2j = ' '.join(prt2)
            break

        print("Valid Test Found")

    else:
        raise NonStandardSongTitle

    try:

        print("Starting final level tests")

        p1Points = artist_match_check(p1j, 3)
        p2Points = artist_match_check(p2j, 3)

    except:
        raise InternetConnectionError

    if abs(p1Points - p2Points) <= 10:

      print("Low accuracy predicted. Attempting to double the accuracy.")

      try:
      
          p1Points = artist_match_check(p1j, 6)
          p2Points = artist_match_check(p2j, 6)

      except:
          raise InternetConnectionError

    if p1Points >= p2Points:

        rtDic = {'artist': p1j, 'songname': p2j}

        print("Tests Successfully Concluded.")
        print("-----------------------------------")

        return rtDic

    else:

        rtDic = {'artist': p2j, 'songname': p1j}

        print("Tests Successfully Concluded.")
        print("-----------------------------------")

        return rtDic
