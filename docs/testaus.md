Testikattavuus (4.3.2026)
![Coverage report. src/huffman.py 99% test coverage. src/lz.py 99% test coverage. 99% Total test coverage.](test_coverage.png)

Pakkaustehon vertailu

Testidatana War and Peace vähemmällä whitespacella, suurin versio noin 3MB. Tässä versiossa edelleen sisennys tehdään välilyönnillä, mikä suosii huffman-algoritmia.

Testaus on tehty tämän rivin kirjoituksen aikaisen commitin main-tiedostossa olevilla käskyillä. Molemmilla algoritmeilla on tarkistettu pakkaamisen oikeellisuus vertailun yhteydessä.

### 1kB

- lz78 100.67%

- huffman: 63.12%

### 4kB

- lz78: 82.26%

- huffman: 58.25%

### 16kB

- lz78: 67.61%

- huffman: 56.97%

### 64kB

- lz78: 61.08%

- huffman: 56.49%

### 256kB

- lz78: 59.94%

- huffman: 56.31%

### 1MB

- lz78: 59.93%

- huffman: 56.26%

### 2MB

- lz78: 59.97%

- huffman: 56.17%

### 3MB

- lz78: 59.97%

- huffman: 56.02%


Tämän vertailun tuloksena on se, että Huffman-koodaus on tälle syötteelle tehokkaampi pakkaustapa kuin LZ78.

Molemmilla algoritmeilla pakkausteho paranee mitä suurempaan tiedostoon siirrytään. 16kB tiedostossa saadaan LZ78-algoritmilla hieman yli 4096 riviä tauluun, minkä jälkeen uusia yhdistelmiä ei enää etsitä. Luultavasti tämän takia pakkausteho ei kasva huomattavasti 16kB suuremmilla tiedostoilla, kun käytetään LZ78-algoritmia.
