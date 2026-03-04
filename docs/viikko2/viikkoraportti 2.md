### Mitä olen tehnyt tällä viikolla?

Koodasin molemmat algoritmit alkuun ja tietty tämän yhteydessä syvennyin niihin. Tällä viikolla ollut muita kiireisiä palautuksia jotka on vienyt aikaa. Ensi viikon jälkeen tämän pitäisi hellittää.

### Miten ohjelma on edistynyt?

Ehkä hieman hitaasti.

Ohjelmoin huffman-algoritmin kohdalla metodit, jotka muodostaa biteistä koostuvan merkkijonon ja kykenee muuttamaan tämän merkkijonon takaisin tekstiksi.

LZ78:n taas olen saanut alkuun, mutta tästä mietin että toimiiko algo oikein? main.py:ssä on pari esimerkkiä lz:n käytöstä ja se tulostaa seuraavan:

{'A': 1, 'B': 2, 'R': 3, '1C': 4, '1D': 5, '1B': 6, '3A': 7, '7B': 8, '1R': 9, '6A': 10, '7EOF': 11}
{'A': 1, 'B': 2, 'R': 3, '1C': 4, '1D': 5, '1B': 6, '3A': 7, '7B': 8, '1R': 9, 'E': 10, '6A': 11, '7E': 12, 'EOF': 13}

Onko jälkimmäinen esimerkki oikein? (syötteessä viimeinen merkki on uusi merkki)

### Mitä opin tällä viikolla / tänään?

Käytännön toteutus auttaa ymmärtämään algoritmeja paremmin. Myös terve muistutus siitä, miten käytännön toteutuksessa tiedon tallentaminen ja lukeminen vaatii tarkoituksellista tietorakenteiden käyttöä. :D

### Mikä jäi epäselväksi tai tuottanut vaikeuksia?

Yllä mainittu kysymys LZ78:sta. Samalla epäselväksi jäänyt bittien tallentaminen pythonissa, mutta tähän olen saanut joitain vinkkejä joihin tutustun... Myös mainittakoon, että tarvitsenko kaikki huffmanissa käyttämäni tietorakenteet? Tallennan kaksi sanakirjaa. (key: code ja code: key)

### Mitä teen seuraavaksi?

Varmaankin pyrin tallentamaan huffman-koodauksen tekstistä bitteinä tiedostoon.
