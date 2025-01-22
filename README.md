# Task Scheduling

## Instalare

Asigurați-vă că aveți Node și Python instalat pe sistem.

1. Package-uri de Node.
```bash
$ npm install
```

2. Package-uri de Python

```bash
$ pip install numpy random datetime tqdm json
```

3. Rulare completă

```bash
$ npm run procesare:completa
```

## Utilizare

Se pot edita totalul de sarcini și VM-uri în `creare-dataset.js`, liniile 8-9.

După afișarea rezultatelor, se pot naviga mașinile cu săgețile de la tastatură (sus / jos). Pentru a naviga între pagini, e nevoie de tastele `CTRL` + `Săgeată dreapta` sau `CTRL` + `Săgeată stânga`.

Pentru a selecta o mașină virtuală și a vedea sarcinile alocate, se poate apăsa tasta `Enter`.

Pentru a naviga înapoi la lista de mașini, se poate apăsa tasta `Backspace`.

În lista de mașini, dacă utilizatorul începe să scrie, se va căuta automat în lista de mașini. `Backspace` pentru ștergerea query-ului de căutare.