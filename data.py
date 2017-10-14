class P:

    def __init__(self, title, type=None, *, choices=None):
        self.title = title
        self.type = type
        self.choices = choices


class Objektas:

    def __init__(self, **kw):
        self.kw = kw

    def __getitem__(self, name):
        return getattr(self, name)

    class meta:
        title = None


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
    """Nusako kaip objekto savybės keitėsi laike."""
    objektas = P("Ryšys su naujesnio laikotarpio objektu", Objektas)
    pradzia = P("Laikotarpio pradžia", DataLaikas)
    pabaiga = P("Laikotarpio pabaiga", DataLaikas)


class Koordinates(Objektas):
    ilguma = P("Geografinė ilguma", str)
    platuma = P("Geografinė platuma", str)


class Adresas(Objektas):
    koordinates = P("Koordinatės", Koordinates)
    apskritis = P("Apskritis")
    rajonas = P("Miestas/Rajonas")
    savivaldybe = P("Savivaldybė")
    gatve = P("Gatvė")
    pastato_numeris = P("Pastato numeris")
    laikotarpis = P("Laikotarpis", Laikotarpis)

    class meta:
        title = "Adresas"


class Agentas(Objektas):
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


class Pastatas(Objektas):
    koordinates = P("Koordinatės", Koordinates)
    adresas = P("Adresas", Adresas)
    aukstu_skaicius = P("Aukštų skaičius")
    statybos_metai = P("Statybos metai")
    pastato_tipas = P("Pastato tipas")
    sildymo_kaina = P("Vidutinė sezono šilumos kaina")
    oro_tarsa = P("Oro tarša")
    rinkos_verte = P("Rinkos vertė")


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
    tautybė = P("Tautybė")
    pilietybe = P("Pilietybė")
    gimtoji_kalba = P("Gimtoji kalba")
    išsilavinimas = P("Išsilavinimas", Issilavinimas)
    teistumas = P("Teistumas")
    seima = P("Šeima", 'Seima')
    santuoka = P("Santuoka", 'Santuoka')

    class meta:
        title = "Asmuo"


class Seima(Objektas):
    tevas = P("Tėvas", Asmuo)
    motina = P("Motina", Asmuo)
    vaikas = P("Vaikas", Asmuo)


class Santuoka(Laikotarpis):
    sutuoktinis = P("Sutuoktinis", Asmuo)


class Darbuotojas(Asmuo):
    pareigos = P("Pareigos")
    profesija = P("Profesija", Profesija)
    darboviete = P("Darbovietė", Imone)
    darbo_el_pastas = P("El. paštas")
    darbo_tel_nr = P("Tel. nr.")
    darbo_vietos_adresas = P("Adresas", Adresas)
    darbo_vietos_koordinates = P("Koordinatės", Koordinates)
    pajamos = P("Pajamos")

    class meta:
        title = "Darbuotojas"


class ValstybesTarnautojas(Darbuotojas):

    class meta:
        title = "Valstybės tarnautojas"


class Sandoris(Objektas):
    subjektas = P("Subjektas", Agentas)
    objektas = P("Objektas", Agentas)
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


class Laikotarpis(Objektas):
    pradzia = P("Pradžia")
    pabaiga = P("Pabaiga")


class Naryste(Laikotarpis):
    narys = P("Narys", Agentas)
    grupe = P("Grupė", Agentas)
    pareigos = P("Pareigos")


class Ivykis(Objektas):
    koordinates = P("Koordinatės", Koordinates)
    adresas = P("Adresas", Adresas)
    pradzia = P("Įvykio pradžia")
    pabaiga = P("Įvykio pabaiga")


class PolicijojeRegistruotasIvykis(Ivykis):
    rusis = P("Įvykio rūšis")


class SeimoNarys(ValstybesTarnautojas):

    class meta:
        title = "Seimo narys"


class Grupe(Agentas):
    pavadinimas = P("Pavadinimas")
    ikurimo_data = P("Įkurimo data")
    likvidavimo_data = P("Likvidavimo data")
    logotipas = P("Logotipas")


class NarysteFrakcijoje(Naryste):
    narys = P("Seimo narys", SeimoNarys)
    grupe = P("Frakcija", Grupe)


class Frakcija(Grupe):
    sutrumpinimas = P("Trumpas pavadinimas")
    partija = P("Partija")


class Dokumentas(Objektas):
    pavadinimas = P("Pavadinimas")
    dokumento_tekstas = P("Dokumento tekstas")


class TeisesAktas(Dokumentas):
    numeris = P("Numeris")
    paskelbimo_data = P("Paskelbimo data")
    įsigaliojimo_data = P("Įsigaliojimo data")
    eurovoc_terminas = P("Eurovoc terminas")


class Balsas(Objektas):
    balso_reiksme = P("Balso reikšmė")
    laikas = P("Laikas")
    seimo_narys = P("Seimo narys", SeimoNarys)
    frakcija = P("Frakcija", Frakcija)
    balsavimas = P("Balsavimas")
    uzsiregistravo = P("Užsiregistravo")
    klausimas = P("Klausimas")
    teises_aktas = P("Teisės aktas", TeisesAktas)


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


class StatistinisRodiklis(Objektas):
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


class Projektas(Ivykis):
    pavadinimas = P("Projekto pavadinimas")
    prasomos_paramos_suma = P("Prašomos paramos suma")
    skirtos_paramos_suma = P("Skirtos paramos suma")
    paramos_teikejas = P("Paramos teikėjas", Agentas)
    vykdytojas = P("Vykdytojas", Agentas)
    sritis = P("Sritis")


class ViesasisPirkimas(Objektas):
    # http://standard.open-contracting.org/
    ocid = P("Globalus identifikatorius")
    id = P("Vidinis identifikatorius")
    laikas = P("Pirkimo paskelbimo data")
    zyme = P("Žymė")
    dalyvis = P("Viešojo pirkimo dalyviai", Imone)
    uzsakovas = P("Užsakovas")
    projektas = P("Projektas", Projektas)


class MetrikuKnyga(Objektas):
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


class Partija(Grupe):
    pavadinimas = P("Pavadinimas")
    rinkimai = P("Rinkimai")
    vadovas = P("Vadovas", Asmuo)


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
