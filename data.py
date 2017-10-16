class P:

    def __init__(self, type, qualifier=None, *, choices=None, wikidata=None):
        assert not isinstance(type, Kvalifikatorius)
        assert qualifier is None or isinstance(qualifier, Kvalifikatorius)
        self.type = type
        self.qualifier = qualifier
        self.choices = choices
        self.wikidata = wikidata


class Meta:

    def __init__(self, title=None, wikidata=None):
        self.title = title
        self.wikidata = wikidata


# Base classes

class Kvalifikatorius:
    pass


class Objektas:
    meta = Meta()

    unikalus_identifikatorius = P(str)
    pavadinimas = P(str)

    def __init__(self, **kw):
        self.meta.title = self.meta.title or self.__class__.__name__
        self.kw = kw

    def __getitem__(self, name):
        return getattr(self, name)


# Data types

class DataLaikas:
    laiko_juosta = P("Laiko juosta")


class Data(DataLaikas):
    metai = P(int)
    menuo = P(int)
    diena = P(int)


class Laikas(DataLaikas):
    valanda = P(int)
    minute = P(int)
    sekunde = P(int)


class Kiekis:
    reikšmė = P(float)
    matavimo_vienetai = P(str)


class PinigųKiekis(Kiekis):
    valiuta = P(str)


class Paveiksliukas:
    pass


class DarboLaikas:
    savaitės_diena = P(str)
    pradžia = P(Laikas)
    pabaiga = P(Laikas)


# Data models

class Laikotarpis(Kvalifikatorius):
    pradžia = P(DataLaikas)
    pabaiga = P(DataLaikas)


class Koordinates(Objektas):
    ilguma = P(str)
    platuma = P(str)


class Adresas(Objektas):
    koordinatės = P(Koordinates)
    apskritis = P(Objektas)
    rajonas = P(Objektas)
    savivaldybė = P(Objektas)
    gatve = P(Objektas)
    pastato_numeris = P(int)


class Pastatas(Objektas):
    koordinatės = P(Koordinates)
    adresas = P(Adresas, Laikotarpis)
    aukštų_skaičius = P(int)
    statybos_metai = P(Data)
    pastato_tipas = P(str)
    šildymo_kaina = P(PinigųKiekis, Laikotarpis)
    oro_tarša = P(Kiekis)
    rinkos_vertė = P(PinigųKiekis)
    darbo_laikas = P(DarboLaikas)


class Agentas(Objektas):
    pass


class Asmuo(Agentas):
    meta = Meta(wikidata='Q5')

    lytis = P(str, wikidata='P21', choices=("vyras", "moteris"))
    vardas = P(Objektas, Laikotarpis)
    pavarde = P(Objektas, Laikotarpis)
    gimimo_data = P(DataLaikas)
    mirties_data = P(DataLaikas)
    nuotrauka = P(Paveiksliukas, Laikotarpis)
    išsilavinimas = P('MokymoĮstaiga', 'Išsilavinimas', choices=("aukštasis", "aukštesnysis", "vidurinis", "pradinis"))
    el_paštas = P(str, Laikotarpis)
    tel_nr = P(str, Laikotarpis)
    grynieji_pinigai = P(PinigųKiekis, Laikotarpis)
    nekilnojamojo_turto_verte = P(PinigųKiekis, Laikotarpis)
    teistumas = P(bool)
    partija = P('Partija')
    tautybė = P(Objektas)
    pilietybe = P(Objektas, Laikotarpis, wikidata='P27')
    gimtoji_kalba = P(Objektas)
    teistumas = P(bool)
    pareigos = P('Pareigos', Laikotarpis, wikidata='P39')
    sutuoktinis = P('Asmuo', Laikotarpis)
    vaikas = P('Asmuo')


class Licencija(Objektas):
    prekyba_alkoholiu = P(bool)


class JuridinisAsmuo(Agentas):
    registracijos_numeris = P(str)
    registracijos_adresas = P(Adresas, Laikotarpis)
    teisine_forma = P(str)
    pastatas = P(Pastatas, Laikotarpis)
    veiklos_sritis = P(str)
    el_pastas = P(str, Laikotarpis)
    tel_nr = P(str, Laikotarpis)
    tinklapis = P(str, Laikotarpis)
    darbuotoju_skaicius = P(int, Laikotarpis)
    vidutinis_atlyginimas = P(PinigųKiekis, Laikotarpis)
    skola_sodrai = P(PinigųKiekis, Laikotarpis)
    apyvarda = P(PinigųKiekis, Laikotarpis)
    iregistravimo_data = P(DataLaikas)
    isregistravimo_data = P(DataLaikas)
    logotipas = P(Paveiksliukas, Laikotarpis)
    akcininkas = P(Agentas)
    direktorius = P(Asmuo)
    licencija = P(Licencija)


class Įmonė(JuridinisAsmuo):
    pass


class Akcininkas(Agentas):
    meta = Meta("Akcininkas")

    akciju_dalis = P("Akcijų dalis įmonėje")


class ValstybineIstaiga(JuridinisAsmuo):
    meta = Meta("Valstybinė įstaiga")

    priklauso_istaigai = P("Valstybinė įstaiga, kuriai yra pavaldi")


class MaitinimoĮstaiga(Objektas):
    """Pastatas, kuriame teikiamos maitinimo paslaugos (kavinė, baras, restorantas)."""
    savininkas = P(Įmonė)
    prekybos_alkoholiu_licencija = P(Objektas, Laikotarpis)
    adresas = P(Adresas)


class MokymoĮstaiga(Objektas):
    institucijos_tipas = P(str, choices=("universitetas", "mokykla"))
    pastatas = P(Pastatas, Laikotarpis)
    adresas = P(Adresas, Laikotarpis)


class Profesija(Objektas):
    sritis = P(str)
    darbo_vietų_skaičius = P(int, Laikotarpis)
    laisvu_darbo_vietu_skaicius = P(int, Laikotarpis)


class StudijuPrograma(Objektas):
    studiju_pakopa = P(str)
    studiju_sritis = P(str)
    programos_valstybinis_numeris = P(str)
    aprasymas = P(str)
    trukme_metais = P(int)
    forma = P(str, choices=('nuolatinė', 'neakyvaizdinė'))
    profesija = P(Profesija)


class StudijuDalykas(Objektas):
    studiju_programa = P(StudijuPrograma)
    privaloma = P(bool)
    kreditai = P(float)


class Išsilavinimas(Laikotarpis):
    mokymo_istaiga = P(MokymoĮstaiga)
    studiju_programa = P(StudijuPrograma)


class Pareigos(Laikotarpis):
    pakeicia = P(
        "Pakeičia", 'Asmuo', wikidata='P1365',
        comment="Pakeičia ansčiau pareigas ėjusį asmenį.",
    )
    pakeistas = P(
        "Pakeistas", 'Asmuo', wikidata='P1366',
        comment="Buvo pakeistas vėliau šias pareigas užėmusio asmens.",
    )


class Santuoka(Laikotarpis):
    sutuoktinis = P("Sutuoktinis", Asmuo)


class ValstybėsTarnautojas(Asmuo):
    pass


class SandorioŠalis(Kvalifikatorius):
    veiksmas = P(str)


class Sandoris(Objektas):
    šalis = P(Asmuo, SandorioŠalis)
    vertė = P(PinigųKiekis)
    data = P(DataLaikas)
    objektas = P(Objektas)


class ValstybesTarnautojoSandoris(Sandoris):
    šalis = P(ValstybėsTarnautojas, SandorioŠalis)


class Laikotarpis(Objektas):
    pradzia = P("Pradžia", DataLaikas)
    pabaiga = P("Pabaiga", DataLaikas)


class Naryste(Laikotarpis):
    narys = P("Narys", Agentas)
    grupe = P("Grupė", Agentas)
    pareigos = P("Pareigos")


class Darbuotojas(Naryste):
    meta = Meta("Darbuotojas")

    narys = P("Asmuo", Asmuo)
    pareigos = P("Pareigos")
    profesija = P("Profesija", Profesija)
    darboviete = P("Darbovietė", Įmonė)
    darbo_el_pastas = P("El. paštas")
    darbo_tel_nr = P("Tel. nr.")
    darbo_vietos_adresas = P("Adresas", Adresas)
    darbo_vietos_koordinates = P("Koordinatės", Koordinates)
    pajamos = P("Pajamos")


class Ivykis(Laikotarpis):
    koordinates = P("Koordinatės", Koordinates)
    adresas = P("Adresas", Adresas)


class PolicijojeRegistruotasIvykis(Ivykis):
    rusis = P("Įvykio rūšis")


class SeimoNarys(ValstybėsTarnautojas):
    meta = Meta("Seimo narys")


class Grupe(Agentas):
    pavadinimas = P("Pavadinimas")
    ikurimo_data = P("Įkurimo data")
    likvidavimo_data = P("Likvidavimo data")
    logotipas = P("Logotipas")
    naryste = P("Grupės narys", Agentas)


class Partija(Grupe):
    pavadinimas = P("Pavadinimas")
    rinkimai = P("Rinkimai")
    vadovas = P("Vadovas", Asmuo)


class Frakcija(Grupe):
    naryste = P("Frakcijos nariai", Naryste(grupe='self', narys=SeimoNarys))
    sutrumpinimas = P("Trumpas pavadinimas")
    partija = P("Partija", Partija)


class Dokumentas(Objektas):
    pavadinimas = P("Pavadinimas")
    dokumento_tekstas = P("Dokumento tekstas")


class TeisesAktas(Dokumentas):
    numeris = P("Numeris")
    paskelbimo_data = P("Paskelbimo data")
    įsigaliojimo_data = P("Įsigaliojimo data")
    eurovoc_terminas = P("Eurovoc terminas")


class SvarstytoKlausimoFormuluote(Objektas):
    formuluote = P("Svarstyto klausimo formuluote")


class SeimeSvarstytasKlausimas(Objektas):
    formuluote = P("Klausimo formuluotė", SvarstytoKlausimoFormuluote)
    etapas = P("Klausimo svarstymo etapas", choices=(
        "pateikimas",
        "svarstymas",
        "priemimas",
    ))


class SeimoBalsavimas(Objektas):
    laikas = P("Laikas", DataLaikas)
    klausimas = P("Klausimas dėl kurio buvo balsuota", SeimeSvarstytasKlausimas)


class Balsas(Objektas):
    balsas = P("Balso reikšmė", str, choices=(
        "už",
        "susilaikė",
        "prieš",
    ))
    formuluote = P("Balsuota už svarstyto klausimo formuluote", SvarstytoKlausimoFormuluote)
    laikas = P("Laikas", DataLaikas)
    seimo_narys = P("Seimo narys", SeimoNarys)
    frakcija = P("Frakcija", Frakcija)
    balsavimas = P("Balsavimas", SeimoBalsavimas)
    uzsiregistravo = P("Užsiregistravo", bool)
    klausimas = P("Klausimas")
    teises_aktas = P("Teisės aktas", TeisesAktas)
    pranešėjas = P(Asmuo)


class Pasisakymas(Objektas):
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


class TeisesAktoPunktas(Objektas):
    teises_aktas = P("Teisės aktas")
    tekstas = P("Teisės akto punkto tekstas")
    straipsnis = P("Teisės akto straipsnis")
    skyrius = P("Teisės akto skyrius")
    tipas = P("Teisės akto punkto tipas")


class TeisesAktoPakeitimas(Objektas):
    keiciamas_punktas = P("Keičiamas punktas")
    naujas_punktas = P("Naujas punktas")
    projektas = P("Teisės akto projektas")


class StatistinisRodiklis(Laikotarpis):
    meta = Meta("Statistinis rodiklis")

    # https://www.w3.org/TR/vocab-data-cube/
    dimensija = P("Dimensija")
    atributas = P("Atributas")
    reiksme = P("Reikšmė")
    matavimo_vienetas = P("Matavimo vienetas")


class Bankrotas(Ivykis):
    meta = Meta("Bankrotas")

    imone = P(Įmonė)
    laikas = P("Data")
    isieskomos_skolos_dalis = P("Išieškomos skolos dalis")
    bankroto_proceso_iniciatorius = P("Bankroto proceso iniciatorius")


class Projektas(Ivykis):
    meta = Meta("Projektas")

    pavadinimas = P("Projekto pavadinimas")
    prasomos_paramos_suma = P("Prašomos paramos suma")
    skirtos_paramos_suma = P("Skirtos paramos suma")
    paramos_teikejas = P("Paramos teikėjas", Agentas)
    vykdytojas = P("Vykdytojas", Agentas)
    sritis = P("Sritis")


class ViesasisPirkimas(Objektas):
    meta = Meta("Viešasis pirkimas")

    # http://standard.open-contracting.org/
    ocid = P("Globalus identifikatorius")
    id = P("Vidinis identifikatorius")
    laikas = P("Pirkimo paskelbimo data")
    zyme = P("Žymė")
    dalyvis = P(Įmonė)
    uzsakovas = P(Įmonė)
    projektas = P("Projektas", Projektas)


class MetrikuKnyga(Objektas):
    meta = Meta("Metriku knyga")

    laikotarpis = P("Laikotarpis")
    pastatas = P("Pastatas")
    skaitmeninimo_data = P("Skaitmeninimo data")


class MetrikuKnygosLapas(Objektas):
    metrikų_knyga = P("Metrikų knyga", MetrikuKnyga)
    lapo_numeris = P("Lapo numeris")
    lapo_paveiksliukas = P("Lapo paveiksliukas")


class ErdvinisObjektas(Objektas):
    koordinates = P("Koordinatės", Koordinates)
    konturas = P("Geografinis kontūras su koordinatėmis")


class VandensTelkinys(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")


class TurizmoObjektas(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")
    rusis = P("Rūšis")


class SaugomaTeritorija(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")


class KurturosVertybe(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")
    rusis = P("Rūšis")


class LietuviskasZodis(Objektas):
    zodis = P("Žodis")
    zodzio_prasmes_aprasymas = P("Žodžio prasmės aprašymas")
    zodzio_naudojimo_pavyzdziai = P("Žodžio naudojimo pavyzdžiai")
    gramatine_forma = P("Gramatinė forma")
    kaitymas_kalbos_dalimis = P("Kaitymas kalbos dalimis")
    galimos_zodzio_formos = P("Galimos žodžio formos")
    zodzio_saknis = P("Žodžio šaknis")
    semantine_kategorija = P("Semantinė kategorija")


class SkabuciuRegistroIrasas(Objektas):
    """Call data record (CDR)"""
    tel_nr = P("Tel. nr.")
    skambucio_pradzia = P("Skambučio pradžios data ir laikas")
    kada_atsiliepta = P("Kada atsiliepta, data ir laikas")
    kada_baigtas_pokalbis = P("Kada baigtas pokalbis, data ir laikas")


class Studijos(Kvalifikatorius):
    pradžia = P(DataLaikas)
    pabaiga = P(DataLaikas)


class Studentas(Asmuo):
    studijavo = P(MokymoĮstaiga, Studijos)
    mokymo_istaiga = P("Mokymo įstaiga", MokymoĮstaiga)
    salis = P("Šalis")
    mokymo_istaiga_is_kurios_atvyko = P("Mokymo įstaiga iš kurios atvyko (užsieniečiams)")


class Liga(Objektas):
    pavadinimas = P("Pavadinimas")


class Susirgimas(Ivykis):
    liga = P("Liga")
    asmuo = P("Asmuo", Asmuo)


class TelefonoRegistracijaPrieMobTinklo(Ivykis):
    """Visitor location register"""
    kilmes_salis = P("Kilmės šalis")
    tel_nr = P("Telefono modelis")


class Salis(ErdvinisObjektas):
    pavadinimas = P("Lietuviškas pavadinimas")
    iso_3166_kodas = P("Šalies ISO-3166 kodas")


class Kapines(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")
    adresas = P("Adresas", Adresas)
    tikejimas = P("Tikėjimas")


class Kapas(ErdvinisObjektas):
    kapines = P("Kapinės", Kapines)
    nuotrauka = P("Nuotrauka")
    asmuo = P("Asmuo", Asmuo)


class LietuvosPilietis(Asmuo):
    registracijos_adresas = P("Registracijos adresas", Adresas)
    nuolatine_gyvenamoji_vieta = P("Nuolatinė gyvenamoji vieta", Adresas)


class ParkavimoAikstele(ErdvinisObjektas):
    kaina = P("Parkavimo kaina")
    darbo_laikas = P("Darbo laikas")
    laisvu_vietu_skaicius = P("Laisvų vietų skaičius")


class Rinkimai(Ivykis):
    pavadinimas = P("Pavadinimas")
    rūšis = P("Rūšis", choices=("prezidento", "seimo", "savivaldybių"))


class RinkimuEtapas(Ivykis):
    pavadinimas = P("Pavadinimas")
    rinkimai = P("Rinkimai", Rinkimai)


class RinkimuApygarda(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")


class RinkimuApylinke(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")
    apygarda = P("Rinkimų apygarda", RinkimuApygarda)
    pastatas = P("Pastatas")


class RinkimuKandidatas(Asmuo):
    partija = P("Partija", Naryste(narys='self', grupe=Partija))
    sandoris = P("Sandoris", Laikotarpis)
    rinkimai = P("Rinkimai")
    eile_sarase = P("Eilė sąraše")
    sarasas = P("Sąrašas")


class Stotele(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")


class AutomusoStotele(Stotele):
    pass


class Marsrutas(Objektas):
    stotele = P("Stotelė", Stotele)
    laikas = P("Atvykimo į stotelę laikas", DataLaikas)


class BiudzetoFiskalinisIrasas(Objektas):
    suma = P("Suma")
    saskaita = P("Sąskaita", choices=("pajamos", "išlaidos"))
    sritis = P("Sritis")
    mokesciu_moketojas = P("Mokesčių mokėtojas")
    asignavimu_valdytojas = P("Asignavimų valdytojas")
    laikas = P("Data ir laikas", DataLaikas)
    adresas = P("Adresas", Adresas)
