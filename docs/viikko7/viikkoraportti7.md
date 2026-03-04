### Mitä olen tehnyt tällä viikolla?

Tällä viikolla vertaisarvioinnin jälkeen loin isoja tekstitiedostoja testaamista varten. Tein LZ:n "perustestit", eli niin sanotusti oikeilla syötteillä ohjelman käytön testausta. Sitten ryhdyin bugijahtiin ja muokkasin ohjelman lukemaan tekstitiedostot tavuina. LZ-bugin kanssa kesti todellakin aika pitkään.

### Miten ohjelma on edistynyt?

LZ-bugi vaikuttaa olevan korjattu. Tein myös tutkimukseni perusteella muutamia testitiedostoja, jotka toivottavasti nappaavat jatkossa saman bugin jos se on edelleen olemassa. Tällä hetkellä testit ei toimi, koska tiedon lukeminen on muuttunut. Ei pitäisi olla vaikea korjata. Huom. Käytin lz_test.py -tiedostossa muuttujanimien tuottamiseen chatgpt:tä (Näitä oli aika paljon). Tämä on kommentoitu sinne koodiin.

### Mitä opin tällä viikolla / tänään?

Todella paljon. Newlinen käsittely vaihtelee käyttöjärjestelmän kanssa ja aiheuttaa bugeja. Opin tosiaan, että olen tehnyt LZ-algoritmin väärin ja olen koodannut sen virheiden ympärille paljon. Jne.

### Mikä jäi epäselväksi tai tuottanut vaikeuksia?

Nyt on huomioitavaa se, että ohjelma ei ole valmis. Testejä voisi tehdä vielä lisää ja suurin osa dokumentaatiosta puuttuu. Myös jonkinnäköinen käyttöliittymä voitaisiin lisätä, taikka sitten vain tyhjentää mainia ja tehdä siitä hyödyllinen käyttäjän näkökulmasta. Kirjoitan tästä siksi, että en ole varma onko kurssin läpipääsy vaarassa tällä hetkellä. Joka tapauksessa, aion vain tehdä projektin loppuun.

Kun aloin tekemään pakkaustehotestejä, huomasin, että jo 1MB-4MB tiedostoilla testeissä kestää kohtuuttoman kauan. Useita minuutteja. Tarviiko näitä lisätä ylipäätään automaattiseen testaukseen, vai raportoinko testausdokumenttiin, että tämänlaista tehoa ollaan saatu eri tiedostoilla?

Jos nyt ohjelma lukee tekstitiedoston tavuina, niin pakkaako se ASCII:ta, utf:ää ja muita enkoodaustapoja oikein? Jos näin on, niin miksi aikaisemmin puhuttiin rajauksesta ASCII:hin?

### Mitä teen seuraavaksi?

Korjaan testit huomioimaan uuden tiedon luku- ja tallennustavan. Kirjoitan dokumentit. Muokkaan mainin käyttäjäystävälliseksi. Demoan ohjelmani.
