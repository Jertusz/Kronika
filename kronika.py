from requests import get
from bs4 import BeautifulSoup
import docx
import os


niepotrzebne = ['© Copyright 2018 - Zespół Szkół Łączności w Gdańsku','Podwale Staromiejskie 51/52, 80-845 Gdańsk','58 301 13 77','58 308 01 00']
errory = []

def raw(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    akt = html_soup.find_all('div', class_='nicdark_small_news')
    return akt

def tworze(blok, tytul, z):
    doc = docx.Document('wzor.docx')
    elo = blok.div.div.h3
    naglowek = elo.text
    print(naglowek)
    doc.add_paragraph(naglowek).style = 'kron'
    for a in elo.find_all('a', href=True):
        link = a['href']
        url_akt = 'http://www.zsl.gda.pl' + link
        odp = get(url_akt)
        zupa = BeautifulSoup(odp.text, 'html.parser')
        div2 = zupa.find_all('p')
        for i in div2:
            if i.text not in niepotrzebne:
                zaw = i.text
                doc.add_paragraph(zaw).style = 'krot'
    for src in blok.div.div.find_all('img', class_='nicdark_section', src=True):
        tmp = 'http://www.zsl.gda.pl' + src['src']
        obrazek(tmp)
        doc.add_picture('tmp.png')
    #zapisuje plik z uwzglednieniem mozliwych bledow, zapisuje je do error loga
    try:
        doc.save('C:\\kronika\\' + tytul + '.docx')
    except:
        doc.save('C:\\kronika\\%s.docx' % z)
        errory.append(tytul)

def obrazek(tmp):
    png = get(tmp)
    with open('tmp.png', 'wb') as f:
        f.write(png.content)
    return

def dzialanie(x, z):
    for i in range(x, -1, -9):
        url = 'http://www.zsl.gda.pl/aktualnosci/?start=%s' % i
        akt = raw(url)
        for blok in reversed(akt):
            #sprawdzam czy plik istnieje
            elo = blok.div.div.h3
            naglowek_tmp = elo.text
            tytul = str(z) + ' - ' + naglowek_tmp
            tytul = str(tytul)
            if (os.path.isfile('C:\\kronika\\%s.docx' % tytul)):
                print('plik juz istnieje')
            else:
            #tworze dokument i uzupełniam treść
                tworze(blok, tytul, z)
            z = z + 1
        print(i)

def main():
    z = 0
    if not os.path.exists('var.txt'):
        print("Sprawdzam ilosc newsow...")
        print("To moze chwile potrwac...")
        i = 0
        while z == 0:
            url = 'http://www.zsl.gda.pl/aktualnosci/?start=%s' % i
            akt = raw(url)
            i += 9
            if akt == []:
                z = 1
                with open('var.txt','w') as g:
                    g.write(str(i))
    with open('var.txt', 'r') as r:
        i = r.read()
    i = int(i)
    if not os.path.exists('C:\\kronika'):
        os.makedirs('C:\\kronika')
    dzialanie(i, z)
    with open('C:\\kronika\\errorlog.txt','w') as f:
        for blad in errory:
            f.write('%s\n' % blad)
    print('Lista nazw plikow ktore powoduja errory:')
    print("\n".join(errory))
    print('\nLista plikow znajduje sie tez w errorlog.txt\n')
    input("Wcisnij dowolny przycisk zeby zakonczyc")
main()