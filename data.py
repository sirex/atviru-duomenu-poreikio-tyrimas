class P:

    def __init__(self, title, type=None, *, choices=None, wikidata=None):
        self.title = title
        self.type = type
        self.choices = choices
        self.wikidata = wikidata


class Meta:

    def __init__(self, title=None, wikidata=None):
        self.title = title
        self.wikidata = wikidata


class Objektas:
    meta = Meta()

    pavadinimas = P("Pavadinimas", str)

    def __init__(self, **kw):
        self.meta.title = self.meta.title or self.__class__.__name__
        self.kw = kw

    def __getitem__(self, name):
        return getattr(self, name)


class DataLaikas(Objektas):
    laiko_juosta = P("Laiko juosta")


class Data(DataLaikas):
    metai = P("Metai", int)
    menuo = P("Menuo", int)
    diena = P("Diena", int)


class Laikas(DataLaikas):
    valanda = P("Valanda", int)
    minute = P("Minute", int)
    sekunde = P("Sekunde", int)


class Laikotarpis(Objektas):
    pradzia = P("Pradžia", DataLaikas, wikidata='P580')
    pabaiga = P("Pabaiga", DataLaikas, wikidata='P582')


class Koordinates(Objektas):
    ilguma = P("Geografinė ilguma", str)
    platuma = P("Geografinė platuma", str)


class Adresas(Objektas):
    meta = Meta("Adresas")

    koordinates = P("Koordinatės", Koordinates)
    apskritis = P("Apskritis")
    rajonas = P("Miestas/Rajonas")
    savivaldybe = P("Savivaldybė")
    gatve = P("Gatvė")
    pastato_numeris = P("Pastato numeris")
    laikotarpis = P("Laikotarpis", Laikotarpis)


class Agentas(Objektas):
    meta = Meta("Agentas")

    pavadinimas = P("Pavadinimas")


class Licencija(Objektas):
    prekyba_alkoholiu = P("Prekyba alkoholiu")


class JuridinisAsmuo(Agentas):
    meta = Meta("Juridinis asmuo")

    registracijos_numeris = P("Registracijos numeris")
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
    licencija = P("Licencija", Licencija)


class Imone(JuridinisAsmuo):
    meta = Meta("Įmonė")


class ImoneiPriklausantisPastatas(Adresas):
    meta = Meta("Įmonei priklausantis pastatas")

    darbo_laikas = P("Darbo laikas")


class Akcininkas(Agentas):
    meta = Meta("Akcininkas")

    akciju_dalis = P("Akcijų dalis įmonėje")


class ValstybineIstaiga(JuridinisAsmuo):
    meta = Meta("Valstybinė įstaiga")

    priklauso_istaigai = P("Valstybinė įstaiga, kuriai yra pavaldi")


class Pastatas(Objektas):
    koordinates = P("Koordinatės", Koordinates)
    adresas = P("Adresas", Adresas)
    aukstu_skaicius = P("Aukštų skaičius")
    statybos_metai = P("Statybos metai")
    pastato_tipas = P("Pastato tipas")
    sildymo_kaina = P("Vidutinė sezono šilumos kaina")
    oro_tarsa = P("Oro tarša")
    rinkos_verte = P("Rinkos vertė")


class MaitinimoIstaiga(Pastatas):
    """Pastatas, kuriame teikiamos maitinimo paslaugos (kavinė, baras, restorantas)."""
    imone = P("Įmonė", Imone)
    licencija = P("Licencija", Licencija)


class MokymoIstaiga(Objektas):
    pavadinimas = P("Pavadinimas")
    institucijos_tipas = P("Institucijos tipas")
    pastatas = P("Pastatas", Pastatas)
    adresas = P("Adresas", Adresas)


class Profesija(Objektas):
    pavadinimas = P("Pavadinimas")
    sritis = P("Sritis")
    darbo_vietų_skaičius = P("Darbo vietų skaičius")
    laisvu_darbo_vietu_skaicius = P("Laisvų darbo vietų skaičius")


class StudijuPrograma(Objektas):
    pavadinimas = P("Pavadinimas")
    studiju_pakopa = P("Studijų pakopa")
    studiju_sritis = P("Studijų sritis")
    programos_valstybinis_numeris = P("Programos valstybinis numeris")
    aprasymas = P("Aprašymas")
    mokymo_istaiga = P("Mokymo įstaiga")
    trukme_metais = P("Trukmė metais")
    forma = P("Forma (nuolatinė, neakivaizdinė)", choices=('nuolatinė', 'neakyvaizdinė'))
    profesija = P("Profesija", Profesija)


class StudijuDalykas(Objektas):
    pavadinimas = P("Pavadinimas")
    studiju_programa = P("Studijų programa", StudijuPrograma)
    privaloma = P("Privaloma")
    kreditai = P("Kreditai")


class Issilavinimas(Laikotarpis):
    studiju_programa = P("Studijų programa", StudijuPrograma)


class Pareigos(Laikotarpis):
    pakeicia = P(
        "Pakeičia", 'Asmuo', wikidata='P1365',
        comment="Pakeičia ansčiau pareigas ėjusį asmenį.",
    )
    pakeistas = P(
        "Pakeistas", 'Asmuo', wikidata='P1366',
        comment="Buvo pakeistas vėliau šias pareigas užėmusio asmens.",
    )


class Asmuo(Agentas):
    meta = Meta("Asmuo", wikidata='Q5')

    lytis = P("Lytis", wikidata='P21', choices=("vyras", "moteris"))
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
    tautybė = P("Tautybė")
    pilietybe = P("Pilietybė", wikidata='P27')
    gimtoji_kalba = P("Gimtoji kalba")
    išsilavinimas = P("Išsilavinimas", Issilavinimas)
    teistumas = P("Teistumas")
    seima = P("Šeima", 'Seima')
    santuoka = P("Santuoka", 'Santuoka')
    pareigos = P("Pareigos", Pareigos, wikidata='P39')


class Seima(Objektas):
    tevas = P("Tėvas", Asmuo)
    motina = P("Motina", Asmuo)
    vaikas = P("Vaikas", Asmuo)


class Santuoka(Laikotarpis):
    sutuoktinis = P("Sutuoktinis", Asmuo)


class ValstybesTarnautojas(Darbuotojas):
    meta = Meta("Valstybės tarnautojas")


class Sandoris(Objektas):
    """Subjekto sandoris su objektu dėl sandorio objekto."""
    meta = Meta("Sandoris")

    subjektas = P("Subjektas", Agentas)
    objektas = P("Objektas", Agentas)
    verte = P("Sandorio vertė")
    veiksmas = P("Subjekto atliktas veiksmas")
    data = P("Sandoro data")
    sandorio_objektas = P("Sandorio objektas")


class ValstybesTarnautojoSandoris(Sandoris):
    meta = Meta("Valstybės tarnautojo sandoris")

    subjektas = P("Valstybės tarnautojas", ValstybesTarnautojas)


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
    darboviete = P("Darbovietė", Imone)
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


class SeimoNarys(ValstybesTarnautojas):
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
    pranešėjas = P("Pranešėjas", Atstovas)


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

    imone = P("Įmonė", Imone)
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
    dalyvis = P("Viešojo pirkimo dalyviai", Imone)
    uzsakovas = P("Užsakovas")
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


class Studentas(Asmuo):
    mokymo_istaiga = P("Mokymo įstaiga", MokymoIstaiga)
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
    sandoris = P("Sandoris", Sandoris)
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
