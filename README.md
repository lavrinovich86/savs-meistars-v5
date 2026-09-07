# SAVS meistars — versija 05 / Rasējumu darbvirsma

Atveriet `index.html` pārlūkā. Nav vajadzīga instalēšana vai būvēšana; visi fonti, attēli un rasējumi ir lokāli. Šī versija ir patstāvīga; iepriekšējās mapes nav mainītas.

Publicēts: https://lavrinovich86.github.io/savs-meistars-v5/

## Dizains

Tumša CAD darbvirsma: koordinātu režģis, plāna līniju grafika un slāņu krāsu sistēma, kur katrai inženiersistēmai ir sava krāsa — arhitektūra balta, jumta elementi pelēki, saules paneļi ciāna, elektroietaise dzeltena, izmēri zaļi. Tā pati krāsa atkārtojas rasējumā, slāņu panelī un apzīmējumos, tāpēc panelis ir arī leģenda.

Slāņi ir **uzklājami**: katrs slēdzis pievieno vai noņem savu slāni virsū pārējiem, nevis pārslēdz skatu. Visi slāņi ir redzami arī tad, ja JavaScript neielādējas.

Fonti: IBM Plex Sans tekstam un IBM Plex Mono rasējumu anotācijām, kodiem un rakstlaukumam. Licence: `assets/Plex-OFL.txt`.

## Rasējumi

Trīs rasējumi, visi veidoti ar kodu kā SVG:

| Lapa | Saturs | Avots |
|---|---|---|
| A-101 | Jumta plāns ar saules paneļu masīvu un elektroietaises trasēm | pasūtītāja iesniegtais aerofoto |
| A-201 | Fasāde, dienvidrietumu skats | pasūtītāja iesniegtais zemes līmeņa foto |
| E-301 | Tipveida principiālā elektroshēma | nozares tipveida risinājums |

**Svarīgi par avotiem.** Abi foto ir no dažādiem laikiem. Aerofoto uz dienvidu nogāzēm ir saules paneļu masīvs; zemes līmeņa foto ir agrāks, un tajā paneļu vēl nav — redzams metāla dakstiņu segums un ķieģeļu mūris. Tāpēc jumta plāns rāda paneļus, bet fasāde ne. Lapā šī atšķirība ir norādīta pie attiecīgā rasējuma.

Rasējumi ir **koncepta ilustrācijas**, nevis būvprojekts, uzmērījums vai tehniskā dokumentācija:

- korpusu proporcijas nolasītas no attēliem, bet visi izmēri un augstumi ir **pieņemti**, nevis uzmērīti;
- paneļu skaits (58) ir **novērtējums pēc aerofoto**, ne inventarizācija;
- elektroshēma ir **tipveida** — tā parāda risinājuma uzbūvi, nevis konkrētās ēkas projektu. Aizsardzības aparāti, kabeļu šķērsgriezumi un grupu skaits nosakāmi projektā un saskaņojami ar tīkla operatoru;
- rasējumos nav adreses, zemes robežu vai koordinātu.

Aerofoto un zemes līmeņa foto lapā **nav iekļauti** — tikai pēc tiem zīmētie rasējumi. Attēli ir trešo pušu kartogrāfijas materiāls, un to publicēšana būtu atsevišķs jautājums.

## Rasējumu ģenerēšana

`tools/drawings.py` aprēķina ģeometriju un izvada SVG fragmentu. Paneļu režģis tiek apgriezts pie jumta šļauktnēm un ap jumta logiem un skursteni, tāpēc masīva mala seko jumta formai.

```
python3 tools/drawings.py roof     # jumta plāns
python3 tools/drawings.py elev     # fasāde
python3 tools/build.py             # ievieto abus index.src.html -> index.html
```

Rediģē `index.src.html`, nevis `index.html`. Pēdējo pārraksta `tools/build.py`.

## Saturs un kontakti

Uzņēmuma dati pārņemti no pirmās versijas pārbaudītajiem avotiem:

- https://www.profymarket.com/companies/savs-meistars — adrese, reģistrācijas numurs, darbības sfēras, būvkomersanta reģistrācija 10.08.2012., Nr. 10000-R. Profila datu atjaunināšanas datums: 01.01.2024.
- https://www.facebook.com/AAreklama/posts/3903228599762014/ — pasūtītāja norādītais auto foto un logo vizuālā atsauce.
- Tālrunis +371 29 354 519, e-pasts info@savs.lv. Pirms publicēšanas uzņēmumam jāapstiprina aktualitāte.

Logo ir pirmās versijas SVG rekonstrukcija pēc auto foto. Darba procesa un zīmola teksti ir redakcionāls priekšlikums uzņēmumam.

## Forma

Pakalpojuma karte automātiski izvēlas attiecīgo pakalpojumu formā. Forma pārbauda nepieciešamos laukus un atver sagatavotu `mailto:` vēstuli apmeklētāja e-pasta programmā. Dati netiek sūtīti uz serveri vai glabāti.

## Pārbaudes

`node --check app.js` pārbauda JavaScript sintaksi. Priekšskati `desktop-preview.png` (1425 px) un `mobile-preview.png` (390 px) uzņemti ar Chromium bezgalvas režīmā no lokāla servera.

`robots.txt` un `<meta name="robots">` tur lapu ārpus meklētājiem, jo tajā ir uzņēmuma īstie kontakti un tā vēl nav apstiprināta publiskošanai.
