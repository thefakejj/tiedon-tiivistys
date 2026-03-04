# Määrittelydokumentti

## Ohjelmointikieli

- Käytän Pythonia

## Muut kielet mitä hallitsen

- JavaScript

## Algoritmit ja tietorakenteet mitä toteutan

- LZ78
- Huffman-koodaus
- Trie

## Minkä ongelman ratkaisen

- Tekstitiedostojen häviötön pakkaus tehokkaasti

## Mitä syötteitä ohjelma saa

- Tekstitiedoston

## Aikavaatimukset ja tilavaativuudet

LZ78:

- aika: O(n) (Olettaen että hashmapissa haku on O(1))
- tila: O(n)

Huffman:

- aika: O(nlogn) (priority queueen lisääminen vaatii logn aikaa)
- tila: O(n)

## Lähteitä

- https://en.wikipedia.org/wiki/LZ77_and_LZ78#LZ78

- https://www.geeksforgeeks.org/dsa/huffman-coding-greedy-algo-3/
- https://en.wikipedia.org/wiki/Huffman_coding

Näistä videoista oli paljon hyötyä

- LZ78: https://youtu.be/LPFtaEy3gMA?si=iU_l7fVOBkX7MU5C
- Huffman: https://youtu.be/iEm1NRyEe5c?si=kFAwrlcMHp3XEP2L

- https://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree

# HARJOITUSTYÖN YDIN

Harjoitustyön ytimenä on toteuttaa tekstitiedostojen tehokkaita pakkausalgoritmeja, ja pakata teksitiedostoja käyttäen niitä. Tarkoituksena on myös verrata algoritmien pakkaustehoja keskenään.

## Koulutusohjelma

Tietojenkäsittelytieteen kandidaatti (Suomi)
