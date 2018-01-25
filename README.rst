Formalus teikiamų ir pageidaujamų atvirų duomenų aprašymo formatas
==================================================================

Šio projekto tikslas dokumentuoti vieną iš variantų, kaip formaliai aprašyti
teikiamus ir pageidaujamus duomenis, taip, kad tiek duomenų tiekėjai žinotų
koks yra duomenų poreikis, tiek duomenų naudotojai žinotų kokie duomenys
teikiami.

Duomenų aprašymas susideda iš tryjų esminių dalių:

- Bendra duomenų struktūros schema.

- Projektai, kurie naudoja arba naudotų atvirus duomenis.

- Tiekėjai, kurie teikia atvirus duomenis.

Tike naudotojai, tiek tiekėjai, nadodami bendrą duomenų struktūros schemą
aprašo kokių duomenų jiems reikia arba kokie duomenys yra teikiami.

Turinti tokius mašinai ir žmogui perskaitomus formalius aprašus, gali sukurti
eilę priemonių, kurios galėtų atlikti įvairius paskaičiavimus, pavyzdžiui:

- Paskaičiuotų kiek procentų ir kokio brandos lygio duomenis projektas gauna iš
  duomenų tiekėjų.

- Duomenų tiekėjas galėtų matyti kiek projektų naudoja jo teikiamus duomenis ir
  ar yra tam tikrų duomenų, kurių brandos lygis galėtų būti padidintas.

- Būtų galima apskaičiuoti esminius veiklos rodiklius, kurie parodytų kaip
  keičiasi atvirų duomenų branda poreikio tenkinimas laike.

- Turint tokius formalius aprašus ir naudojant bendrą duomenų struktūros
  schemą, galia sukurti automatizuotus įrankius, kurie iš visų tiekėjų galėtų
  surinkti visų projektui reikalingų duomenų paketą ir pateikti duomenis
  projektui tinkamu formatu.

- Bendros schemos naudojimas užtikrintų, kad tarp skirtingų įstaigų būtų
  laikomasi duomenų vientisumo.

- Pateikus nuasmeninimo taisykles bendroje schemoje, galima žymiai
  supaprastinti atveriamų duomenų nuasmeninimą ir automatizuoti šį procesą.

- Iš duomenų tiekėjų aprašų galima atlikti automatinį duomenų užpildymą CKAN ar
  panašioje sistemoje.

- Bendroje schemoje galima pateikti nuorodas į išorines duomenų bazes, tokias
  kaip wikidata ar kitas plačiai naudojomas ontologijas. Tokiu būtu atveriami
  duomenys automatiškai įgaus penktą brandos lygį.


Kad visa tai veiktų, reikėtų įteisinti procesus, kuriais remiantis duomenų
naudotojai galėtų formaliai pateikti prašymą duomenims gauti, o duomenų
tiekėjai turėtų laikytis formalaus duomenų aprašytmo taisyklių atveriant savo
duomenis.


Vienas iš pavyzdžių, kokias ataskaitas galima generuoti naudojantis minėtais
formaliais duomenų aprašais:


.. image:: https://raw.githubusercontent.com/sirex/atviru-duomenu-poreikio-tyrimas/master/reports/sunburst.png
   :height: 638 px
   :width: 850 px
   :alt: Atvirų duomenų progreso sunburst diagrama.
   :align: center
   :target: https://raw.githubusercontent.com/sirex/atviru-duomenu-poreikio-tyrimas/master/reports/sunburst.png


Susijusios nuorodos
-------------------


- `Wikidata duomenų models <https://www.mediawiki.org/wiki/Wikibase/DataModel/Primer>`_

- `Resource Description Framework (RDF) <https://en.wikipedia.org/wiki/Resource_Description_Framework>`_

- `frictionlessdata.io <https://frictionlessdata.io/>`_

- `WordNet <http://wordnetweb.princeton.edu/perl/webwn>`_
