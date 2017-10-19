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

    raktas = P(str, comment="Vidinis identifikatorius (raktas)")
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


class ErdvinisObjektas(Objektas):
    pass


class Taškas(ErdvinisObjektas):
    koordinates = P(Koordinates)


class Linija(ErdvinisObjektas):
    linija = P(list)


class Kontūras(ErdvinisObjektas):
    kontūras = P(list)


class Teritorija(Kontūras):
    gyventojų_skaičius = P(int)


class Apskritis(Teritorija):
    pass


class Rajonas(Teritorija):
    pass


class Savivaldybė(Teritorija):
    pass


class Seniūnija(Teritorija):
    pass


class Gyvenvietė(Teritorija, Taškas):
    rūšis = P(str, choices=(
        'miestas',
        'kaimas',
        'vienkiemis',
    ))


class Gatvė(Linija):
    pass


class Adresas(ErdvinisObjektas):
    koordinatės = P(Koordinates)
    apskritis = P(Apskritis)
    rajonas = P(Rajonas)
    savivaldybė = P(Savivaldybė)
    seniūnija = P(Seniūnija)
    gyvenvietė = P(Gyvenvietė)
    gatve = P(Gatvė)
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


class Laikotarpis(Objektas):
    pradžia = P(DataLaikas)
    pabaiga = P(DataLaikas)


class Įvykis(Laikotarpis):
    adresas = P(Adresas)


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
    sutuoktinis = P('Asmuo', Laikotarpis)
    vaikas = P('Asmuo')


class Pareigos(Objektas):
    pass


class Narystė(Laikotarpis):
    narys = P(Agentas)
    grupė = P(Agentas)
    pareigos = P(Pareigos, 'UžimamosPareigos', m2mbref='grupė')


class Grupė(Agentas):
    vadovas = P(Asmuo)
    logotipas = P(str)
    įkurta = P(DataLaikas)
    likviduota = P(DataLaikas)
    narys = P(Agentas, Narystė, m2mbref='grupė')


class UžimamosPareigos(Laikotarpis):
    asmuo = P(Asmuo)
    grupė = P(Grupė)
    pareigos = P(Pareigos)
    pakeičia = P(Asmuo, wikidata='P1365', comment="Pakeičia ansčiau pareigas ėjusį asmenį.")
    pakeistas = P(Asmuo, wikidata='P1366', comment="Buvo pakeistas vėliau šias pareigas užėmusio asmens.")


class MaitinimoĮstaigosAdresas(Adresas):
    pass


class MaitinimoĮstaiga(Objektas):
    savininkas = P(Agentas)
    adresas = P(MaitinimoĮstaigosAdresas)


class PrekybosAlkoholiuLicencija(Laikotarpis):
    maitinimo_įstaiga = P(MaitinimoĮstaiga)


class KategorijųMedis(Objektas):
    pass


class KategorijųMedžioŠaka(Objektas):
    medis = P(KategorijųMedis)
    kamienas = P('self')


class VeiklosSritis(KategorijųMedis):
    pass


class TeisinėForma(Laikotarpis):
    pavadinimas = P(str, choices=(
        "Valstybės ar savivaldybės įmonė",
        "Tikroji ar komanditinė ūkinė bendrija",
        "Uždaroji akcinė bendrovė",
        "Akcinė bendrovė",
        "Žemės ūkio bendrovė",
        "Viešoji įstaiga",
        "Asociacija",
        "Kooperatinė bendrovė",
        "Individuali įmonė",
        "Mažoji bendrija",
    ))


class JuridinisAsmuo(Grupė):
    registracijos_numeris = P(str)
    adresas = P(Adresas, Laikotarpis)
    teisinė_forma = P(TeisinėForma)
    pastatas = P(Pastatas, Laikotarpis)
    veiklos_sritis = P(VeiklosSritis)
    el_paštas = P(str, Laikotarpis)
    tel_nr = P(str, Laikotarpis)
    tinklapis = P(str, Laikotarpis)
    darbuotojų_skaičius = P(int, Laikotarpis, sameas='narių_skaičius')
    vidutinis_atlyginimas = P(PinigųKiekis, Laikotarpis)
    skola_sodrai = P(PinigųKiekis, Laikotarpis)
    įregistravimo_data = P(DataLaikas, sameas='įkurta')
    išregistravimo_data = P(DataLaikas, sameas='likviduota')
    direktorius = P(Asmuo, sameas='vadovas')


class Įmonė(JuridinisAsmuo):
    apyvarda = P(PinigųKiekis, Laikotarpis)
    akcininkas = P(Agentas)


class Akcininkas(Agentas):
    įmonė = P(Įmonė)
    akciju_dalis_įmonėje = P(Kiekis)


class ValstybinėĮstaiga(JuridinisAsmuo):
    priklauso_įstaigai = P('self')


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
    sritis = P(VeiklosSritis)
    darbo_vietų_skaičius = P(int, Laikotarpis)
    laisvu_darbo_vietu_skaicius = P(int, Laikotarpis)


class VardasPavardė(Laikotarpis):
    asmuo = P(Asmuo)
    vardas = P(str)
    pavardė = P(str)


class ValstybėsTarnautojoVardasPavardė(VardasPavardė):
    pass


class ValstybinėsĮstaigosPareigybės(Laikotarpis):
    įstaiga = P(ValstybinėĮstaiga)
    pareigos = P(Profesija)


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


class Santuoka(Laikotarpis):
    sutuoktinis = P("Sutuoktinis", Asmuo)


class ValstybėsTarnautojas(Asmuo):
    pareigos = P(Pareigos, 'ValstybėsTarnautojoUžimamosPareigos', m2mbref='tarnautojas')


class ValstybėsTarnautojoUžimamosPareigos(UžimamosPareigos):
    tarnautojas = P(ValstybėsTarnautojas, sameas='asmuo')
    įstaiga = P(ValstybinėĮstaiga, sameas='grupė')
    el_paštas = P(str)
    tel_nr = P(str)


class SandorioŠalis(Kvalifikatorius):
    veiksmas = P(str)


class Sandoris(Objektas):
    šalis = P(Asmuo, SandorioŠalis)
    vertė = P(PinigųKiekis)
    data = P(DataLaikas)
    objektas = P(Objektas)


class ValstybesTarnautojoSandoris(Sandoris):
    šalis = P(ValstybėsTarnautojas, SandorioŠalis)


class Darbuotojas(Narystė):
    darbuotojas = P(Asmuo, sameas='narys')
    darbovietė = P(Įmonė, sameas='grupė')
    profesija = P(Profesija)
    el_paštas = P(str)
    tel_nr = P(str)
    adresas = P(Adresas)
    pajamos = P(PinigųKiekis)


class PolicijojeRegistruotasIvykis(Įvykis):
    rūšis = P(str)


class PartijosVadovas(Asmuo):
    pass


class Rinkimai(Įvykis):
    rūšis = P(str, choices=("prezidento", "seimo", "savivaldybių"))


class Partija(Grupė):
    trumpinys = P(str)
    rinkimai = P(Rinkimai)
    vadovas = P(PartijosVadovas)
    politinė_kryptis = P('str', ("kairė", "centro", "dešinė"))


class RinkimųEtapas(Įvykis):
    rinkimai = P(Rinkimai)


class RinkimųApygarda(Kontūras):
    pass


class RinkimųApylinkė(Kontūras):
    apygarda = P(RinkimųApygarda)
    pastatas = P(Pastatas)


class RinkimųKandidatas(Asmuo):
    partija = P(Partija)
    sandoris = P(Laikotarpis)
    rinkimai = P(Rinkimai)
    eilė_sąraše = P(int)
    sąrašas = P(str)


class Frakcija(Grupė):
    trumpinys = P(str)
    partija = P(Partija)


class SeimoKadencija(Laikotarpis):
    pass


class SeimoNarys(ValstybėsTarnautojas):
    frakcija = P(Frakcija, 'FrakcijosNarys', m2mbref='narys')
    partija = P(Partija, 'SeimoNarioPartija', m2mbref='narys')
    mandatas = P(SeimoKadencija, 'SeimoNarioMandatas', m2mbref='seimo_narys')


class SeimoNarioMandatas(Laikotarpis):
    seimo_narys = P(SeimoNarys)
    kadencija = P(SeimoKadencija)


class FrakcijosNarys(Narystė):
    frakcija = P(Frakcija, sameas='grupė')
    seimo_narys = P(SeimoNarys, sameas='narys')


class SeimoNarioPartija(Narystė):
    seimo_narys = P(SeimoNarys, sameas='narys')
    partija = P(Partija, sameas='grupė')


class Dokumentas(Objektas):
    dokumento_tekstas = P("Dokumento tekstas")


class DokumentoElementas(Objektas):
    dokumentas = P(Dokumentas)
    kamienas = P('self', comments="Kamieninis (tėvinis) dokumento elementas.")
    ankstesnis = P('self', comments="Prieš šį elementą einantis elementas.")
    sekantis = P('self', comments="Po šio elemento einantis elementas.")
    pakeičia = P('self', comments="Šis elementas pakeičia seną elementą.")
    pakeistas = P('self', comments="Šis elemntas yra pakeistas nauju elementu.")
    tipas = P(str, comments="Dokumento paragrafo tipas.", choices=(
        'text',
        'p', 'quote',
        'ol', 'ul', 'li',
        'table', 'tr', 'th', 'td',
        'h1', 'h2', 'h3', 'h4', 'h5',
        'removed',
    ))


class EurovocTerminas(KategorijųMedžioŠaka):
    pass


class TeisėsAktas(Dokumentas):
    rūšis = P(str)
    numeris = P(str)
    paskelbimo_data = P(Data)
    įsigaliojimo_data = P(Data)
    eurovoc_terminas = P(str)


class TeisėsAktoElementas(DokumentoElementas):
    teisės_aktas = P(TeisėsAktas, sameas='dokumentas')
    tipas = P(str, choices=DokumentoElementas.tipas.choices + ('straipsnis'))


class SeimeSvarstytasTeisėsAktas(Objektas):
    klausimas = P('SeimeSvarstytasKlausimas')
    teisės_aktas = P(TeisėsAktas)
    teisės_akto_elementas = P(TeisėsAktoElementas)
    etapas = P("Klausimo svarstymo etapas", choices=("pateikimas", "svarstymas", "priėmimas"))


class SeimeSvarstytasKlausimas(Objektas):
    pranešėjas = P('SeimeSvartytoKlausimoPranešėjas', backref='klausimas')
    teisės_aktas = P(TeisėsAktas, SeimeSvarstytasTeisėsAktas, m2mbref='klausimas')


class SeimeSvartytoKlausimoPranešėjas(Asmuo):
    klausimas = P(SeimeSvarstytasKlausimas)


class SeimoBalsavimas(Objektas):
    laikas = P(DataLaikas)
    klausimas = P(SeimeSvarstytasKlausimas, comments="Klausimas dėl kurio buvo balsuota.")
    teisės_aktas = P(TeisėsAktas)
    teisės_akto_elementas = P(TeisėsAktoElementas)


class BalsavimoFormuluočiųGrupė(Objektas):
    pass


class BalsavimoFormuluotė(Objektas):
    grupė = P(BalsavimoFormuluočiųGrupė)


class Balsas(Objektas):
    reikšmė = P(str, choices=("už", "susilaikė", "prieš"))
    formuluotė = P(BalsavimoFormuluotė, comment="Formuluotė už kurią buvo balsuojama.")
    laikas = P(DataLaikas)
    seimo_narys = P(SeimoNarys)
    frakcija = P(Frakcija)
    balsavimas = P(SeimoBalsavimas)
    užsiregistravo = P(bool)
    klausimas = P(SeimeSvarstytasKlausimas)


class Pasisakymas(Objektas):
    laikas = P(DataLaikas)
    asmuo = P(Asmuo)


class AsmuoPasisakęsSeimoPosėdžioMetu(Asmuo):
    pass


class PasisakymasStenogramoje(Pasisakymas):
    asmuo = P(AsmuoPasisakęsSeimoPosėdžioMetu)
    pirmininkas = P(bool)
    klausimas = P(SeimeSvarstytasKlausimas, comments="Klausimas apie kurį buvo kalbėta.")
    teisės_aktas = P(TeisėsAktas)
    teisės_akto_elementas = P(TeisėsAktoElementas)


class StatistinisRodiklis(Laikotarpis):
    meta = Meta("Statistinis rodiklis")

    # https://www.w3.org/TR/vocab-data-cube/
    dimensija = P("Dimensija")
    atributas = P("Atributas")
    reiksme = P("Reikšmė")
    matavimo_vienetas = P("Matavimo vienetas")


class Bankrotas(Įvykis):
    įmonė = P(Įmonė)
    iniciatorius = P(str, choices=(
        "darbuotojai",
        "kreditoriai",
        "likvidatorius",
        "vadovas",
        "savininkai",
        "vmi",    # Valstybinė mokesčių inspekcija
        "vsdfv",  # Valstybinio socialinio draudimo fondo valdyba
    ))
    išieškomos_skolos_dalis = P(PinigųKiekis)
    nutarties_priėmimo_data = P(Data)
    supaprastinta_tvarka = P(bool)
    teismo_tvarka = P(bool)


class PrekiųPaslaugųKategorija(KategorijųMedžioŠaka):
    pass


class PrekėPaslauga(Objektas):
    kategorija = P(PrekiųPaslaugųKategorija)
    vidutinė_rinkos_vertė = P(PinigųKiekis, comment="Prekės ar paslaugos vieneto vidutinė rinkos vertė.")


class Projektas(Įvykis):
    sritis = P(VeiklosSritis)
    vykdytojas = P(Agentas)
    biudžetas = P(PinigųKiekis)
    parama = P('Parama', backref='projektas')
    prašomos_paramos_suma = P(PinigųKiekis)


class Parama(Objektas):
    projektas = P(Projektas)
    teikėjas = P(Agentas)
    suma = P(PinigųKiekis)


class ValstybinioProjektoParamosTeikėjas(Agentas):
    pass


class ValstybinisProjektas(Projektas):
    vykdytojas = P(ValstybinėĮstaiga)
    parama = P('ValstybinioProjektoParama', backref='projektas')


class ValstybinioProjektoParama(Parama):
    projektas = P(ValstybinisProjektas)
    teikėjas = P(ValstybinioProjektoParamosTeikėjas)


class ViešojoPirkimoDalyvis(Agentas):
    pass


class ViešasisPirkimas(Laikotarpis):
    # http://standard.open-contracting.org/
    projektas = P(Projektas, backref='vykdytojas')
    pirkėjas = P(ValstybinėĮstaiga)
    tiekėjas = P(ViešojoPirkimoDalyvis, 'DalyvavimasViešajamePirkime', m2mbref='pirkimas')
    etapas = P(str, choices=("nuostatai", "specifikacija", "įgyvendinimas"))
    suma = P(PinigųKiekis, comment="Viešojo pirkimo sandorio suma.")
    žymė = P(str)


class DalyvavimasViešajamePirkime(Laikotarpis):
    dalyvis = P(ViešojoPirkimoDalyvis)
    pirkimas = P(ViešasisPirkimas)
    laimėtojas = P(bool, comment="Viešojo pirkimo konkurso laimėtojas.")


class ViešojoPirkimoLėšųPanaudojimas(Objektas):
    pirkimas = P(ViešasisPirkimas)
    tiekėjas = P(Agentas)
    objektas = P(PrekėPaslauga)
    kiekis = P(Kiekis)
    suma = P(PinigųKiekis, comment="Perkamo objekto vieneto kaina.")


class MetrikųKnyga(Objektas):
    laikotarpis = P("Laikotarpis")
    pastatas = P("Pastatas")
    skaitmeninimo_data = P("Skaitmeninimo data")


class MetrikuKnygosLapas(Objektas):
    metrikų_knyga = P("Metrikų knyga", MetrikųKnyga)
    lapo_numeris = P("Lapo numeris")
    lapo_paveiksliukas = P("Lapo paveiksliukas")


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


class Susirgimas(Įvykis):
    liga = P("Liga")
    asmuo = P("Asmuo", Asmuo)


class TelefonoRegistracijaPrieMobTinklo(Įvykis):
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
