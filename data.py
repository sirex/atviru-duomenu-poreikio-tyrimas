import collections


Prop = collections.namedtuple('Prop', (
    'title',
))


def P(title):
    return Prop(title)


class Thing:

    def __getitem__(self, name):
        return getattr(self, name)

    class meta:
        title = None



class Koordinates(Thing):
    ilguma = P("Geografinė ilguma")
    platuma = P("Geografinė platuma")


class Adresas(Thing):
    koordinates = P("Koordinatės", koordinates)
    apskritis = P("Apskritis")
    rajonas = P("Miestas/Rajonas")
    savivaldybe = P("Savivaldybė")
    gatve = P("Gatvė")
    pastato_numeris = P("Pastato numeris")

    class meta:
        title = "Adresas"


class Agentas(Thing):
    pavadinimas = P("Pavadinimas")

    class meta:
        title = "Agentas"


class JuridinisAsmuo(Agentas):
    registracijos_adresas = P("Registracijos adresas")
    teisine_forma = P("teisinė forma")
    pastatas = P("įmonei priklausantis pastatas")
    veiklos_sritis = P("veiklos sritis")
    el_pastas = P("el. paštas")
    tel_nr = P("tel. nr.")
    tinklapis = P("tinklapis")
    darbuotoju_skaicius = P("darbuotojų skaičius")
    vidutinis_atlyginimas = P("vidutinis atlyginimas")
    skola_sodrai = P("skola sodrai")
    apyvarda = P("apyvarta")
    iregistravimo_data = P("įregistravimo data")
    isregistravimo_data = P("išregistravimo data")
    logotipas = P("logotipas")
    akcininkas = P("Įmonės akcininkas")
    direktorius = P("Direktorius")

    class meta:
        title = "Juridinis asmuo"


class Imone(Agentas):

    class meta:
        title = "Įmonė"


class ImoneiPriklausantisPastatas(Adresas):
    darbo_laikas = P("Darbo laikas")

    class meta:
        title = "Įmonei priklausantis pastatas"


class Akcininkas(Agentas):
    akciju_dalis = P("Akcijų dalis įmonėje")

    class meta:
        title = "Akcininkas"


class ValstybineIstaiga(JuridinisAsmuo):
    priklauso_istaigai = P("Valstybinė įstaiga, kuriai yra pavaldi")

    class meta:
        title = "Valstybinė įstaiga"


class Asmuo(Agentas):
    vardas = P("Vardas")
    pavarde = P("Pavardė")
    gimimo_data = P("Gimimo data")
    mirties_data = P("Mirties data")
    nuotrauka = P("Nuotrauka")
    issilavinimas = P("Išsilavinimas")
    el_pastas = P("El. paštas")
    tel_nr = P("Tel. nr.")
    grynieji_pinigai = P("Grynieji pinigai")
    nekilnojamojo_turto_verte = P("Nekilnojamo turto vertė")
    teistumas = P("Teistumas")
    partija = P("Narystė partijoje")

    class meta:
        title = "Asmuo"


class Darbuotojas(Asmuo):
    pareigos = P("Pareigos")
    darboviete = P("Valstybinį įstaiga, kurioje dirba")
    darbo_el_pastas = P("El. paštas")
    darbo_tel_nr = P("Tel. nr.")
    pajamos = P("Pajamos")
    darboviete = P("Darbovietė")

    class meta:
        title = "Darbuotojas"


class ValstybesTarnautojas(Darbuotojas):

    class meta:
        title = "Valstybės tarnautojas"


class Sandoris(Thing):
    subjektas = P("Subjektas", Agent)
    objektas = P("Objektas", Agent)
    verte = P("Sandorio vertė")
    veiksmas = P("Subjekto atliktas veiksmas")
    data = P("Sandoro data")
    sandorio_objektas = P("Sandorio objektas")

    class meta:
        title = "Sandoris"
        comment = "Subjekto sandoris su objektu dėl sandorio objekto"


class ValstybesTarnautojoSandoris(Sandoris):
    subjektas = P("Valstybės tarnautojas", ValstybesTarnautojas)

    class meta:
        title = "Valstybės tarnautojo sandoris"


class Naryste:
    narys = P("Narys", Agent)
    grupe = P("Grupė", Agent)
    pradzia = P("Pradžios data")
    pabaiga = P("Pabaigos data")
    pareigos = P("Pareigos")


class Pastatas(Thing):
    koordinates = P("Koordinatės", Koordinates)
    adresas = P("Adresas", Adresas)
    aukstu_skaicius = P("Aukštų skaičius")
    statybos_metai = P("Statybos metai")
    pastato_tipas = P("Pastato tipas")
    sildymo_kaina = P("Vidutinė sezono šilumos kaina")
    oro_tarsa = P("Oro tarša")
    rinkos_verte = P("Rinkos vertė")


class Ivykis(Thing):
    koordinates = P("Koordinatės", Koordinates)
    adresas = P("Adresas", Adresas)
    laikas = P("Laikas")


class PolicijojeRegistruotasIvykis(Ivykis):
    rusis = P("Įvykio rūšis")


class SeimoNarys(ValstybesTarnautojas):

    class meta:
        title = "Seimo narys"


class NarysteFrakcijoje(Naryste):
    narys = P("Seimo narys", SeimoNarys)
    grupe = P("Frakcija", Grupe)


class Grupe(Agent):
    pavadinimas = P("Pavadinimas")
    ikurimo_data = P("Įkurimo data")
    likvidavimo_data = P("Likvidavimo data")
    logotipas = P("Logotipas")


class Frakcija(Grupe):
    sutrumpinimas = P("Trumpas pavadinimas")
    partija = P("Partija")


class Dokumentas(Thing):
    pavadinimas = P("Pavadinimas")
    dokumento_tekstas = P("Dokumento tekstas")


class TeisesAktas(Dokumentas):
    numeris = P("Numeris")
    paskelbimo_data = P("Paskelbimo data")
    įsigaliojimo_data = P("Įsigaliojimo data")
    eurovoc_terminas = P("Eurovoc terminas")



class Balsas(Thing):
    balso_reiksme = P("Balso reikšmė")
    laikas = P("Laikas")
    seimo_narys = P("Seimo narys", SeimoNarys)
    frakcija = P("Frakcija", Frakcija)
    balsavimas = P("Balsavimas")
    uzsiregistravo = P("Užsiregistravo")
    klausimas = P("Klausimas")
    teises_aktas = P("Teisės aktas", TeisesAktas)


class Pasisakymas(Thing):
    laikas = P("Pasisakymo data")
    tekstas = P("Pasisakymo tekstas")
    pasisakiusysis = P("Pasisakiusysis", Asmuo)


class PasisakymasStenogramoje(Pasisakymas):
    stenograma = P("Stenograma")
    valstybės_tarnautojas = P("Valstybės tarnautojas")
    posėdžio_pirmininkas = P("Posėdžio pirmininkas")
    teisės_aktas = P("Teisės aktas")
    balsavimas = P("Balsavimas")
    teisės_akto_punktas = P("Teisės akto puntas")


class TeisesAktoPunktas(Thing):
    teises_aktas = P("Teisės aktas")
    tekstas = P("Teisės akto punkto tekstas")
    straipsnis = P("Teisės akto straipsnis")
    skyrius = P("Teisės akto skyrius")
    tipas = P("Teisės akto punkto tipas")


class TeisesAktoPakeitimas(Thing):
    keiciamas_punktas = P("Keičiamas punktas")
    naujas_punktas = P("Naujas punktas")
    projektas = P("Teisės akto projektas")


class StatistinisRodiklis(Thing):
    # https://www.w3.org/TR/vocab-data-cube/
    laikotarop_pradzia = P("Laikotarpio pradžia")
    laikotarop_pabaiga = P("Laikotarpio pabaiga")
    dimensija = P("Dimensija")
    atributas = P("Atributas")
    reikšmė = P("Reikšmė")
    matavimo_vienetas = P("Matavimo vienetas")


class Bankrotas(Ivykis):
    imone = P("Įmonė", Imone)
    laikas = P("Data")
    isieskomos_skolos_dalis = P("Išieškomos skolos dalis")
    bankroto_proceso_iniciatorius = P("Bankroto proceso iniciatorius")

class ViesasisPirkimas(Thing):
    # http://standard.open-contracting.org/
    ocid = P("Globalus identifikatorius")
    id = P("Vidinis identifikatorius")
    laikas = P("Pirkimo paskelbimo data")
    zyme = P("Žymė")
    dalyvis = P("Viešojo pirkimo dalyviai", Imone)
    uzsakovas = P("Užsakovas")


Metrikų knygos lapas	Metrikų knyga
Metrikų knygos lapas	Lapo numeris
Metrikų knygos lapas	Lapo paveiksliukas
Metrikų knyga	Laikotarpis
Metrikų knyga	Pastatas
Metrikų knyga	Skaitmeninimo data
Pastatas	Pastato istorinis administracinis suskirstymas
Pastato istorinis administracinis suskirstymas	Priklausė administraciniam vienetui
Pastato istorinis administracinis suskirstymas	Pradžios data
Pastato istorinis administracinis suskirstymas	Pabaigos data
Vandens telkinys	Pavadinimas
Vandens telkinys	Geografinės koordinatės
Turizmo objektas	Pavadinimas
Turizmo objektas	Rūšis
Turizmo objektas	Geografinės koordinatės
Saugoma teritorija	Pavadinimas
Saugoma teritorija	Geografinės koordinatės
Kultūros vertybė	Pavadinimas
Kultūros vertybė	Geografinės koordinatės
Kultūros vertybė	Rūšis
Lietuviškas žodis	Žodis
Lietuviškas žodis	Žodžio prasmės aprašymas
Lietuviškas žodis	Žodžio naudojimo pavyzdžiai
Lietuviškas žodis	Gramatinė forma
Lietuviškas žodis	Kaitymas kalbos dalimis
Lietuviškas žodis	Galimos dodžio formos
Lietuviškas žodis	Žodžio šaknis
Lietuviškas žodis	Semantinė kategorija
Call data record (CDR)	Tel. nr.
Call data record (CDR)	Skambučio pradžios data ir laikas
Call data record (CDR)	Kada atsiliepta, data ir laikas
Call data record (CDR)	Kada baigtas pokalbis, data ir laikas
Mokymo įstaiga	Pavadinimas
Mokymo įstaiga	Institucijos tipas
Mokymo įstaiga	Pastatas
Studijų programa	Pavadinimas
Studijų programa	Studijų pakopa
Studijų programa	Studijų sritis
Studijų programa	Programos valstybinis numeris
Studijų programa	Aprašymas
Studijų programa	Mokymo įstaiga
Studijų programa	Trukmė metais
Studijų programa	Forma (nuolatinė, neakivaizdinė)
Studijų programa	Profesija
Studijų dalykas	Pavadinimas
Studijų dalykas	Studijų programa
Studijų dalykas	Privaloma
Studijų dalykas	Kreditai
Studentas	Mokymo įstaiga
Studentas	Šalis
Studentas	Mokymo įstaiga iš kurios atvyko (užsieniečiams)
Studentas	Pilietybė
Profesija	Pavadinimas
Profesija	Sritis
Profesija	Darbo vietų skaičius
Profesija	Laisvų darbo vietų skaičius
Darbo vieta	Profesija
Darbo vieta	Pavadinimas
Darbo vieta	Geografinės koordinatės
Liga	Pavadinimas
Susirgimas	Liga
Susirgimas	Susirgimo pradžia
Susirgimas	Susirgimo pabaiga
Susirgimas	Profesija
Susirgimas	Geografinės koordinatės
Visitor location register	Kilmės šalis
Visitor location register	Registracijos data ir laikas
Visitor location register	Telefono modelis
Šalis	Lietuviškas pavadinimas
Šalis	ISO-3166 kodas
Kapinės	Pavadinimas
Kapinės	Geografinės koordinatės
Kapinės	Seniūnija
Kapinės	Savivaldybė
Kapinės	Miestas/Rajonas
Kapas	Kapinės
Kapas	Nuotrauka
Kapas	Vardas
Kapas	Pavardė
Kapas	Gimimo data
Kapas	Mirties data
Lietuvos pilietis	Vardas
Lietuvos pilietis	Gimimo data
Lietuvos pilietis	Gimimo Miestas/Rajonas
Parkavimo aikštelė	Geografinės koordinatės
Parkavimo aikštelė	Parkavimo kaina
Parkavimo aikštelė	Darbo laikas
Parkavimo aikštelė	Laisvų vietų skaičius
Projektas	Prašomos paramos suma
Projektas	Skirtos paramos suma
Projektas	Paramos teikėjas
Projektas	Pavadinimas
Projektas	Vykdytojas
Projektas	Pradžios data
Projektas	Pabaigos data
Projektas	Geografinės koordinatės
Projektas	Sritis
Rinkimai	Pavadinimas
Rinkimai	Rūšis
Rinkimų etapas	Pavadinimas
Rinkimų etapas	Data
Rinkimų apylinkė	Pavadinimas
Rinkimų apylinkė	Geografinės koordinatės
Rinkimų apylinkė	Rinkimų apygarda
Rinkimų apylinkė	Pastatas
Rinkimų apygarda	Pavadinimas
Rinkimų apygarda	Geografinės koordinatės
Partija	Rinkimai
Partija	Pavadinimas
Partija	Vadovas
Rinkimų kandidatas	Vardas
Rinkimų kandidatas	Pavardė
Rinkimų kandidatas	Gimimo data
Rinkimų kandidatas	Gimtoji kalba
Rinkimų kandidatas	Išsilavinimas
Rinkimų kandidatas	Tautybė
Rinkimų kandidatas	Nuotrauka
Rinkimų kandidatas	Teistumas
Rinkimų kandidatas	Grynieji pinigai
Rinkimų kandidatas	Nekilnojamo turto vertė
Rinkimų kandidatas	Pajamos
Rinkimų kandidatas	Darbovietė
Rinkimų kandidatas	Narystė partijoje
Rinkimų kandidatas	Išsilavinimas
Rinkimų kandidatas	Sandoris
Rinkimų kandidatas	Rinkimai
Rinkimų kandidatas	Eilė sąraše
Rinkimų kandidatas	Sąrašas
Rinkimų kandidatas	Sutuoktinis
Rinkimų kandidatas	Vaikas
Autobusų stotelė	Pavadinimas
Autobusų stotelė	Geografinės koordinatės
Maršrutas	Pavadinimas
Maršrutas	Stotelių sąrašas
Biudžeto fiskalinis įrašas	Suma
Biudžeto fiskalinis įrašas	Pajamos/Išlaidos
Biudžeto fiskalinis įrašas	Sritis
Biudžeto fiskalinis įrašas	Mokesčių mokėtojas
Biudžeto fiskalinis įrašas	Asignavimų valdytojas
Biudžeto fiskalinis įrašas	Data ir laikas
Biudžeto fiskalinis įrašas	Geografinės koordinatės
