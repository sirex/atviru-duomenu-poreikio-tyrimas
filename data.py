class P:

    def __init__(self, type, qualifier=None, *, choices=None, wikidata=None,
                 comment=None, m2mref=None, backref=None, same_as=None):
        self.type = type
        self.qualifier = qualifier
        self.choices = choices
        self.wikidata = wikidata
        self.comment = comment


class Meta:

    def __init__(self, title=None, wikidata=None):
        self.title = title
        self.wikidata = wikidata


# Base classes

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
    laiko_juosta = P(str)


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

class Laikotarpis(Objektas):
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
    gatvė = P(Gatvė)
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


class Įvykis(Laikotarpis):
    adresas = P(Adresas)


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


class KategorijųMedis(Objektas):
    pass


class KategorijųMedžioŠaka(Objektas):
    medis = P(KategorijųMedis)
    kamienas = P('self')


class VeiklosSritiesKategorijųMedis(KategorijųMedis):
    pass


class VeiklosSritis(KategorijųMedžioŠaka):
    pass


class Agentas(Objektas):
    registracijos_numeris = P(str)
    paveiksliukas = P(str)
    adresas = P(Adresas, Laikotarpis)
    teisinė_forma = P(TeisinėForma)
    veiklos_sritis = P(VeiklosSritis)


class Asmuo(Agentas):
    meta = Meta(wikidata='Q5')
    lytis = P(str, wikidata='P21', choices=("vyras", "moteris"))
    asmens_kodas = P(str, same_as='registracijos_numeris')
    vardas = P(Objektas, Laikotarpis)
    pavardė = P(Objektas, Laikotarpis)
    gimimo_data = P(DataLaikas)
    mirties_data = P(DataLaikas)
    nuotrauka = P(Paveiksliukas, Laikotarpis, same_as='paveiksliukas')
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
    asmuo = P(Asmuo)


class Narystė(Laikotarpis):
    narys = P(Agentas)
    grupė = P(Agentas)
    pareigos = P(Pareigos, 'UžimamosPareigos', m2mref='grupė')


class Grupė(Agentas):
    vadovas = P(Asmuo)
    logotipas = P(str, same_as='paveiksliukas')
    įkurta = P(DataLaikas)
    likviduota = P(DataLaikas)
    narys = P(Agentas, Narystė, m2mref='grupė')


class UžimamosPareigos(Laikotarpis):
    asmuo = P(Asmuo)
    grupė = P(Grupė)
    pareigos = P(Pareigos)
    pakeičia = P(Asmuo, wikidata='P1365', comment="Pakeičia ansčiau pareigas ėjusį asmenį.")
    pakeistas = P(Asmuo, wikidata='P1366', comment="Buvo pakeistas vėliau šias pareigas užėmusio asmens.")


class JuridinioAsmensAdresas(Adresas):
    pass


class JuridinisAsmuo(Grupė):
    pastatas = P(Pastatas, Laikotarpis)
    el_paštas = P(str, Laikotarpis)
    tel_nr = P(str, Laikotarpis)
    tinklapis = P(str, Laikotarpis)
    darbuotojų_skaičius = P(int, Laikotarpis, same_as='narių_skaičius')
    vidutinis_atlyginimas = P(PinigųKiekis, Laikotarpis)
    skola_sodrai = P(PinigųKiekis, Laikotarpis)
    įregistravimo_data = P(DataLaikas, same_as='įkurta')
    išregistravimo_data = P(DataLaikas, same_as='likviduota')
    direktorius = P(Asmuo, same_as='vadovas')
    adresas = P(JuridinioAsmensAdresas)


class Įmonė(JuridinisAsmuo):
    apyvarda = P(PinigųKiekis, Laikotarpis)
    akcininkas = P(Agentas)


class Akcininkas(Agentas):
    įmonė = P(Įmonė)
    akciju_dalis_įmonėje = P(Kiekis)


class ValstybinėsĮstaigosAdresas(Adresas):
    pass


class ValstybinėĮstaiga(JuridinisAsmuo):
    priklauso_įstaigai = P('self')
    adresas = P(ValstybinėsĮstaigosAdresas)


class MaitinimoĮstaigosSavininkas(JuridinisAsmuo):
    pass


class MaitinimoĮstaigosAdresas(Adresas):
    pass


class MaitinimoĮstaiga(Objektas):
    savininkas = P(Agentas)
    adresas = P(MaitinimoĮstaigosAdresas)


class PrekybosAlkoholiuLicencija(Laikotarpis):
    maitinimo_įstaiga = P(MaitinimoĮstaiga)


class MaitinimoĮstaiga(Objektas):
    """Pastatas, kuriame teikiamos maitinimo paslaugos (kavinė, baras, restorantas)."""
    savininkas = P(Įmonė)
    prekybos_alkoholiu_licencija = P(Objektas, Laikotarpis)
    adresas = P(Adresas)


class MokymoĮstaigosPastatas(Pastatas):
    pass


class MokymoĮstaigosAdresas(Adresas):
    pass


class MokymoĮstaigosGatvė(Gatvė):
    pass


class MokymoĮstaigosGyvenvietė(Gyvenvietė):
    pass


class MokymoĮstaigosSeniūnija(Seniūnija):
    pass


class MokymoĮstaigosSavivaldybė(Savivaldybė):
    pass


class MokymoĮstaiga(Objektas):
    institucijos_tipas = P(str, choices=("universitetas", "mokykla"))
    pastatas = P(MokymoĮstaigosPastatas)
    adresas = P(MokymoĮstaigosAdresas)


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
    pareigos = P(Pareigos, 'ValstybėsTarnautojoUžimamosPareigos', m2mref='tarnautojas')


class ValstybėsTarnautojoUžimamosPareigos(UžimamosPareigos):
    tarnautojas = P(ValstybėsTarnautojas, same_as='asmuo')
    įstaiga = P(ValstybinėĮstaiga, same_as='grupė')
    el_paštas = P(str)
    tel_nr = P(str)


class SandorioŠalis(Objektas):
    veiksmas = P(str)


class Sandoris(Objektas):
    šalis = P(Asmuo, SandorioŠalis)
    vertė = P(PinigųKiekis)
    data = P(DataLaikas)
    objektas = P(Objektas)


class ValstybesTarnautojoSandoris(Sandoris):
    šalis = P(ValstybėsTarnautojas, SandorioŠalis)


class Darbuotojas(Narystė):
    darbuotojas = P(Asmuo, same_as='narys')
    darbovietė = P(Įmonė, same_as='grupė')
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
    frakcija = P(Frakcija, 'FrakcijosNarys', m2mref='narys')
    partija = P(Partija, 'SeimoNarioPartija', m2mref='narys')
    mandatas = P(SeimoKadencija, 'SeimoNarioMandatas', m2mref='seimo_narys')


class SeimoNarioMandatas(Laikotarpis):
    seimo_narys = P(SeimoNarys)
    kadencija = P(SeimoKadencija)


class FrakcijosNarys(Narystė):
    frakcija = P(Frakcija, same_as='grupė')
    seimo_narys = P(SeimoNarys, same_as='narys')


class SeimoNarioPartija(Narystė):
    seimo_narys = P(SeimoNarys, same_as='narys')
    partija = P(Partija, same_as='grupė')


class Dokumentas(Objektas):
    dokumento_tekstas = P("Dokumento tekstas")


class DokumentoElementas(Objektas):
    dokumentas = P(Dokumentas)
    kamienas = P('self', comment="Kamieninis (tėvinis) dokumento elementas.")
    ankstesnis = P('self', comment="Prieš šį elementą einantis elementas.")
    sekantis = P('self', comment="Po šio elemento einantis elementas.")
    pakeičia = P('self', comment="Šis elementas pakeičia seną elementą.")
    pakeistas = P('self', comment="Šis elemntas yra pakeistas nauju elementu.")
    tipas = P(str, comment="Dokumento paragrafo tipas.", choices=(
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


class TeisėsDokumentoAktoElementas(DokumentoElementas):
    teisės_aktas = P(TeisėsAktas, same_as='dokumentas')
    tipas = P(str, choices=DokumentoElementas.tipas.choices + ('straipsnis',))


class SeimeSvarstytasTeisėsAktas(Objektas):
    klausimas = P('SeimeSvarstytasKlausimas')
    teisės_aktas = P(TeisėsAktas)
    teisės_akto_elementas = P(TeisėsDokumentoAktoElementas)
    etapas = P("Klausimo svarstymo etapas", choices=("pateikimas", "svarstymas", "priėmimas"))


# wordnet: entity / abstraction / communication / message / proposal / question
class SeimeSvarstytasKlausimas(Objektas):
    pranešėjas = P('SeimeSvartytoKlausimoPranešėjas', backref='klausimas')
    teisės_aktas = P(TeisėsAktas, SeimeSvarstytasTeisėsAktas, m2mref='klausimas')


# wordnet: entity / abstraction / psychological feature / event / human activity / activity / occupation / position
class SeimeSvartytoKlausimoPranešėjoPareigos(Pareigos):
    pass


# wordnet: entity / physical entity / object / unit / living thing / organism / person / communicator / articulator / speaker
class SeimeSvartytoKlausimoPranešėjas(Asmuo):
    klausimas = P(SeimeSvarstytasKlausimas)
    pareigos = P(SeimeSvartytoKlausimoPranešėjoPareigos, backref='asmuo')


# wordnet: entity / abstraction / psychological feature / event / human activity / action / choice / vote
# wikidata: event
# wikidata: group decision-making
# wikidata: legal action
class SeimoBalsavimas(Objektas):
    laikas = P(DataLaikas)
    klausimas = P(SeimeSvarstytasKlausimas, comment="Klausimas dėl kurio buvo balsuota.")
    teisės_aktas = P(TeisėsAktas)
    teisės_akto_elementas = P(TeisėsDokumentoAktoElementas)


# wordnet: entity / abstraction / group / collection
class BalsavimoFormuluočiųGrupė(Objektas):
    pass


# wordnet: entity / abstraction / psychological feature / knowledge / process / higher cognitive process / decision making / option
class BalsavimoFormuluotė(Objektas):
    grupė = P(BalsavimoFormuluočiųGrupė)


# wordnet: entity / abstraction / communication / message / opinion / position
# wikidata: action / human action / choice
class Balsas(Objektas):
    reikšmė = P(str, choices=("už", "susilaikė", "prieš"))
    formuluotė = P(BalsavimoFormuluotė, comment="Formuluotė už kurią buvo balsuojama.")
    laikas = P(DataLaikas)
    seimo_narys = P(SeimoNarys)
    frakcija = P(Frakcija)
    balsavimas = P(SeimoBalsavimas)
    užsiregistravo = P(bool)
    klausimas = P(SeimeSvarstytasKlausimas)


# wordnet: entity / abstraction / communication / message
class Pasisakymas(Objektas):
    laikas = P(DataLaikas)
    asmuo = P(Asmuo)


# wordnet: entity / physical entity / object / unit / living thing / organism / person / communicator / articulator / speaker
class AsmuoPasisakęsSeimoPosėdžioMetu(Asmuo):
    pass


# wordnet: entity / abstraction / communication / message
class PasisakymasStenogramoje(Pasisakymas):
    asmuo = P(AsmuoPasisakęsSeimoPosėdžioMetu)
    pirmininkas = P(bool)
    klausimas = P(SeimeSvarstytasKlausimas, comment="Klausimas apie kurį buvo kalbėta.")
    teisės_aktas = P(TeisėsAktas)
    teisės_akto_elementas = P(TeisėsDokumentoAktoElementas)


class StatistinisRodiklis(Laikotarpis):
    meta = Meta("Statistinis rodiklis")

    # https://www.w3.org/TR/vocab-data-cube/
    dimensija = P("Dimensija")
    atributas = P("Atributas")
    reikšmė = P("Reikšmė")
    matavimo_vienetas = P("Matavimo vienetas")


class BankrutuojančiosĮmonėsAdresas(Adresas):
    pass


class BankrutuojantiĮmonė(Įmonė):
    adresas = P(BankrutuojančiosĮmonėsAdresas)


class Bankrotas(Įvykis):
    įmonė = P(BankrutuojantiĮmonė)
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


class PrekiųPaslaugųKategorųMedis(KategorijųMedis):
    pass


class PrekiųPaslaugųKategorija(KategorijųMedžioŠaka):
    pass


# wordnet: entity / physical entity / object / unit / artifact / creation / product
# wordnet: entity / abstraction / psychological feature / event / human activity / activity / work / service
class PrekėPaslauga(Objektas):
    kategorija = P(PrekiųPaslaugųKategorija)
    vidutinė_rinkos_vertė = P(PinigųKiekis, comment="Prekės ar paslaugos vieneto vidutinė rinkos vertė.")


# wordnet: entity / abstraction / psychological feature / cognition / content / idea / plan
class Projektas(Įvykis):
    sritis = P(VeiklosSritis)
    vykdytojas = P(Agentas)
    biudžetas = P(PinigųKiekis)
    parama = P('Parama', backref='projektas')
    prašomos_paramos_suma = P(PinigųKiekis)


# wordnet: entity / abstraction / amount / system of measurement / measure / monetary system / money / fund
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
    tiekėjas = P(ViešojoPirkimoDalyvis, 'DalyvavimasViešajamePirkime', m2mref='pirkimas')
    etapas = P(str, choices=("nuostatai", "specifikacija", "įgyvendinimas"))
    suma = P(PinigųKiekis, comment="Viešojo pirkimo sandorio suma.")
    žymė = P(str)


class DalyvavimasViešajamePirkime(Laikotarpis):
    dalyvis = P(ViešojoPirkimoDalyvis)
    pirkimas = P(ViešasisPirkimas)
    laimėtojas = P(bool, comment="Viešojo pirkimo konkurso laimėtojas.")


class ViešojoPirkimoTiekėjasĮmonė(JuridinisAsmuo):
    pass


class ViešojoPirkimoTiekėjasFizinisAsmuo(Asmuo):
    pass


class ViešojoPirkimoLėšųPanaudojimas(Objektas):
    pirkimas = P(ViešasisPirkimas)
    tiekėjas = P(Agentas)  # ViešojoPirkimoTiekėjasĮmonė | ViešojoPirkimoTiekėjasFizinisAsmuo
    objektas = P(PrekėPaslauga)
    kiekis = P(Kiekis)
    suma = P(PinigųKiekis, comment="Perkamo objekto vieneto kaina.")


class MetrikųKnyga(Objektas):
    laikotarpis = P("Laikotarpis")
    pastatas = P("Pastatas")
    skaitmeninimo_data = P("Skaitmeninimo data")


class MetrikųKnygosLapas(Objektas):
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


class KultūrosVertybė(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")
    rusis = P("Rūšis")


class LietuviškasŽodis(Objektas):
    žodis = P("Žodis")
    žodžio_prasmės_aprašymas = P("Žodžio prasmės aprašymas")
    žodžio_naudojimo_pavyzdžiai = P("Žodžio naudojimo pavyzdžiai")
    gramatinė_forma = P("Gramatinė forma")
    kaitymas_kalbos_dalimis = P("Kaitymas kalbos dalimis")
    galimos_žodžio_formos = P("Galimos žodžio formos")
    žodžio_šaknis = P("Žodžio šaknis")
    semantinė_kategorija = P("Semantinė kategorija")


class SkambučiųRegistroĮrašas(Objektas):
    """Call data record (CDR)"""
    tel_nr = P("Tel. nr.")
    skambučio_pradžia = P("Skambučio pradžios data ir laikas")
    kada_atsiliepta = P("Kada atsiliepta, data ir laikas")
    kada_baigtas_pokalbis = P("Kada baigtas pokalbis, data ir laikas")


class Studijos(Objektas):
    pradžia = P(DataLaikas)
    pabaiga = P(DataLaikas)


class Studentas(Asmuo):
    studijavo = P(MokymoĮstaiga, Studijos)
    mokymo_įstaiga = P("Mokymo įstaiga", MokymoĮstaiga)
    šalis = P("Šalis")
    mokymo_įstaiga_iš_kurios_atvyko = P("Mokymo įstaiga iš kurios atvyko (užsieniečiams)")


class Liga(Objektas):
    pavadinimas = P("Pavadinimas")


class Susirgimas(Įvykis):
    liga = P("Liga")
    asmuo = P("Asmuo", Asmuo)


class Produktas(Objektas):
    kaina = P(PinigųKiekis)


class TelefonoModelis(PrekėPaslauga):
    pass


class ŠaliesPavadinimas(LietuviškasŽodis):
    pass


class Šalis(ErdvinisObjektas):
    pavadinimas = P(ŠaliesPavadinimas)
    iso_3166_kodas = P("Šalies ISO-3166 kodas")


class TelefonoRegistracijaPrieMobTinklo(Įvykis):
    """Visitor location register"""
    unikalus_įrenginio_identifikatorius = P(str)
    kilmės_šalis = P(Šalis)
    telefono_modelis = P(TelefonoModelis)


class Kapinės(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")
    adresas = P("Adresas", Adresas)
    tikejimas = P("Tikėjimas")


class Kapas(ErdvinisObjektas):
    kapines = P("Kapinės", Kapinės)
    nuotrauka = P("Nuotrauka")
    asmuo = P("Asmuo", Asmuo)


class LietuvosPilietis(Asmuo):
    registracijos_adresas = P("Registracijos adresas", Adresas)
    nuolatine_gyvenamoji_vieta = P("Nuolatinė gyvenamoji vieta", Adresas)


class ParkavimoAikstele(ErdvinisObjektas):
    kaina = P("Parkavimo kaina")
    darbo_laikas = P("Darbo laikas")
    laisvu_vietu_skaicius = P("Laisvų vietų skaičius")


class Stotelė(ErdvinisObjektas):
    pavadinimas = P("Pavadinimas")


class AutobusoStotelė(Stotelė):
    pass


class Marsrutas(Objektas):
    stotelė = P("Stotelė", Stotelė)
    laikas = P("Atvykimo į stotelę laikas", DataLaikas)


class FinansinėsOperacijosAgentas(Agentas):
    pass


class FinansinėOperacija(Objektas):
    suma = P("Suma")
    sąskaita = P("Sąskaita", choices=("pajamos", "išlaidos"))
    sritis = P(VeiklosSritis)
    objektas = P(PrekėPaslauga)
    subjektas = P(Agentas)
    laikas = P("Data ir laikas", DataLaikas)


class BiudžetoFiskalinisĮrašas(FinansinėOperacija):
    suma = P("Suma")
    sąskaita = P("Sąskaita", choices=("pajamos", "išlaidos"))
    sritis = P(VeiklosSritis)
    mokesčių_mokėtojas = P(JuridinisAsmuo)
    asignavimų_valdytojas = P(ValstybinėĮstaiga)
    laikas = P("Data ir laikas", DataLaikas)
    adresas = P("Adresas", Adresas)


class ValstybinėsĮstaigosFinOpSubjektasJuridinis(JuridinisAsmuo):
    pass


class ValstybinėsĮstaigosFinOpSubjektasFizinis(Asmuo):
    pass


class ValstybinėsĮstaigosFinansinėOperacija(FinansinėOperacija):
    subjektas = P(ValstybinėsĮstaigosFinOpSubjektasJuridinis)  # arba ValstybinėsĮstaigosFinOpSubjektasFizinis
