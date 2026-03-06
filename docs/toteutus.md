# Toteutusdokumentti

## Ohjelman rakenne

### main.py

Mainissa ohjelma saa polut luettavalle tekstitiedostolle ja pakatulle binääritiedostolle joka luodaan. Lisäksi mainissa luetaan tekstitiedosto.

Mainin tehtävänä on kutsua enkoodaus- ja dekoodausmetodeja, antaen niille argumenttina luetun tiedoston tavuina ja binääritiedoston polun.

### lz.py

[LZ78 wikipedia](https://en.wikipedia.org/wiki/LZ77_and_LZ78#LZ78)

#### Enkoodauksessa toimitaan seuraavasti:

Taulun luominen -> Taulu binäärimerkkijonoksi -> Tallennetaan binäärimerkkijono tiedostoon

Taulun luomisessa jo tunnettujen merkkijonojen tallentamiseen ja löytämiseen käytetään [trie](https://en.wikipedia.org/wiki/Trie)-tietorakennetta.

Aikavaativuuksia

- Search: O(n), missä n on avaimen pituus
- Insert: O(n), missä n on avaimen pituus
- Create table: O(nlogn), missä n on tekstin pituus

Tilavaativuuksia

- Trie: O(n), missä n on tekstin pituus
- LZ78-taulu: O(m), missä m on taulun rivien määrä

#### Dekoodaukseussa toimitaan seuraavasti:

Luetaan tiedostosta binäärimerkkijono tavuina -> Muokataan tavut binäärimerkkijonoksi -> Luodaan taulu binäärimerkkijonosta -> Luodaan alkuperäinen merkkijono taulusta

- Dekoodauksessa aikavaativuus on O(n), missä n on tavujen määrä pakatussa tiedostossa

### huffman.py

[Huffman coding gfg](https://www.geeksforgeeks.org/dsa/huffman-coding-greedy-algo-3/) <- puun muodostaminen priority queuella

[Huffman coding wikipedia](https://en.wikipedia.org/wiki/Huffman_coding) <- aikavaativuuksia

[Huffman-puun tallentaminen binäärinä
](https://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree)

#### Enkoodauksessa toimitaan seuraavasti:

Frequency table luominen -> Huffman-puun luominen -> Huffman-koodien luominen merkeille -> teskstin tavut binäärimerkkijonoksi -> Huffman-puu biteiksi -> tallennetaan Huffman-puu ja teksti pakattuun tiedostoon tavuina

Aikavaativuuksia

- Frequency table luominen: O(n), missä n on tekstin pituus (hashmap käytössä)
- Huffman-puun luominen: O(nlogn) missä n on eri merkkien määrä
- Huffman-koodien asettaminen merkeille: O(n), missä n on solmujen määrä puussa
- Teksti binääriksi: O(n), missä n on tekstin pituus
- Puu binääriksi: O(n), missä n on solmujen määrä

Tilavaativuuksia

- Frequency table: O(m), missä m uniikkien merkkien määrä
- Huffman-puu: O(m), missä m on uniikkien merkkien määrä

#### Dekoodaukseussa toimitaan seuraavasti:

Luetaan tiedosto tavuina -> muokataan tavut biteiksi -> luodaan Huffman-puu biteistä -> luodaan sanakirja merkeille puun avulla -> muodostetaan teksti viimeisistä biteistä sanakirjalla

Aikavaativuuksia

- Puun luominen biteistä: O(n), missä n on puun solmujen määrä
- Sanakirjan luominen merkeille: O(n), missä n on solmujen määrä puussa
- Merkkijonon muodostaminen biteistä: O(n), missä n on bittien määrä

## Puutteet ja parannukset

Ohjelmasta olisi käytännöllisempi käyttöliittymän kanssa. Minulla on visio komentorivikäyttöliittymästä, johon voi kirjoittaa pakattavaksi laitettavan tiedoston polun, ja kenties pakatun tiedoston polun. Voisin myös tehdä hakemiston, johon tallennetaan pakattavia tiedostoja, joista käyttäjä voi valita pakattavaksi jonkun syöttämällä sitä vastaavan numeron.

## Laajojoen kielimallien käyttö

Käytin ChatGPT:tä muuttujanimien luomiselle testitiedostoille huffman_test.py ja lz_test.py -tiedostoihin.
