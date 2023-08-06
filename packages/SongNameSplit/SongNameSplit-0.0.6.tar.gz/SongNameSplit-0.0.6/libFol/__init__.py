class NonStandardSongTitle(Exception):
    pass

class InternetConnectionError(Exception):
    pass

def junkRmv(inputName):
    fname = list(inputName)
    songname = ''
    hyphc = 0
    for i in range(len(fname)):
        if fname[i] == '(' or fname[i] == '{' or fname[i] == '|' or fname[i] == '[':
            break
        if fname[i] == '-':
            hyphc += 1
        if fname[i] == '-' and hyphc == 2:
            break
        songname += str(fname[i])
    
    return songname


def artist_match_check(query):
  from googlesearch import search
  from bs4 import BeautifulSoup
  import requests
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

  aprvList = ["singer", "creator", "artist", "sing", "sings", "singing"]

  for j in search(query, num=5, stop=5, pause=2):
      res = requests.get(j)
      html_page = res.content
      soup = BeautifulSoup(html_page, 'html.parser')
      text = soup.find_all(text=True)
      output = ''
      for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
      outL = output.split()
      for word in outL:
        for apC in aprvList:
          if word.lower() == apC.lower():
            artistC += 1

  return artistC


def namesplit(inpTitle):
    songtitle = junkRmv(inpTitle)

    songL = songtitle.split()

    if '-' in songL:
        prt1 = songL[:songL.index('-')]
        prt2 = songL[songL.index('-')+1:]
        p1j = ' '.join(prt1)
        p2j = ' '.join(prt2)
        print(p1j, '|', p2j)


    elif '|' in songL:
        prt1 = songL[:songL.index('-')]
        prt2 = songL[songL.index('-')+1:]
        p1j = ' '.join(prt1)
        p2j = ' '.join(prt2)
        print(p1j, '|', p2j)

    else:
        raise NonStandardSongTitle

    try:
    
        p1Points = artist_match_check(p1j)
        p2Points = artist_match_check(p2j)

    except:
        raise InternetConnectionError

    if p1Points >= p2Points:
        rtDic = {'artist': p1j, 'songname': p2j}
        return rtDic

    else:
        rtDic = {'artist': p2j, 'songname': p1j}
        return rtDic




