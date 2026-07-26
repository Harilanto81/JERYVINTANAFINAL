import os
import math
from datetime import datetime, timedelta
import platform
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()

if platform.system() == 'Windows':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line

# ==========================================
# THÈMES ET PALETTE DE COULEURS JOYEUSE & VIVE
# ==========================================
T1_BG = (0.09, 0.05, 0.20, 1)
T1_CARD = (0.16, 0.09, 0.30, 1)
T1_BTN = (1.00, 0.42, 0.20, 1)
T1_BTN2 = (0.08, 0.82, 0.75, 1)

T2_BG = (0.26, 0.08, 0.06, 1)
T2_CARD = (0.36, 0.14, 0.07, 1)
T2_BTN = (1.00, 0.66, 0.05, 1)
T2_BTN2 = (1.00, 0.32, 0.30, 1)

T3_BG = (0.22, 0.05, 0.24, 1)
T3_CARD = (0.32, 0.10, 0.34, 1)
T3_BTN = (0.95, 0.15, 0.55, 1)
T3_BTN2 = (1.00, 0.55, 0.20, 1)

COLOR_INPUT_BG = (0.20, 0.13, 0.34, 1)
COLOR_INPUT_BORDER = (0.55, 0.38, 0.85, 1)
COLOR_INPUT_ACTIVE = (1.00, 0.55, 0.20, 1)

mois_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
annees_list = [str(y) for y in range(datetime.now().year, 1899, -1)]
heures_list = [f"{i:02d}h" for i in range(0, 24)]
minutes_list = [f"{i:02d}" for i in range(0, 60)]

SIGNATURE_TEXT = "[i][color=909090]Novokarin'i Harilanto Fidinirina, Facebook Fotoana Mety 034 90 906 25[/color][/i]"

# ==========================================
# FONCTIONS DE CALCUL 
# ==========================================
def reduire_nombre(nombre):
    while nombre > 9:
        if nombre in [11, 22, 33]: break
        nombre = sum(int(stat) for stat in str(nombre))
    return nombre

def calculer_signe_solaire(jour, mois):
    if (mois == 3 and jour >= 21) or (mois == 4 and jour <= 19): return "Alahamady (Bélier)"
    elif (mois == 4 and jour >= 20) or (mois == 5 and jour <= 20): return "Adaoro (Taureau)"
    elif (mois == 5 and jour >= 21) or (mois == 6 and jour <= 20): return "Adizaoza (Gémeaux)"
    elif (mois == 6 and jour >= 21) or (mois == 7 and jour <= 22): return "Asorotany (Cancer)"
    elif (mois == 7 and jour >= 23) or (mois == 8 and jour <= 22): return "Alahasaty (Lion)"
    elif (mois == 8 and jour >= 23) or (mois == 9 and jour <= 22): return "Asombola (Vierge)"
    elif (mois == 9 and jour >= 23) or (mois == 10 and jour <= 22): return "Adimizana (Balance)"
    elif (mois == 10 and jour >= 23) or (mois == 11 and jour <= 21): return "Alakarabo (Scorpion)"
    elif (mois == 11 and jour >= 22) or (mois == 12 and jour <= 21): return "Alakaosy (Sagittaire)"
    elif (mois == 12 and jour >= 22) or (mois == 1 and jour <= 19): return "Adijady (Capricorne)"
    elif (mois == 1 and jour >= 20) or (mois == 2 and jour <= 18): return "Adalo (Verseau)"
    elif (mois == 2 and jour >= 19) or (mois == 3 and jour <= 20): return "Alohotsy (Poissons)"
    return "Tsy fantatra"

def calculer_signe_lunaire(date_objet):
    utc_time = date_objet - timedelta(hours=3)
    year = utc_time.year; month = utc_time.month
    day = utc_time.day + (utc_time.hour + utc_time.minute/60.0 + utc_time.second/3600.0) / 24.0
    if month <= 2: year -= 1; month += 12
    A = year // 100; B = 2 - A + A // 4
    JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    T = (JD - 2451545.0) / 36525.0
    L0 = 218.316 + 481267.8813 * T; M = 134.963 + 477198.8676 * T
    F = 93.272 + 483202.0175 * T; D = 297.850 + 445267.11135 * T
    longitude = L0 + 6.289 * math.sin(math.radians(M)) - 1.274 * math.sin(math.radians(M - 2 * D)) + 0.658 * math.sin(math.radians(2 * D))
    longitude = longitude % 360
    signs = [(0, "Alahamady (Bélier)"), (30, "Adaoro (Taureau)"), (60, "Adizaoza (Gémeaux)"), (90, "Asorotany (Cancer)"), (120, "Alahasaty (Lion)"), (150, "Asombola (Vierge)"), (180, "Adimizana (Balance)"), (210, "Alakarabo (Scorpion)"), (240, "Alakaosy (Sagittaire)"), (270, "Adijady (Capricorne)"), (300, "Adalo (Verseau)"), (330, "Alohotsy (Poissons)")]
    signe_nom = "Tsy fantatra"
    for deg, nom in reversed(signs):
        if longitude >= deg: signe_nom = nom; break
    return signe_nom

def calculer_chemin_de_vie(date_texte):
    chiffres = [int(char) for char in date_texte if char.isdigit()]
    addition_format = "+".join(str(c) for c in chiffres)
    somme_reduite = reduire_nombre(sum(chiffres))
    elements = {1: "Afo (Feu)", 2: "Rano (Eau)", 3: "Rivotra (Air)", 4: "Tany (Terre)", 5: "Rivotra (Air)", 6: "Tany (Terre)", 7: "Rano (Eau)", 8: "Afo (Feu)", 9: "Afo (Feu)", 11: "Rivotra (Air - Maitre)", 22: "Tany (Terre - Maitre)", 33: "Afo (Feu - Maitre)"}
    interpretations = {1: "Olon'ny asa.", 2: "Mpiara-miasa tsara.", 3: "Mahay mamorona.", 4: "Mpanorina mahatoky.", 5: "Mpitady fivoarana.", 6: "Mpitantana fianakaviana.", 7: "Mpitady fahalalana.", 8: "Mitady fahombiazana.", 9: "Mpanasoa fiarahamonina.", 11: "Isambitana Mahery.", 22: "Isambitana Mahery.", 33: "Isambitana Mahery."}
    return addition_format, somme_reduite, elements.get(somme_reduite, "Tsy fantatra"), interpretations.get(somme_reduite, "Tsy misy fanazavana.")

def calculer_details_lune(date_objet):
    utc_time = date_objet - timedelta(hours=3)
    date_reference = datetime(2000, 1, 6, 18, 14, 0)
    delta_seconds = (utc_time - date_reference).total_seconds()
    delta_jours = delta_seconds / 86400.0
    cycle_lunaire = 29.530588853
    age_lune = delta_jours % cycle_lunaire
    angle = 2 * math.pi * age_lune / cycle_lunaire
    luminosite = round((1 - math.cos(angle)) / 2 * 100)
    if age_lune < 1.84566: repartition = "Maizim-bolana (Nouvelle Lune)"
    elif age_lune < 5.53699: repartition = "Tsinanan-kerinandro (Premier Croissant)"
    elif age_lune < 9.22831: repartition = "Miaka-bolana (Premier Quartier)"
    elif age_lune < 12.91964: repartition = "Mivoitra ho Diavolana (Gibbeuse Croissante)"
    elif age_lune < 16.8: repartition = "Diavolana (Pleine Lune)"
    elif age_lune < 20.30229: repartition = "Midim-bolana mihena (Gibbeuse Décroissante)"
    elif age_lune < 23.99362: repartition = "Midim-bolana (Dernier Quartier)"
    else: repartition = "Midim-bolana farany (Dernier Croissant)"
    return luminosite, repartition, age_lune

# FONCTIONS POUR LA COMPATIBILITÉ FIFANAMBINANA
def check_crossed_opposition(reni_l, zana_l, reni_v, zana_v):
    def get_core(signe):
        try:
            s = signe.split('(')[1].replace(')', '').strip().upper()
            s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii')
            return s.replace("POISSON", "POISSONS")
        except: return ""
    rl = get_core(reni_l); zl = get_core(zana_l); rv = get_core(reni_v); zv = get_core(zana_v)
    signs_map = {"BELIER": 1, "TAUREAU": 2, "GEMEAUX": 3, "CANCER": 4, "LION": 5, "VIERGE": 6, "BALANCE": 7, "SCORPION": 8, "SAGITTAIRE": 9, "CAPRICORNE": 10, "VERSEAU": 11, "POISSONS": 12}
    idx_rl = signs_map.get(rl); idx_zl = signs_map.get(zl); idx_rv = signs_map.get(rv); idx_zv = signs_map.get(zv)
    def is_opp(id1, id2):
        if id1 is None or id2 is None: return False
        return (id1 + 6) % 12 == id2 % 12
    if is_opp(idx_rl, idx_rv): return True
    if is_opp(idx_rl, idx_zv): return True
    if is_opp(idx_zl, idx_rv): return True
    if is_opp(idx_zl, idx_zv): return True
    return False

def get_tanjaka_status(reni, zana, age_lune):
    try:
        reni_core = unicodedata.normalize('NFD', reni.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
        zana_core = unicodedata.normalize('NFD', zana.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
        rang = TANJAKA_TABLE.get((reni_core, zana_core), 0)
    except: rang = 0
    if age_lune >= 14.8 and age_lune < 16.8: return "FISA-BINTANA"
    elif rang < 72: return "MATANJAKA"
    else: return "MALEFAKA"

def get_tanjaka_interp(status_l, status_v):
    if status_l == "MATANJAKA" and status_v == "MATANJAKA":
        return "Samy manana vintana matanjaka ka sady afaka miara-miasa tsara mba hampitombo be ny fahombiazana no mahomby, raha samy manana ny asa dia misy vokany tsara ihany koa"
    elif status_l == "MATANJAKA" or status_v == "MATANJAKA":
        return "Mandeha ila ny tanjaky ny vintana ka ilay manana Vintana matanjaka dia tokony omena sehatra malalaka mba handraharaha sy hampidi-vola"
    elif status_l == "MALEFAKA" and status_v == "MALEFAKA":
        return "Samy malefaka ny vintana ka samy mila miasa mafy vao ahita fahombiazana"
    elif status_l == "FISA-BINTANA" or status_v == "FISA-BINTANA":
        return "Misavika ny vintan'ilay manana vintana tsy misy olana ilay fisa-bintana ka mila matanjaka ilay vintana iray raha te ahita fahombiazana"
    else: return ""

def combine_elements(el1, el2):
    e1 = el1.split()[0].upper()
    e2 = el2.split()[0].upper()
    if (e1 == "AFO" and e2 == "AFO") or (e1 == "RIVOTRA" and e2 == "RIVOTRA") or (e1 == "RANO" and e2 == "RANO") or (e1 == "TANY" and e2 == "TANY"): return "TANY"
    if (e1 == "AFO" and e2 == "RANO") or (e1 == "RIVOTRA" and e2 == "TANY") or (e1 == "RANO" and e2 == "AFO") or (e1 == "TANY" and e2 == "RIVOTRA"): return "RIVOTRA"
    if (e1 == "AFO" and e2 == "RIVOTRA") or (e1 == "RIVOTRA" and e2 == "AFO") or (e1 == "RANO" and e2 == "TANY") or (e1 == "TANY" and e2 == "RANO"): return "RANO"
    if (e1 == "AFO" and e2 == "TANY") or (e1 == "RIVOTRA" and e2 == "RANO") or (e1 == "RANO" and e2 == "RIVOTRA") or (e1 == "TANY" and e2 == "AFO"): return "AFO"
    return ""

def deduce_fifamabinana(el1, el2):
    e1 = el1.upper()
    e2 = el2.upper()
    combos = {
        ("AFO", "AFO"): "TAREKY", ("AFO", "RIVOTRA"): "KARIJA", ("AFO", "RANO"): "ALAKASAZY", ("AFO", "TANY"): "ALAHASADY",
        ("RIVOTRA", "AFO"): "ALAKARABO", ("RIVOTRA", "RIVOTRA"): "ADALO", ("RIVOTRA", "RANO"): "ALOKOLA", ("RIVOTRA", "TANY"): "ALIHIZANA",
        ("RANO", "AFO"): "ALAKAOSY", ("RANO", "RIVOTRA"): "ALATSIMAY", ("RANO", "RANO"): "ALOHOTSY", ("RANO", "TANY"): "ALAIMORA",
        ("TANY", "AFO"): "ADABARAY", ("TANY", "RIVOTRA"): "ALEBIAVO", ("TANY", "RANO"): "ALIKISY", ("TANY", "TANY"): "ASOMBOLA"
    }
    return combos.get((e1, e2), "")

def interpret_fifamabinana(result):
    if result in ["TAREKY", "ASOMBOLA", "ALATSIMAY"]:
        return "ANTONONY", "Tsy misy olana lehibe, antonony ny fifanaraka."
    elif result in ["ADABARAY", "ALAHASADY", "ALAKARABO", "ALAKASAZY", "ALEBIAVO", "ALIHIZANA", "ALAKAOSY"]:
        return "TSARA", "Mahay miaraka ny singa ka tsy avy ao anatin'ny tokantrano mihitsy no ihavian'ny olana fa avy any ivelany raha hisy."
    else:
        return "RATSY", "Tsy mahay miaraka ny singa ka misy ady matetika sy tsy fifankazahoan-kevitra"

# ==========================================
# FONCTIONS DE RÉSUMÉ (FAMINTINANA)
# ==========================================
def calculer_isambitana_glob(nom_complet):
    table_lettres = {chr(i): (i - 64) % 9 if (i - 64) % 9 != 0 else 9 for i in range(65, 91)}
    nom_nettoye = nom_complet.upper().replace(" ", "")
    valeurs = [table_lettres[l] for l in nom_nettoye if l in table_lettres]
    if not valeurs: return "0", 0, "Tsy hita", "Tsy misy anarana voasoratra."
    somme_reduite = reduire_nombre(sum(valeurs))
    elements = {1: "Afo (Feu)", 2: "Rano (Eau)", 3: "Rivotra (Air)", 4: "Tany (Terre)", 5: "Rivotra (Air)", 6: "Tany (Terre)", 7: "Rano (Eau)", 8: "Afo (Feu)", 9: "Afo (Feu)", 11: "Rivotra (Air - Maitre)", 22: "Tany (Terre - Maitre)", 33: "Afo (Feu - Maitre)"}
    interpretations = {1: "Olon'ny asa.", 2: "Mpiara-miasa tsara.", 3: "Mahay mamorona.", 4: "Mpanorina mahatoky.", 5: "Mpitady fivoarana.", 6: "Mpitantana fianakaviana.", 7: "Mpitady fahalalana.", 8: "Mitady fahombiazana.", 9: "Mpanasoa fiarahamonina.", 11: "Isambitana Mahery.", 22: "Isambitana Mahery.", 33: "Isambitana Mahery."}
    return somme_reduite, elements.get(somme_reduite, "Tsy fantatra"), interpretations.get(somme_reduite, "Tsy misy fanazavana.")

def get_moon_interp(age_lune):
    if age_lune < 1.3: aspect = "Maizim-bolana"; interp = "Teraka maizim-bolana ianao ka somary sahirana rehefa manainga fikasana na mitady vahaolana, be hevitra fa vitsy ny ho tanteraka"
    elif age_lune < 7.4: aspect = "Miaka-bolana (ambany hazavany)"; interp = "Teraka miaka-bolana ianao saingy mbola ambany hazavany ka mora aminao ny manainga fikasana na mitady vahaolana fa tsy mahatsangana zavatra vetivety"
    elif age_lune < 14.8: aspect = "Mazava volana be"; interp = "Teraka mazava volana be ianao ka sady mora aminao ny manainga fikasana na mitady vahaolana sady vetivety dia mahatsangana sy mahasoa zavatra"
    elif age_lune < 16.8: aspect = "Diavolana"; interp = "Teraka Diavolana ianao ka tsy takona afenina fa mora misongandina sy tazana saingy misy olana ny vintana fa mifanoto ka mahatonga olana betsaka eo amin'ny fiainanao, FISA-BINTANA no filaza azy"
    elif age_lune < 23.1: aspect = "Mazava volana (midina ny hazavany)"; interp = "Teraka mazava volana ianao fa midina ny hazavany ka mora aminao ny manainga fikasana na mitady vahaolana sady vetivety dia mahatsangana fa tsy mahasoa zavatra sady tsy mahatan-javatra fa mora mamotsotra"
    else: aspect = "Manakaiky ny maizim-bolana"; interp = "Teraka manakaiky ny maizim-bolana ianao ka somary sahirana rehefa manainga fikasana na mitady vahaolana, be hevitra fa vitsy ny ho tanteraka"
    return aspect, interp

def calculate_lesoka(reni, zana, elem_dest, elem_cdv, andro_gasy):
    elem_reni, _ = SIGNES_DATA.get(reni, ("", ""))
    elem_zana, _ = SIGNES_DATA.get(zana, ("", ""))
    elem_jour = JOUR_ELEMENTS.get(andro_gasy, "Tsy fantatra")
    elem_reni_w = elem_reni.split()[0].upper() if elem_reni else "TSY FANTATRA"
    elem_zana_w = elem_zana.split()[0].upper() if elem_zana else "TSY FANTATRA"
    elem_dest_w = elem_dest.split()[0].upper() if elem_dest else "TSY FANTATRA"
    elem_cdv_w = elem_cdv.split()[0].upper() if elem_cdv else "TSY FANTATRA"
    elem_jour_w = elem_jour.split()[0].upper() if elem_jour else "TSY FANTATRA"
    
    percents = {'AFO': 0, 'RANO': 0, 'RIVOTRA': 0, 'TANY': 0}
    if elem_reni_w in percents: percents[elem_reni_w] += 50
    if elem_zana_w in percents: percents[elem_zana_w] += 25
    if elem_dest_w in percents: percents[elem_dest_w] += 10
    if elem_cdv_w in percents: percents[elem_cdv_w] += 10
    if elem_jour_w in percents: percents[elem_jour_w] += 5
    
    conclusions = []
    effets = {'AFO': {'manque': "Tsy misy Afo: Tsy manana fanahy mavitrika sy fahamarinan-toerana, mora morandraina sy kamo.", 'exces': "Be loatra ny Afo: Moratezitra, tsy mahazaka tsy faneken-kevitra, mavesatra ny fahatsapana tena."}, 'RANO': {'manque': "Tsy misy Rano: Tsy mahay mifandray am-po, malaina amin'ny fihetseham-po, sarotra mandefa fitiavana.", 'exces': "Be loatra ny Rano: Mora sendra fiankinan-doha, be onjam-po, lasa tafintohina mora."}, 'RIVOTRA': {'manque': "Tsy misy Rivotra: Tsy tia fifandraisana, somary mitokana, mifikitra amin'ny fomba taloha.", 'exces': "Be loatra ny Rivotra: Tsy milamina, be fisainana tsy tanteraka, miresaka tsy misy farany."}, 'TANY': {'manque': "Tsy misy Tany: Tsy miorina, tia mandehandeha tsy misy tanjona, tsy mahay mitahiry.", 'exces': "Be loatra ny Tany: Mafy loha, manelingelina, lasa materialiste loatra sy milamina fongana."}}
    for elem, perc in percents.items():
        if perc >= 80: conclusions.append(f"Be loatra ny {elem}: " + effets[elem]['exces'])
        elif perc == 0: conclusions.append("Tsy misy " + elem + ": " + effets[elem]['manque'])
    if conclusions:
        return "\n".join(conclusions)
    return "Tsy misy lesoka lehibe, mifandray tsara ny singa rehetra ao aminao."

# ==========================================
# COMPOSANTS VISUELS MODERNISÉS
# ==========================================
class DynamicLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.valign = kwargs.get('valign', 'top')
        self.halign = kwargs.get('halign', 'left')
        self.size_hint_y = None
        self.bind(width=self.update_size, texture_size=self.update_height)
    def update_size(self, instance, value):
        pad_x = self.padding[0] if isinstance(self.padding, (list, tuple)) else 0
        self.text_size = (value - pad_x * 2, None)
    def update_height(self, instance, value):
        pad_y = self.padding[1] if isinstance(self.padding, (list, tuple)) else 0
        self.height = value[1] + pad_y * 2

class BarWidget(Widget):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6,])
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class ThemedBox(BoxLayout):
    def __init__(self, bg_color=T1_CARD, radius=[18,], padding=15, spacing=12, **kwargs):
        super().__init__(padding=padding, spacing=spacing, **kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class RoundedButton(Button):
    def __init__(self, bg_color=T1_BTN, radius=[14,], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.base_color = bg_color
        with self.canvas.before:
            self.btn_color = Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.btn_color.rgba = (self.base_color[0]*0.8, self.base_color[1]*0.8, self.base_color[2]*0.8, 1)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.btn_color.rgba = self.base_color
        return super().on_touch_up(touch)

class ThemedInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = COLOR_INPUT_BG
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (0.4, 0.7, 1, 1)
        self.padding = [12, 12, 12, 12]
        with self.canvas.after:
            self.border_color = Color(*COLOR_INPUT_BORDER)
            self.line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1.2)
        self.bind(pos=self.update_rect, size=self.update_rect, focus=self.on_focus)

    def update_rect(self, *args):
        self.line.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)

    def on_focus(self, instance, value):
        if value:
            self.border_color.rgba = COLOR_INPUT_ACTIVE
        else:
            self.border_color.rgba = COLOR_INPUT_BORDER

class ModernDateField(BoxLayout):
    def __init__(self, values, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.values = values
        
        self.btn = Button(text=str(values[0]) if values else "", 
                          background_normal='', background_down='', 
                          background_color=COLOR_INPUT_BG, color=(1, 1, 1, 1), 
                          font_size='14sp', halign='center', valign='middle')
        self.btn.bind(size=lambda i, v: setattr(self.btn, 'text_size', v))
        
        with self.btn.canvas.after:
            self.border_color = Color(*COLOR_INPUT_BORDER)
            self.line = Line(rounded_rectangle=(self.btn.x, self.btn.y, self.btn.width, self.btn.height, 10), width=1.2)
        self.btn.bind(pos=self.update_rect, size=self.update_rect)
        
        self.dropdown = DropDown(auto_width=False, width=self.width)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.btn, 'text', x))
        
        self.scroll = ScrollView(do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', size_hint=(1, None))
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=2)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        max_h = Window.height * 0.4
        self.scroll.height = max_h
        
        for value in values:
            b = Button(text=str(value), size_hint_y=None, height=44, 
                       background_normal='', background_down='', 
                       background_color=(0.20, 0.22, 0.32, 1), color=(1, 1, 1, 1), 
                       font_size='14sp', halign='center', valign='middle')
            b.bind(size=lambda i, v: setattr(b, 'text_size', v))
            b.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.grid.add_widget(b)
            
        self.scroll.add_widget(self.grid)
        self.dropdown.add_widget(self.scroll)
        
        self.btn.bind(on_release=self.dropdown.open)
        self.add_widget(self.btn)
        self.bind(width=self.update_dropdown_width)
        
    def update_dropdown_width(self, *args):
        self.dropdown.width = self.width
        
    def update_rect(self, instance, value):
        instance.canvas.after.clear()
        with instance.canvas.after:
            Color(*COLOR_INPUT_BORDER)
            Line(rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 10), width=1.2)
            
    @property
    def text(self):
        return self.btn.text

    @text.setter
    def text(self, val):
        self.btn.text = str(val)

# Data Tables & Consts
SIGNES_DATA = {
    "Alahamady (Bélier)": ("Afo (Feu)", "Olona mailaka, matanjaka, tia mandroso sy mpitarika olona, manana faharisihana be. Somary Pingapinga sy tsy mahandry tantana ary tsy tia ampiandrasina."),
    "Adaoro (Taureau)": ("Tany (Terre)", "Calme be, tsy taitaitra, mijoro amin'ny heviny ary sarotra resena lahatra, mafy ary azo itokiana, izay atombony tsy maintsy vitany, somary mafy loha, possessif, bedoika."),
    "Adizaoza (Gémeaux)": ("Rivotra (Air)", "Olona tia miresaka, mahay mandresy lahatra sy mivarotra amin'ny vava, lian-zavatra, mahay mis'adapte amin'ny situation misy, be fisalasalana. Somary be resaka kanefa betsaka amin'ny zavatra teneniny no tsy misy fotony."),
    "Asorotany (Cancer)": ("Rano (Eau)", "Manana intuition be, fantary avy hatrany vao misy olona hafahafa na mandainga, sarotin-zavatra sy saropiaro, tia ankohonana sy tia maka fotoana iarahana aminy. Mora tohina, be kiry."),
    "Alahasaty (Lion)": ("Afo (Feu)", "Olona mavitrika, jejojejo, manana créativité be ary tia miseho olona sy deraina ary ankasitrahana amin'ny zavara ataony, dedaka kely. Somary manana hambo ambony, tia fifaninanana ary tia manindry."),
    "Asombola (Vierge)": ("Tany (Terre)", "Mieritreritra be vao manao zavatra, mitandrina be ary mandinika sy manao drafitra vao miroso, tia manao critique mba hanatsarana zavatra. Be fitaintainana, somary perfectionniste sy matérialiste."),
    "Adimizana (Balance)": ("Rivotra (Air)", "Tia miresaka, vetivety dia mampita sy mampilaza vaovao, tia mifandray amin'ny mpiara-monina, be fisalasalana, somary tia tena na égoiste ary superficiel."),
    "Alakarabo (Scorpion)": ("Rano (Eau)", "Olona tafiditra be rehefa manao zavatra, mamita izay natomboka, mahery vaika ary mandindona be sy manana présence be, somary sokirina vao miresaka. Manao am-po be, somary manipulateur."),
    "Alakaosy (Sagittaire)": ("Afo (Feu)", "Tia mandehandeha, manana fijery lavitra sy mihabo, mahitsy firesaka be ary tsy tia olona miolakolana, tsy ampiandrasina. Kizitina, tsy ampy fitandremana."),
    "Adijady (Capricorne)": ("Tany (Terre)", "Olona manana vina lavitra, tompon'andraikitra, tia discipline sy mampandanja izany saingy somary pessimiste na manana fijery mihiba. Somary mangatsiaka na miavona, be fifehezana."),
    "Adalo (Verseau)": ("Rivotra (Air)", "Mahaleo tena, tsy tia miankina amin'olona, tia aventure sy mandehandeha, tia mikaroka zava-baovao, tia manampy olona ary tia miavaka kely amin'ny endrika ivelany. Somary mitokatokana, sarotra raisina."),
    "Alohotsy (Poissons)": ("Rano (Eau)", "Mpandrevirevy sy mpanonofy, raha tsy kotabaisina tsy mahavita zavatra haingana, manana sens artistique be ary liana amin'ny resaka ara-panahy. Mora rebirebena, tsy atokisana amin'ny vola.")
}

# ==========================================
# ICÔNES DES SIGNES ASTROLOGIQUES & DES ÉLÉMENTS (fichiers PNG)
# ==========================================
ICONS_DIR = os.path.join(BASE_DIR, 'icons')

ZODIAC_ICON_FILES = {
    "Alahamady (Bélier)": "signe_bel.png", "Adaoro (Taureau)": "signe_tau.png", "Adizaoza (Gémeaux)": "signe_gem.png",
    "Asorotany (Cancer)": "signe_can.png", "Alahasaty (Lion)": "signe_leo.png", "Asombola (Vierge)": "signe_vie.png",
    "Adimizana (Balance)": "signe_bal.png", "Alakarabo (Scorpion)": "signe_sco.png", "Alakaosy (Sagittaire)": "signe_sag.png",
    "Adijady (Capricorne)": "signe_cap.png", "Adalo (Verseau)": "signe_ver.png", "Alohotsy (Poissons)": "signe_poi.png",
}
ELEMENT_ICON_FILES = {"AFO": "feu.png", "RANO": "rano.png", "RIVOTRA": "rivotra.png", "TANY": "tany.png"}

def chemin_icone_signe(nom_signe):
    fichier = ZODIAC_ICON_FILES.get(nom_signe)
    if not fichier: return None
    chemin = os.path.join(ICONS_DIR, fichier)
    return chemin if os.path.exists(chemin) else None

def chemin_icone_element(nom_element):
    if not nom_element: return None
    cle = nom_element.split()[0].strip().upper()
    cle = unicodedata.normalize('NFD', cle).encode('ascii', 'ignore').decode('ascii')
    fichier = ELEMENT_ICON_FILES.get(cle)
    if not fichier: return None
    chemin = os.path.join(ICONS_DIR, fichier)
    return chemin if os.path.exists(chemin) else None

class IconImage(Image):
    def __init__(self, size_px=28, **kwargs):
        super().__init__(allow_stretch=True, keep_ratio=True, size_hint=(None, None), size=(size_px, size_px), **kwargs)
        if not self.source:
            self.opacity = 0
    def set_source(self, chemin):
        if chemin:
            self.source = chemin
            self.opacity = 1
        else:
            self.opacity = 0

JOUR_ELEMENTS = {"Alatsinainy": "Rano (Eau)", "Talata": "Afo (Feu)", "Alarobia": "Rivotra (Air)", "Alakamisy": "Afo (Feu)", "Zoma": "Rano (Eau)", "Sabotsy": "Tany (Terre)", "Alahady": "Afo (Feu)"}
TANJAKA_TABLE = {
    ("BELIER", "CANCER"): 1, ("BALANCE", "CAPRICORNE"): 2, ("CANCER", "BELIER"): 3, ("CAPRICORNE", "BALANCE"): 4, ("CANCER", "BALANCE"): 5, ("CAPRICORNE", "BELIER"): 6, ("BALANCE", "CANCER"): 7, ("BELIER", "CAPRICORNE"): 8, ("BELIER", "BELIER"): 9, ("CANCER", "CANCER"): 10, ("BALANCE", "BALANCE"): 11, ("CAPRICORNE", "CAPRICORNE"): 12, ("BELIER", "BALANCE"): 13, ("BALANCE", "BELIER"): 14, ("CANCER", "CAPRICORNE"): 15, ("CAPRICORNE", "CANCER"): 16, ("CANCER", "SAGITTAIRE"): 17, ("CAPRICORNE", "GEMEAUX"): 18, ("BALANCE", "TAUREAU"): 19, ("BELIER", "SCORPION"): 20, ("BELIER", "VIERGE"): 21, ("BELIER", "LION"): 22, ("CANCER", "SCORPION"): 23, ("BALANCE", "POISSONS"): 24, ("CAPRICORNE", "TAUREAU"): 25, ("BALANCE", "VERSEAU"): 26, ("CAPRICORNE", "POISSONS"): 27, ("BALANCE", "SAGITTAIRE"): 28, ("CANCER", "VIERGE"): 29, ("BALANCE", "SCORPION"): 30, ("BELIER", "SAGITTAIRE"): 31, ("CANCER", "VERSEAU"): 32, ("BALANCE", "GEMEAUX"): 33, ("CAPRICORNE", "LION"): 34, ("CAPRICORNE", "VIERGE"): 35, ("CANCER", "POISSONS"): 36, ("CANCER", "LION"): 37, ("CAPRICORNE", "VERSEAU"): 38, ("BELIER", "POISSONS"): 39, ("BALANCE", "VIERGE"): 40, ("BELIER", "GEMEAUX"): 41, ("BELIER", "TAUREAU"): 42, ("BELIER", "VERSEAU"): 43, ("CANCER", "TAUREAU"): 44, ("BALANCE", "LION"): 45, ("CAPRICORNE", "SCORPION"): 46, ("CANCER", "GEMEAUX"): 47, ("CAPRICORNE", "SAGITTAIRE"): 48, ("TAUREAU", "BALANCE"): 49, ("SCORPION", "BELIER"): 50, ("GEMEAUX", "CAPRICORNE"): 51, ("SAGITTAIRE", "CANCER"): 52, ("LION", "CAPRICORNE"): 53, ("VERSEAU", "CANCER"): 54, ("POISSONS", "CANCER"): 55, ("GEMEAUX", "BALANCE"): 56, ("VIERGE", "CAPRICORNE"): 57, ("SAGITTAIRE", "BELIER"): 58, ("TAUREAU", "CANCER"): 59, ("LION", "BALANCE"): 60, ("SCORPION", "CAPRICORNE"): 61, ("VERSEAU", "BELIER"): 62, ("POISSONS", "BALANCE"): 63, ("VIERGE", "BELIER"): 64, ("TAUREAU", "CAPRICORNE"): 65, ("LION", "BELIER"): 66, ("SCORPION", "CANCER"): 67, ("VERSEAU", "BALANCE"): 68, ("SAGITTAIRE", "BALANCE"): 69, ("VIERGE", "CANCER"): 70, ("POISSONS", "CAPRICORNE"): 71, ("SCORPION", "BALANCE"): 72, ("VIERGE", "BALANCE"): 73, ("LION", "CANCER"): 74, ("VERSEAU", "CAPRICORNE"): 75, ("POISSONS", "BELIER"): 76, ("GEMEAUX", "CANCER"): 77, ("SAGITTAIRE", "CAPRICORNE"): 78, ("GEMEAUX", "BELIER"): 79, ("TAUREAU", "BELIER"): 80, ("VIERGE", "VERSEAU"): 81, ("POISSONS", "LION"): 82, ("VERSEAU", "TAUREAU"): 83, ("LION", "SCORPION"): 84, ("GEMEAUX", "VIERGE"): 85, ("POISSONS", "SAGITTAIRE"): 86, ("VERSEAU", "VIERGE"): 87, ("SCORPION", "LION"): 88, ("LION", "TAUREAU"): 89, ("TAUREAU", "VERSEAU"): 90, ("VIERGE", "GEMEAUX"): 91, ("TAUREAU", "VIERGE"): 92, ("LION", "SAGITTAIRE"): 93, ("SCORPION", "POISSONS"): 94, ("SAGITTAIRE", "TAUREAU"): 95, ("VERSEAU", "GEMEAUX"): 96, ("TAUREAU", "LION"): 97, ("VIERGE", "SAGITTAIRE"): 98, ("SCORPION", "VERSEAU"): 99, ("SAGITTAIRE", "POISSONS"): 100, ("POISSONS", "GEMEAUX"): 101, ("VIERGE", "SCORPION"): 102, ("SAGITTAIRE", "VERSEAU"): 103, ("VERSEAU", "SAGITTAIRE"): 104, ("POISSONS", "TAUREAU"): 105, ("TAUREAU", "SAGITTAIRE"): 106, ("SCORPION", "GEMEAUX"): 107, ("SAGITTAIRE", "LION"): 108, ("GEMEAUX", "SCORPION"): 109, ("LION", "POISSONS"): 110, ("VIERGE", "TAUREAU"): 111, ("SAGITTAIRE", "VIERGE"): 112, ("SCORPION", "VIERGE"): 113, ("GEMEAUX", "LION"): 114, ("VERSEAU", "SCORPION"): 115, ("POISSONS", "SCORPION"): 116, ("GEMEAUX", "VERSEAU"): 117, ("GEMEAUX", "POISSONS"): 118, ("LION", "GEMEAUX"): 119, ("TAUREAU", "SCORPION"): 120, ("GEMEAUX", "SAGITTAIRE"): 121, ("LION", "VERSEAU"): 122, ("VIERGE", "POISSONS"): 123, ("SCORPION", "TAUREAU"): 124, ("SAGITTAIRE", "GEMEAUX"): 125, ("VERSEAU", "LION"): 126, ("POISSONS", "VIERGE"): 127, ("GEMEAUX", "TAUREAU"): 128, ("TAUREAU", "GEMEAUX"): 129, ("LION", "VIERGE"): 130, ("SCORPION", "SAGITTAIRE"): 131, ("VERSEAU", "POISSONS"): 132, ("TAUREAU", "POISSONS"): 133, ("VIERGE", "LION"): 134, ("SAGITTAIRE", "SCORPION"): 135, ("POISSONS", "VERSEAU"): 136, ("TAUREAU", "TAUREAU"): 137, ("GEMEAUX", "GEMEAUX"): 138, ("LION", "LION"): 139, ("VIERGE", "VIERGE"): 140, ("SCORPION", "SCORPION"): 141, ("SAGITTAIRE", "SAGITTAIRE"): 142, ("VERSEAU", "VERSEAU"): 143, ("POISSONS", "POISSONS"): 144
}

# ==========================================
# ÉCRANS DE L'APPLICATION
# ==========================================
class EcranAccueil(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T1_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl_titre = Label(text="[color=ffd700][b]JERY VINTANA[/b][/color]", markup=True, font_size='30sp', size_hint_y=0.12, halign='center')
        
        box_image = ThemedBox(bg_color=T1_CARD, orientation='vertical', size_hint_y=0.38, padding=10)
        img_path = os.path.join(BASE_DIR, 'Harilanto.jpg')
        if os.path.exists(img_path): 
            box_image.add_widget(Image(source=img_path, allow_stretch=True, keep_ratio=True))
        else: 
            box_image.add_widget(Label(text="[i]Tsy hita ny sary 'Harilanto.jpg'[/i]", markup=True, color=(1,0,0,1)))
            
        lbl_tongasoa = Label(text="[color=00ff88][b]Tongasoa[/b][/color]", markup=True, font_size='26sp', size_hint_y=0.08, halign='center')
        
        btn_vintana = RoundedButton(text="[b]HIJERY VINTANA[/b]", markup=True, bg_color=T1_BTN, color=(1,1,1,1), font_size='18sp', size_hint_y=0.1)
        btn_vintana.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_principal'))
        
        btn_fifam = RoundedButton(text="[b]HIJERY FIFANAMBINANA[/b]", markup=True, bg_color=T3_BTN, color=(1,1,1,1), font_size='18sp', size_hint_y=0.1)
        btn_fifam.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_fifamabinana'))
        
        lbl_sig = DynamicLabel(text=SIGNATURE_TEXT, font_size='11sp', halign='center', size_hint_y=0.1)
        
        layout.add_widget(lbl_titre)
        layout.add_widget(box_image)
        layout.add_widget(lbl_tongasoa)
        layout.add_widget(btn_vintana)
        layout.add_widget(btn_fifam)
        layout.add_widget(lbl_sig)
        self.add_widget(layout)
        
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class EcranPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T1_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]JERY VINTANA[/b][/color]\n[size=14sp]Astrologie & Numérologie[/size]", markup=True, font_size='22sp', size_hint_y=None, height=50, halign='center')

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=12)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        
        box_inputs = ThemedBox(bg_color=T1_CARD, orientation='vertical', size_hint_y=None, spacing=8)
        box_inputs.bind(minimum_height=box_inputs.setter('height'))
        
        lbl_date = Label(text="[b]DATY NAHATERAHANA[/b]", markup=True, halign='left', size_hint_y=None, height=20, font_size='13sp', color=(0.8, 0.8, 0.9, 1))
        row_date = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.spin_jour = ModernDateField(values=[str(i) for i in range(1, 32)], size_hint=(0.3, 1))
        self.spin_mois = ModernDateField(values=mois_list, size_hint=(0.4, 1))
        self.spin_annee = ModernDateField(values=annees_list, size_hint=(0.3, 1))
        row_date.add_widget(self.spin_jour); row_date.add_widget(self.spin_mois); row_date.add_widget(self.spin_annee)
        
        lbl_heure = Label(text="[b]ORA NAHATERAHANA[/b]", markup=True, halign='left', size_hint_y=None, height=20, font_size='13sp', color=(0.8, 0.8, 0.9, 1))
        row_heure = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)
        self.spin_heure = ModernDateField(values=heures_list, size_hint=(0.5, 1))
        self.spin_min = ModernDateField(values=minutes_list, size_hint=(0.5, 1))
        row_heure.add_widget(self.spin_heure); row_heure.add_widget(self.spin_min)
        
        lbl_nom = Label(text="[b]Anarana feno[/b]", markup=True, halign='left', size_hint_y=None, height=20, font_size='13sp', color=(0.8, 0.8, 0.9, 1))
        self.nom_input = ThemedInput(hint_text="Ohatra: Rakoto Jean", multiline=False, font_size='14sp', size_hint_y=None, height=44)
        
        lbl_lieu = Label(text="[b]Toerana nahaterahana[/b]", markup=True, halign='left', size_hint_y=None, height=20, font_size='13sp', color=(0.8, 0.8, 0.9, 1))
        self.lieu_input = ThemedInput(hint_text="Ohatra: Antananarivo", multiline=False, font_size='14sp', size_hint_y=None, height=44)
        
        box_inputs.add_widget(lbl_date); box_inputs.add_widget(row_date)
        box_inputs.add_widget(lbl_heure); box_inputs.add_widget(row_heure)
        box_inputs.add_widget(lbl_nom); box_inputs.add_widget(self.nom_input)
        box_inputs.add_widget(lbl_lieu); box_inputs.add_widget(self.lieu_input)
        
        self.btn_momba = RoundedButton(text="[b]NY MOMBA NY ANDRONAO[/b]", markup=True, bg_color=T1_BTN, color=(1,1,1,1), font_size='16sp', size_hint_y=None, height=50)
        self.btn_momba.bind(on_press=self.calculer_et_afficher_momba)

        self.result_label = DynamicLabel(text="[i]Tsindrio ny bokotra etsy ambany raha hijery ny vokatra.[/i]", font_size='14sp', color=(1, 1, 1, 1), padding=(10, 10))

        self.btn_vintanao = RoundedButton(text="[b]JEREO NY VINTANAO[/b]", markup=True, bg_color=T1_BTN2, color=(1,1,1,1), font_size='16sp', size_hint_y=None, height=50)
        self.btn_vintanao.bind(on_press=self.changer_ecran)
        
        btn_retour = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='15sp', size_hint_y=None, height=44)
        btn_retour.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_accueil'))
        
        conteneur.add_widget(box_inputs)
        conteneur.add_widget(self.btn_momba)
        conteneur.add_widget(self.result_label)
        conteneur.add_widget(self.btn_vintanao)
        conteneur.add_widget(btn_retour)
        
        scroll.add_widget(conteneur)
        layout.add_widget(lbl_titre)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def changer_ecran(self, instance):
        if not hasattr(self, 'renivintana') or not self.renivintana:
            self.result_label.text = "[color=ff5555][b]Tsy mbola voakajy :[/b][/color] Tsindrio aloha ny bokotra 'NY MOMBA NY ANDRONAO'."
            return
        app = App.get_running_app()
        ecran_vintanao = app.sm.get_screen('ecran_vintanao')
        ecran_vintanao.mettre_a_jour_donnees(self.renivintana, self.zanabintana)
        app.sm.current = 'ecran_vintanao'

    def valider_donnees(self):
        jour_text = self.spin_jour.text.strip()
        mois_text = self.spin_mois.text.strip()
        annee_text = self.spin_annee.text.strip()
        if not jour_text or not mois_text or not annee_text:
            self.result_label.text = "[color=ff5555][b]Misy diso :[/b][/color] Misafidiana na soraty azafady ny Andro, Volana ary Taona."
            return None, None, None, None
        try:
            jour = int(jour_text)
            if not (1 <= jour <= 31): raise ValueError
            mois = mois_list.index(mois_text) + 1
            annee = int(annee_text)
            date_recherchee = f"{jour:02d}/{mois:02d}/{annee}"
            date_objet = datetime.strptime(date_recherchee, "%d/%m/%Y")
            nom_complet = self.nom_input.text.strip()
            heure_recherchee = ""
            heure_text = self.spin_heure.text.strip().replace("h", "").replace("H", "")
            min_text = self.spin_min.text.strip()
            if heure_text and min_text:
                h = int(heure_text); m = int(min_text)
                if not (0 <= h <= 23 and 0 <= m <= 59): raise ValueError
                heure_recherchee = f"{h:02d}:{m:02d}"
            return date_recherchee, date_objet, nom_complet, heure_recherchee
        except Exception:
            self.result_label.text = "[color=ff5555][b]Misy diso :[/b][/color] Format daty na ora tsy mety."
            return None, None, None, None

    def calculer_et_afficher_momba(self, instance):
        date_recherchee, date_objet, nom_complet, heure_recherchee = self.valider_donnees()
        if not date_objet: return
        try:
            andro_gasy = self.obtenir_andro_gasy(date_recherchee)
            if heure_recherchee:
                h, m = map(int, heure_recherchee.split(":"))
                date_objet = date_objet.replace(hour=h, minute=m)
            luminosite_lune, repartition_lune, age_lune = calculer_details_lune(date_objet)
            ange_gardien = self.calculer_ange_gardien(date_objet.day, date_objet.month)
            add_cdv, reduite_cdv, element_cdv, inter_cdv = calculer_chemin_de_vie(date_recherchee)
            reduite_dest, element_dest, inter_dest = self.calculer_isambitana(nom_complet)
            self.renivintana = calculer_signe_solaire(date_objet.day, date_objet.month)
            self.zanabintana = calculer_signe_lunaire(date_objet)
            self.nom_complet = nom_complet
            self.date_recherchee = date_recherchee
            self.age_lune = age_lune
            self.repartition_lune = repartition_lune
            self.elem_dest = element_dest
            self.elem_cdv = element_cdv
            self.andro_gasy = andro_gasy
        except Exception as e:
            self.result_label.text = f"[color=ff5555]Erreur : {str(e)}[/color]"
            return

        affichage_heure = f" tamin'ny {heure_recherchee}" if heure_recherchee else ""
        nom_affiche = f" {nom_complet}" if nom_complet else ""
        lieu_naissance = self.lieu_input.text.strip()
        lieu_affiche = f"\n[b]TOERANA :[/b] {lieu_naissance}" if lieu_naissance else ""
        resultat = f"[color=ffd700][b]JERY VINTANA[/b][/color]\n[b]An'i{nom_affiche}[/b] teraka ny {date_recherchee}{affichage_heure}{lieu_affiche}\n------------------------------------------------\n\n"
        resultat += f"[b]ANDRO NAHATERAHANA :[/b] {andro_gasy.upper()}\n[b]HAZAVAN'NY VOLANA :[/b] {luminosite_lune} %\n[b]ENDRIKY NY VOLANA :[/b] {repartition_lune}\n[b]ANJELY MPIAMBINA :[/b] [color=00ff88]{ange_gardien.upper()}[/color]\n\n"
        resultat += "[color=00d4ff][b]LALAM-PIAINANA (Chemin de Vie)[/b][/color]\n[i]Isa fototra kajiana avy amin'ny daty nahaterahanao...[/i]\n\n"
        resultat += f"Fampifanampiana ny isa : {add_cdv}\nIsa farany : [b]{reduite_cdv}[/b] ({element_cdv})\n[i]Toetra :[/i] {inter_cdv}\n\n"
        resultat += "[color=00d4ff][b]VINTAN'NY ANARANA (CHIFFRE DU DESTIN)[/b][/color]\n[i]Isa kajiana avy amin'ny anarana...[/i]\n\n"
        resultat += f"Isa farany : [b]{reduite_dest}[/b] ({element_dest})\n[i]Toetra :[/i] {inter_dest}\n\n"
        resultat += "[i]Tsindrio ny bokotra etsy ambany raha hijery ny Renivintana sy Zanabintana.[/i]"
        self.result_label.text = resultat

    def obtenir_andro_gasy(self, date_texte):
        dictionnaire_jours = {"Monday": "Alatsinainy", "Tuesday": "Talata", "Wednesday": "Alarobia", "Thursday": "Alakamisy", "Friday": "Zoma", "Saturday": "Sabotsy", "Sunday": "Alahady"}
        date_objet = datetime.strptime(date_texte, "%d/%m/%Y")
        return dictionnaire_jours.get(date_objet.strftime("%A"), "Tsy fantatra")

    def calculer_isambitana(self, nom_complet):
        return calculer_isambitana_glob(nom_complet)

    def calculer_ange_gardien(self, jour, mois):
        donnees_anges = "01/01-05/01:Nemamiah|06/01-10/01:Yeialel|11/01-15/01:Harahel|16/01-20/01:Mitzrael|21/01-25/01:Umabel|26/01-30/01:Iah-Hel|31/01-04/02:Anauel|05/02-09/02:Mehiel|10/02-14/02:Damabiah|15/02-19/02:Manakel|20/02-24/02:Eyael|25/02-29/02:Habuhiah|01/03-05/03:Rochel|06/03-10/03:Jabamiah|11/03-15/03:Haiaiel|16/03-20/03:Mumiah|21/03-25/03:Vehuaiah|26/03-30/03:Jeliel|31/03-04/04:Sitael|05/04-09/04:Elemiah|10/04-14/04:Mahasiah|15/04-20/04:Lelahel|21/04-25/04:Achaiah|26/04-30/04:Cahetel|01/05-05/05:Haziel|06/05-10/05:Aladiah|11/05-15/05:Lauviah|16/05-20/05:Hahaiah|21/05-25/05:Iezalel|26/05-31/05:Mebahel|01/06-05/06:Hariel|06/06-10/06:Hekamiah|11/06-15/06:Lauviah|16/06-21/06:Caliel|22/06-26/06:Leuviah|27/06-01/07:Pahaliah|02/07-06/07:Nelchael|07/07-11/07:Yeiayel|12/07-16/07:Melahel|17/07-23/07:Haheuiah|24/07-27/07:Nith-Haiah|28/07-01/08:Haaiah|02/08-06/08:Yeratel|07/08-12/08:Seheiah|13/08-17/08:Reiyel|18/08-22/08:Omael|23/08-28/08:Lecabel|29/08-02/09:Vasariah|03/09-07/09:Yehuiah|08/09-12/09:Lehahiah|13/09-17/09:Chavakiah|18/09-23/09:Menadel|24/09-28/09:Aniel|29/09-03/10:Haamiah|04/10-08/10:Rehael|09/10-13/10:Ieiazel|14/10-18/10:Hahahel|19/10-23/10:Mikael|24/10-28/10:Veuliah|29/10-02/11:Yelahiah|03/11-07/11:Sealiah|08/11-12/11:Ariel|13/11-17/11:Asaliah|18/11-22/11:Mihael|23/11-27/11:Vehuel|28/11-02/12:Daniel|03/12-07/12:Hahasiah|08/12-12/12:Imamiah|13/12-16/12:Nanael|17/12-21/12:Nithael|22/12-26/12:Mebahiah|27/12-31/12:Poyel"
        for bloc in donnees_anges.split("|"):
            dates, ange_nom = bloc.split(":")
            debut, fin = dates.split("-")
            dj, dm = map(int, debut.split("/"))
            fj, fm = map(int, fin.split("/"))
            if dm == fm:
                if mois == dm and dj <= jour <= fj: return ange_nom
            else:
                if (mois == dm and jour >= dj) or (mois == fm and jour <= fj): return ange_nom
        return "Tsy hita"

class EcranVintanao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T1_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]NY VINTANAO[/b][/color]", markup=True, font_size='24sp', halign='center', size_hint_y=None, height=45)
        
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=12)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        
        card_reni = ThemedBox(bg_color=T1_CARD, orientation='vertical', size_hint_y=None, spacing=8)
        card_reni.bind(minimum_height=card_reni.setter('height'))
        hbox_reni = BoxLayout(orientation='horizontal', size_hint_y=None, height=70, spacing=10)
        img_soleil_path = os.path.join(BASE_DIR, 'soleil.png')
        if os.path.exists(img_soleil_path): hbox_reni.add_widget(Image(source=img_soleil_path, allow_stretch=True, size_hint=(0.3, 1)))
        self.icon_signe_reni = IconImage(size_px=42)
        hbox_reni.add_widget(self.icon_signe_reni)
        self.lbl_reni = DynamicLabel(text="RENIVINTANA\n[color=ff9900][b]--[/b][/color]", font_size='18sp', size_hint=(0.7, 1))
        hbox_reni.add_widget(self.lbl_reni)
        
        lbl_exp_reni = DynamicLabel(text="[i]Nifanitsy teo amin'io antokokintana io ny Tany sy ny Masoandro tamin'ny andro nahaterahanao[/i]", font_size='13sp', color=(0.8, 0.8, 0.8, 1))
        row_elem_reni = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=8)
        self.icon_elem_reni = IconImage(size_px=26)
        self.lbl_elem_reni = DynamicLabel(text="", font_size='15sp', halign='left', color=(0.9, 0.7, 0.2, 1))
        row_elem_reni.add_widget(self.icon_elem_reni); row_elem_reni.add_widget(self.lbl_elem_reni)
        self.lbl_toetra_reni = DynamicLabel(text="", font_size='14sp', color=(1, 1, 1, 1))
        card_reni.add_widget(hbox_reni); card_reni.add_widget(lbl_exp_reni); card_reni.add_widget(row_elem_reni); card_reni.add_widget(self.lbl_toetra_reni)
        conteneur.add_widget(card_reni)
        
        card_zana = ThemedBox(bg_color=T1_CARD, orientation='vertical', size_hint_y=None, spacing=8)
        card_zana.bind(minimum_height=card_zana.setter('height'))
        hbox_zana = BoxLayout(orientation='horizontal', size_hint_y=None, height=70, spacing=10)
        img_lune_path = os.path.join(BASE_DIR, 'lune.png')
        if os.path.exists(img_lune_path): hbox_zana.add_widget(Image(source=img_lune_path, allow_stretch=True, size_hint=(0.3, 1)))
        self.icon_signe_zana = IconImage(size_px=42)
        hbox_zana.add_widget(self.icon_signe_zana)
        self.lbl_zana = DynamicLabel(text="ZANABINTANA\n[color=00bfff][b]--[/b][/color]", font_size='18sp', size_hint=(0.7, 1))
        hbox_zana.add_widget(self.lbl_zana)
        
        lbl_exp_zana = DynamicLabel(text="[i]Nifanitsy teo amin'io antokokintana io ny Tany sy ny Volana tamin'ny andro nahaterahanao[/i]", font_size='13sp', color=(0.8, 0.8, 0.8, 1))
        row_elem_zana = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=8)
        self.icon_elem_zana = IconImage(size_px=26)
        self.lbl_elem_zana = DynamicLabel(text="", font_size='15sp', halign='left', color=(0.2, 0.8, 0.9, 1))
        row_elem_zana.add_widget(self.icon_elem_zana); row_elem_zana.add_widget(self.lbl_elem_zana)
        self.lbl_toetra_zana = DynamicLabel(text="", font_size='14sp', color=(1, 1, 1, 1))
        card_zana.add_widget(hbox_zana); card_zana.add_widget(lbl_exp_zana); card_zana.add_widget(row_elem_zana); card_zana.add_widget(self.lbl_toetra_zana)
        conteneur.add_widget(card_zana)
        scroll.add_widget(conteneur)
        
        box_boutons = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        btn_retour = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='15sp')
        btn_retour.bind(on_press=self.retour_ecran_principal)
        btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T2_BTN, color=(1,1,1,1), font_size='15sp')
        btn_tohiny.bind(on_press=self.aller_famakafakana)
        box_boutons.add_widget(btn_retour); box_boutons.add_widget(btn_tohiny)
        
        layout.add_widget(lbl_titre); layout.add_widget(scroll); layout.add_widget(box_boutons)
        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def mettre_a_jour_donnees(self, renivintana, zanabintana):
        self.renivintana = renivintana
        self.zanabintana = zanabintana
        self.lbl_reni.text = f"RENIVINTANA\n[color=ffa733][b]{renivintana}[/b][/color]"
        self.lbl_zana.text = f"ZANABINTANA\n[color=33d6ff][b]{zanabintana}[/b][/color]"
        self.icon_signe_reni.set_source(chemin_icone_signe(renivintana))
        self.icon_signe_zana.set_source(chemin_icone_signe(zanabintana))
        elem_reni, toetra_reni = SIGNES_DATA.get(renivintana, ("", ""))
        elem_zana, toetra_zana = SIGNES_DATA.get(zanabintana, ("", ""))
        self.icon_elem_reni.set_source(chemin_icone_element(elem_reni))
        self.icon_elem_zana.set_source(chemin_icone_element(elem_zana))
        self.lbl_elem_reni.text = f"[b]Singa : {elem_reni}[/b]"
        self.lbl_toetra_reni.text = f"[i]Toetra : {toetra_reni}[/i]"
        self.lbl_elem_zana.text = f"[b]Singa : {elem_zana}[/b]"
        self.lbl_toetra_zana.text = f"[i]Toetra : {toetra_zana}[/i]"

    def retour_ecran_principal(self, instance): App.get_running_app().sm.current = 'ecran_principal'
    def aller_famakafakana(self, instance):
        app = App.get_running_app()
        ecran_principal = app.sm.get_screen('ecran_principal')
        ecran_fm = app.sm.get_screen('ecran_famakafakana')
        ecran_fm.mettre_a_jour_donnees(ecran_principal.nom_complet, ecran_principal.date_recherchee, self.renivintana, self.zanabintana, ecran_principal.age_lune, ecran_principal.elem_dest, ecran_principal.elem_cdv, ecran_principal.andro_gasy)
        app.sm.current = 'ecran_famakafakana'

class EcranFamakafakana(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T2_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]FAMAKAFAKANA[/b][/color]", markup=True, font_size='26sp', halign='center', size_hint_y=None, height=50)
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=15)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        card = ThemedBox(bg_color=T2_CARD, orientation='vertical', size_hint_y=None, spacing=12, padding=20)
        card.bind(minimum_height=card.setter('height'))
        self.lbl_info = DynamicLabel(text="", font_size='17sp')
        self.lbl_signes = DynamicLabel(text="", font_size='19sp')
        lbl_sous_titre = DynamicLabel(text="[color=00bfff][b]TANJAKY NY VINTANA[/b][/color]", font_size='22sp', halign='center')
        self.lbl_rang = DynamicLabel(text="", font_size='18sp', halign='center')
        self.lbl_interp = DynamicLabel(text="", font_size='17sp', halign='center', color=(1, 1, 0, 1))
        self.lbl_force = DynamicLabel(text="", font_size='16sp', color=(0.9, 0.9, 0.9, 1))
        img_tanjaka_path = os.path.join(BASE_DIR, 'TANJAKA.jpg')
        if os.path.exists(img_tanjaka_path): card.add_widget(Image(source=img_tanjaka_path, allow_stretch=True, keep_ratio=True, size_hint_y=None, height=220))
        card.add_widget(self.lbl_info); card.add_widget(self.lbl_signes); card.add_widget(lbl_sous_titre); card.add_widget(self.lbl_rang); card.add_widget(self.lbl_interp); card.add_widget(self.lbl_force)
        conteneur.add_widget(card)
        scroll.add_widget(conteneur)
        box_boutons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        btn_hiverina = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='16sp')
        btn_hiverina.bind(on_press=self.retour_vintanao)
        btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T2_BTN2, color=(1,1,1,1), font_size='16sp')
        btn_tohiny.bind(on_press=self.aller_famakafakana2)
        box_boutons.add_widget(btn_hiverina); box_boutons.add_widget(btn_tohiny)
        layout.add_widget(lbl_titre); layout.add_widget(scroll); layout.add_widget(box_boutons)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def mettre_a_jour_donnees(self, nom, date, reni, zana, age_lune, elem_dest, elem_cdv, andro_gasy):
        self.nom = nom; self.date = date; self.reni = reni; self.zana = zana; self.age_lune = age_lune; self.elem_dest = elem_dest; self.elem_cdv = elem_cdv; self.andro_gasy = andro_gasy
        self.lbl_info.text = f"[b]Anarana feno :[/b] {nom}\n[b]Teraka ny :[/b] {date}"
        self.lbl_signes.text = f"[b]RENIVINTANA :[/b] {reni}\n[b]ZANABINTANA :[/b] {zana}"
        
        reni_core = ""
        zana_core = ""
        try:
            reni_core = unicodedata.normalize('NFD', reni.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
            zana_core = unicodedata.normalize('NFD', zana.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
            rang = TANJAKA_TABLE.get((reni_core, zana_core), 0)
        except: 
            rang = 0
            
        self.lbl_rang.text = f"Rang : [b]{rang}[/b] / 144"
        interp = "VINTANA MATANJAKA" if rang < 72 else "VINTANA MALEFAKA MILA ARENINA"
        self.lbl_interp.text = f"[i]{interp}[/i]"
        
        signs_forts = ["BELIER", "CANCER", "BALANCE", "CAPRICORNE"]
        is_reni_fort = reni_core in signs_forts
        is_zana_fort = zana_core in signs_forts
        
        if is_reni_fort and is_zana_fort:
            force_text = "Matanjaka daholo ny Renivintana sy Zanabintana ka sady tafiakatra ambony ny fahombiazana no vetivety ny fotoana hiakarany."
        elif is_reni_fort and not is_zana_fort:
            force_text = "Matanjaka ny Renivintana ka tafiakatra ambony ny fahombiazana saingy somary elaela ny fotoana hiakarany noho ny zanabintana malefaka."
        elif not is_reni_fort and is_zana_fort:
            force_text = "Matanjaka ny Zanabintana ka Vetivety dia miakatra ny fahombiazana saingy tsy mety tafiakatra ambony loatra araka ny eritreretina."
        else:
            force_text = "Malefaka daholo ny Renivintana sy Zanabintana ka sady tsy tafiakatra ambony ny fahombiazana no sady ela ny fotoana hiakarany ka mila arenina."
            
        self.lbl_force.text = f"[i]{force_text}[/i]"
        
    def retour_vintanao(self, instance): App.get_running_app().sm.current = 'ecran_vintanao'
    def aller_famakafakana2(self, instance):
        app = App.get_running_app()
        ecran_fm2 = app.sm.get_screen('ecran_famakafakana2')
        ecran_fm2.mettre_a_jour_donnees(self.nom, self.date, self.reni, self.zana, self.age_lune, self.elem_dest, self.elem_cdv, self.andro_gasy)
        app.sm.current = 'ecran_famakafakana2'

class EcranFamakafakana2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T2_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]FAMAKAFAKANA[/b][/color]", markup=True, font_size='26sp', halign='center', size_hint_y=None, height=50)
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=15)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        card = ThemedBox(bg_color=T2_CARD, orientation='vertical', size_hint_y=None, spacing=12, padding=20)
        card.bind(minimum_height=card.setter('height'))
        self.lbl_info = DynamicLabel(text="", font_size='17sp')
        self.lbl_signes = DynamicLabel(text="", font_size='18sp')
        lbl_sous_titre = DynamicLabel(text="[color=00bfff][b]TOETRY NY VOLANA[/b][/color]", font_size='22sp', halign='center')
        self.lbl_lune_aspect = DynamicLabel(text="", font_size='19sp', halign='center', color=(1, 1, 0, 1))
        self.lbl_lune_interp = DynamicLabel(text="", font_size='16sp', color=(0.9, 0.9, 0.9, 1))
        lbl_sous_titre_singa = DynamicLabel(text="[color=00bfff][b]FIFANDAJAN'NY SINGA[/b][/color]", font_size='22sp', halign='center')
        self.lbl_singa_interp = DynamicLabel(text="", font_size='16sp', color=(0.9, 0.9, 0.9, 1))
        img_volana_path = os.path.join(BASE_DIR, 'VOLANA.jpg')
        if os.path.exists(img_volana_path): card.add_widget(Image(source=img_volana_path, allow_stretch=True, keep_ratio=True, size_hint_y=None, height=220))
        card.add_widget(self.lbl_info); card.add_widget(self.lbl_signes); card.add_widget(lbl_sous_titre); card.add_widget(self.lbl_lune_aspect); card.add_widget(self.lbl_lune_interp)
        card.add_widget(lbl_sous_titre_singa); card.add_widget(self.lbl_singa_interp)
        conteneur.add_widget(card)
        scroll.add_widget(conteneur)
        box_boutons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        btn_hiverina = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='16sp')
        btn_hiverina.bind(on_press=self.retour_famakafakana1)
        btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T2_BTN2, color=(1,1,1,1), font_size='16sp')
        btn_tohiny.bind(on_press=self.aller_famakafakana3)
        box_boutons.add_widget(btn_hiverina); box_boutons.add_widget(btn_tohiny)
        layout.add_widget(lbl_titre); layout.add_widget(scroll); layout.add_widget(box_boutons)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def mettre_a_jour_donnees(self, nom, date, reni, zana, age_lune, elem_dest, elem_cdv, andro_gasy):
        self.nom = nom; self.date = date; self.reni = reni; self.zana = zana; self.age_lune = age_lune; self.elem_dest = elem_dest; self.elem_cdv = elem_cdv; self.andro_gasy = andro_gasy
        self.lbl_info.text = f"[b]Anarana feno :[/b] {nom}\n[b]Teraka ny :[/b] {date}"
        self.lbl_signes.text = f"[b]RENIVINTANA :[/b] {reni}\n[b]ZANABINTANA :[/b] {zana}"
        aspect, interp = get_moon_interp(age_lune)
        self.lbl_lune_aspect.text = f"[b]{aspect}[/b]"
        self.lbl_lune_interp.text = f"[i]{interp}[/i]"
        elem_reni, _ = SIGNES_DATA.get(reni, ("", ""))
        elem_zana, _ = SIGNES_DATA.get(zana, ("", ""))
        reni_elem = elem_reni.split()[0] if elem_reni else ""
        zana_elem = elem_zana.split()[0] if elem_zana else ""
        
        if reni_elem == zana_elem: 
            interp_singa = "Tsy mari-toerana ny vintana fa miaka-midina sady mitongina eo amin'ny singa ka misy toetra na fihetsika tsy mety voafehy ka mila itandremana. Be fikasana fa vitsy no tanteraka ary somary sahirana rehefa manainga projet na mitady vahaolana. Mila mitandrina fa misy fitanilana eo amin'ny Singa ka misy toetra sy fihetsika tsy mety voafehy, tsy maritoerana ny vintana fa miakamidina ihany koa."
        else:
            is_harm = (reni_elem == "Afo" and zana_elem == "Rano") or (reni_elem == "Rano" and zana_elem == "Afo") or (reni_elem == "Tany" and zana_elem == "Rivotra") or (reni_elem == "Rivotra" and zana_elem == "Tany")
            if is_harm: 
                interp_singa = "Maritoerana ny vintana ka tsy atahorana hiakamidina loatra na fitiavana na asa. Mahay miaraka ny Singan'ny Vintanao ka tsy atahorana hiaka-midina loatra ny fahombiazana."
            else: 
                interp_singa = "Tsy mari-toerana ny vintana ka miaka-midina, tsapa izany eo amin'ny asa sy ny fitiavana. Fisaka ny Vintana ka miteraka olana matetika sy misesy eo amin'ny fiainana toy ny ara-pahasalamana na ara-bola. Tsy mahay miaraka ny Singa ao aminao ka tsy mari-toerana ny vintana fa miaka-midina, na fitiavana na fitadiavam-bola."
                
        self.lbl_singa_interp.text = f"[i]{interp_singa}[/i]"
        
    def retour_famakafakana1(self, instance): App.get_running_app().sm.current = 'ecran_famakafakana'
    def aller_famakafakana3(self, instance):
        app = App.get_running_app()
        ecran_fm3 = app.sm.get_screen('ecran_famakafakana3')
        ecran_fm3.mettre_a_jour_donnees(self.nom, self.date, self.reni, self.zana, self.age_lune, self.elem_dest, self.elem_cdv, self.andro_gasy)
        app.sm.current = 'ecran_famakafakana3'

class EcranFamakafakana3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T2_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]FAMAKAFAKANA[/b][/color]", markup=True, font_size='26sp', halign='center', size_hint_y=None, height=50)
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=15)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        card = ThemedBox(bg_color=T2_CARD, orientation='vertical', size_hint_y=None, spacing=12, padding=20)
        card.bind(minimum_height=card.setter('height'))
        self.lbl_info = DynamicLabel(text="", font_size='17sp')
        self.lbl_signes = DynamicLabel(text="", font_size='18sp')
        lbl_sous_titre = DynamicLabel(text="[color=00bfff][b]FIFAMENOAN'NY SINGA[/b][/color]", font_size='22sp', halign='center')
        self.lbl_singa_summary = DynamicLabel(text="", font_size='16sp', color=(0.9, 0.9, 0.9, 1))
        self.box_diagram = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.box_diagram.bind(minimum_height=self.box_diagram.setter('height'))
        card.add_widget(self.lbl_info); card.add_widget(self.lbl_signes); card.add_widget(lbl_sous_titre); card.add_widget(self.lbl_singa_summary); card.add_widget(self.box_diagram)
        conteneur.add_widget(card)
        self.box_lesoka = ThemedBox(bg_color=(0.35, 0.08, 0.08, 1), orientation='vertical', size_hint_y=None, padding=15, spacing=10)
        self.lbl_lesoka = DynamicLabel(text="", font_size='16sp', color=(1, 0.85, 0.3, 1))
        self.lbl_lesoka.bind(texture_size=lambda *x: setattr(self.box_lesoka, 'height', self.lbl_lesoka.texture_size[1] + 40 if self.lbl_lesoka.text else 0))
        self.box_lesoka.add_widget(self.lbl_lesoka)
        self.box_lesoka.height = 0; self.box_lesoka.opacity = 0
        conteneur.add_widget(self.box_lesoka)
        scroll.add_widget(conteneur)
        box_boutons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        btn_hiverina = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='16sp')
        btn_hiverina.bind(on_press=self.retour_famakafakana2)
        btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T2_BTN2, color=(1,1,1,1), font_size='16sp')
        btn_tohiny.bind(on_press=self.aller_famintinana)
        box_boutons.add_widget(btn_hiverina); box_boutons.add_widget(btn_tohiny)
        layout.add_widget(lbl_titre); layout.add_widget(scroll); layout.add_widget(box_boutons)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def mettre_a_jour_donnees(self, nom, date, reni, zana, age_lune, elem_dest, elem_cdv, andro_gasy):
        self.nom = nom; self.date = date; self.reni = reni; self.zana = zana; self.age_lune = age_lune; self.elem_dest = elem_dest; self.elem_cdv = elem_cdv; self.andro_gasy = andro_gasy
        self.lbl_info.text = f"[b]Anarana feno :[/b] {nom}\n[b]Teraka ny :[/b] {date}"
        self.lbl_signes.text = f"[b]RENIVINTANA :[/b] {reni}\n[b]ZANABINTANA :[/b] {zana}"
        elem_reni, _ = SIGNES_DATA.get(reni, ("", ""))
        elem_zana, _ = SIGNES_DATA.get(zana, ("", ""))
        elem_jour = JOUR_ELEMENTS.get(andro_gasy, "Tsy fantatra")
        elem_reni_w = elem_reni.split()[0].upper() if elem_reni else "TSY FANTATRA"
        elem_zana_w = elem_zana.split()[0].upper() if elem_zana else "TSY FANTATRA"
        elem_dest_w = elem_dest.split()[0].upper() if elem_dest else "TSY FANTATRA"
        elem_cdv_w = elem_cdv.split()[0].upper() if elem_cdv else "TSY FANTATRA"
        elem_jour_w = elem_jour.split()[0].upper() if elem_jour else "TSY FANTATRA"
        percents = {'AFO': 0, 'RANO': 0, 'RIVOTRA': 0, 'TANY': 0}
        if elem_reni_w in percents: percents[elem_reni_w] += 50
        if elem_zana_w in percents: percents[elem_zana_w] += 25
        if elem_dest_w in percents: percents[elem_dest_w] += 10
        if elem_cdv_w in percents: percents[elem_cdv_w] += 10
        if elem_jour_w in percents: percents[elem_jour_w] += 5
        summary = f"RENIVINTANA: {elem_reni_w}\nZANABINTANA: {elem_zana_w}\nANARANA: {elem_dest_w}\nLALAM-PIAINANA: {elem_cdv_w}\nTERAKA ANDRO ({andro_gasy.upper()}): {elem_jour_w}"
        self.lbl_singa_summary.text = summary
        conclusions = []; interpretations_lesoka = []
        effets = {'AFO': {'manque': "Tsy misy Afo: Tsy manana fanahy mavitrika sy fahamarinan-toerana, mora morandraina sy kamo.", 'exces': "Be loatra ny Afo: Moratezitra, tsy mahazaka tsy faneken-kevitra, mavesatra ny fahatsapana tena."}, 'RANO': {'manque': "Tsy misy Rano: Tsy mahay mifandray am-po, malaina amin'ny fihetseham-po, sarotra mandefa fitiavana.", 'exces': "Be loatra ny Rano: Mora sendra fiankinan-doha, be onjam-po, lasa tafintohina mora."}, 'RIVOTRA': {'manque': "Tsy misy Rivotra: Tsy tia fifandraisana, somary mitokana, mifikitra amin'ny fomba taloha.", 'exces': "Be loatra ny Rivotra: Tsy milamina, be fisainana tsy tanteraka, miresaka tsy misy farany."}, 'TANY': {'manque': "Tsy misy Tany: Tsy miorina, tia mandehandeha tsy misy tanjona, tsy mahay mitahiry.", 'exces': "Be loatra ny Tany: Mafy loha, manelingelina, lasa materialiste loatra sy milamina fongana."}}
        for elem, perc in percents.items():
            if perc >= 80: conclusions.append(f"[b]LESOKA: BE LOATRA NY {elem}[/b]"); interpretations_lesoka.append(effets[elem]['exces'])
            elif perc == 0: conclusions.append(f"[b]LESOKA: TSY MISY {elem}[/b]"); interpretations_lesoka.append(effets[elem]['manque'])
        if conclusions:
            lesoka_lines = [f"{c}\n[i]{i}[/i]" for c, i in zip(conclusions, interpretations_lesoka)]
            self.lbl_lesoka.text = f"[color=ff3333][size=20sp][b]/!\\[/b][/size]  " + "\n\n".join(lesoka_lines)
            self.box_lesoka.opacity = 1
        else: self.lbl_lesoka.text = ""; self.box_lesoka.opacity = 0
        self.box_diagram.clear_widgets()
        colors = {'AFO': (1, 0.35, 0.25, 1), 'RANO': (0.25, 0.55, 1, 1), 'RIVOTRA': (0.85, 0.85, 0.85, 1), 'TANY': (0.5, 0.3, 0.15, 1)}
        for elem in ['AFO', 'RANO', 'RIVOTRA', 'TANY']:
            p = percents[elem]
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=38, spacing=5)
            icon_e = IconImage(size_px=26)
            icon_e.set_source(chemin_icone_element(elem))
            lbl_e = Label(text=f"[b]{elem}[/b]", markup=True, size_hint_x=0.28, color=(1,1,1,1), font_size='15sp')
            bar_bg = BoxLayout(size_hint_x=0.47, height=26, size_hint_y=None, padding=2)
            bar_bg.add_widget(BarWidget(colors[elem], size_hint_x=(p/100.0 if p > 0 else 0.001)))
            bar_bg.add_widget(Widget(size_hint_x=max(0.001, 1.0 - p/100.0)))
            lbl_p = Label(text=f"{p}%", size_hint_x=0.2, color=(1,1,1,1), font_size='15sp')
            row.add_widget(icon_e); row.add_widget(lbl_e); row.add_widget(bar_bg); row.add_widget(lbl_p)
            self.box_diagram.add_widget(row)
    def retour_famakafakana2(self, instance): App.get_running_app().sm.current = 'ecran_famakafakana2'
    def aller_famintinana(self, instance):
        app = App.get_running_app()
        ecran_fam = app.sm.get_screen('ecran_famintinana')
        ecran_fam.mettre_a_jour_donnees(self.nom, self.date, self.reni, self.zana, self.age_lune, self.elem_dest, self.elem_cdv, self.andro_gasy)
        app.sm.current = 'ecran_famintinana'

class EcranFamintinana(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T2_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]FAMINTINANA[/b][/color]", markup=True, font_size='26sp', halign='center', size_hint_y=None, height=50)
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=15)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        
        card = ThemedBox(bg_color=T2_CARD, orientation='vertical', size_hint_y=None, spacing=12, padding=20)
        card.bind(minimum_height=card.setter('height'))
        self.lbl_summary = DynamicLabel(text="", font_size='16sp', color=(1, 1, 1, 1))
        card.add_widget(self.lbl_summary)
        
        conteneur.add_widget(card)
        scroll.add_widget(conteneur)
        
        btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T2_BTN2, color=(1,1,1,1), font_size='16sp', size_hint_y=None, height=50)
        btn_tohiny.bind(on_press=self.aller_manambina)
        
        layout.add_widget(lbl_titre); layout.add_widget(scroll); layout.add_widget(btn_tohiny)
        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def aller_manambina(self, instance):
        app = App.get_running_app()
        ecran_m = app.sm.get_screen('ecran_manambina')
        ecran_m.mettre_a_jour_donnees(self.renivintana, self.zanabintana)
        app.sm.current = 'ecran_manambina'

    def mettre_a_jour_donnees(self, nom, date, reni, zana, age_lune, elem_dest, elem_cdv, andro_gasy):
        self.renivintana = reni
        self.zanabintana = zana
        
        elem_reni, toetra_reni = SIGNES_DATA.get(reni, ("", ""))
        elem_zana, toetra_zana = SIGNES_DATA.get(zana, ("", ""))
        reni_elem_w = elem_reni.split()[0].upper() if elem_reni else ""
        zana_elem_w = elem_zana.split()[0].upper() if elem_zana else ""
        
        relation_text = ""
        if reni_elem_w and zana_elem_w:
            if reni_elem_w == zana_elem_w:
                relation_text = "Mila mitandrina fa misy fitanilana eo amin'ny Singa (mitovy singa ny Renivintana sy Zanabintana) ka misy toetra sy fihetsika tsy mety voafehy, tsy maritoerana ny vintana fa miakamidina ihany koa."
            else:
                is_harm = (reni_elem_w == "AFO" and zana_elem_w == "RANO") or (reni_elem_w == "RANO" and zana_elem_w == "AFO") or (reni_elem_w == "TANY" and zana_elem_w == "RIVOTRA") or (reni_elem_w == "RIVOTRA" and zana_elem_w == "TANY")
                if is_harm:
                    relation_text = "Mahay miaraka ny Singan'ny Vintanao ka tsy atahorana hiaka-midina loatra ny fahombiazana."
                else:
                    relation_text = "Tsy mahay miaraka ny Singa ao aminao ka tsy mari-toerana ny vintana fa miaka-midina, na fitiavana na fitadiavam-bola."
        
        _, reduite_cdv, _, inter_cdv = calculer_chemin_de_vie(date)
        reduite_dest, _, inter_dest = calculer_isambitana_glob(nom)
        
        reni_core = unicodedata.normalize('NFD', reni.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
        zana_core = unicodedata.normalize('NFD', zana.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
        rang = TANJAKA_TABLE.get((reni_core, zana_core), 0)
        interp_tanjaka = "VINTANA MATANJAKA" if rang < 72 else "VINTANA MALEFAKA MILA ARENINA"
        
        aspect, interp_lune = get_moon_interp(age_lune)
        lesoka_text = calculate_lesoka(reni, zana, elem_dest, elem_cdv, andro_gasy)
        
        summary_text = f"[color=00d4ff][b]1. NY TOETRAO MANOKANA[/b][/color]\n\n"
        summary_text += f"[b]Renivintana ({reni}):[/b] {toetra_reni}\n\n"
        summary_text += f"[b]Zanabintana ({zana}):[/b] {toetra_zana}\n\n"
        summary_text += f"[b]Lalam-piainana (Isa {reduite_cdv}):[/b] {inter_cdv}\n\n"
        summary_text += f"[b]Vintan'ny anarana (Isa {reduite_dest}):[/b] {inter_dest}\n\n"
        summary_text += "------------------------------------------------\n"
        summary_text += f"[color=00d4ff][b]2. NY TANJAKY NY VINTANA[/b][/color]\n\n"
        summary_text += f"Ity vintanao ity dia [b]{interp_tanjaka}[/b]. Raha matanjaka izy dia mahomby ny asa ataonao ary maivana ny fifanarahana. Raha mila arenina kosa dia mila fitandremana sy asa fanahy noho ny fahaketrahany, saingy azo ovaina izany amin'ny alalan'ny fivavahana sy fomba famerenana hasina na rituel.\n\n"
        summary_text += "------------------------------------------------\n"
        summary_text += f"[color=00d4ff][b]3. NY VOLANA SY NY SINGA[/b][/color]\n\n"
        summary_text += f"[b]Toetry ny Volana:[/b] {aspect}. {interp_lune}\n\n"
        summary_text += f"[b]Fifanarahan'ny Singa (Renivintana sy Zanabintana):[/b] {relation_text}\n\n"
        summary_text += f"[b]Fifanjarian'ny Singa ankapobeny:[/b]\n{lesoka_text}\n\n"
        summary_text += "------------------------------------------------\n"
        summary_text += f"[color=00d4ff][b]4. TOROHEVITRA FARANY[/b][/color]\n\n"
        summary_text += "Mba hahitanao ny fivoaran'ny vintanao amin'ny alalan'ny fomba mahomby dia afaka mandre sy manatona an'i [b]Harilanto Fidinirina[/b] ianao.\n"
        summary_text += "Facebook: [b]Fotoana Mety[/b]\n"
        summary_text += "WhatsApp: [b]034 90 906 25[/b]\n"
        summary_text += "[i]Tadidio fa ny vintana dia azo arenina fa tsy azo ovaina. Misy torolalana fomba sy fady arahinao sy ny rituel mifanaraka amin'ny olanao.[/i]"
        
        self.lbl_summary.text = summary_text

class EcranManambina(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T2_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]LISITRY NY MANAMBINA[/b][/color]", markup=True, font_size='24sp', halign='center', size_hint_y=None, height=45)
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=15)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        self.card_reni = ThemedBox(bg_color=T2_CARD, orientation='vertical', size_hint_y=None, spacing=8)
        self.card_reni.bind(minimum_height=self.card_reni.setter('height'))
        self.lbl_reni_title = Label(text="", markup=True, font_size='18sp', halign='center', size_hint_y=None, height=35)
        img_reni_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=350, padding=5)
        self.img_reni = Image(source="", allow_stretch=True, keep_ratio=True, size_hint=(1, 1))
        img_reni_box.add_widget(self.img_reni)
        self.card_reni.add_widget(self.lbl_reni_title); self.card_reni.add_widget(img_reni_box)
        conteneur.add_widget(self.card_reni)
        self.card_zana = ThemedBox(bg_color=T2_CARD, orientation='vertical', size_hint_y=None, spacing=8)
        self.card_zana.bind(minimum_height=self.card_zana.setter('height'))
        self.lbl_zana_title = Label(text="", markup=True, font_size='18sp', halign='center', size_hint_y=None, height=35)
        img_zana_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=350, padding=5)
        self.img_zana = Image(source="", allow_stretch=True, keep_ratio=True, size_hint=(1, 1))
        img_zana_box.add_widget(self.img_zana)
        self.card_zana.add_widget(self.lbl_zana_title); self.card_zana.add_widget(img_zana_box)
        conteneur.add_widget(self.card_zana)
        scroll.add_widget(conteneur)
        btn_hiverina = RoundedButton(text="[b]Hiverina (Retour)[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='16sp', size_hint_y=None, height=45)
        btn_hiverina.bind(on_press=self.retour_famakafakana3)
        
        lbl_sig = DynamicLabel(text=SIGNATURE_TEXT, font_size='11sp', halign='center', size_hint_y=None, height=25)
        
        layout.add_widget(lbl_titre); layout.add_widget(scroll); layout.add_widget(btn_hiverina); layout.add_widget(lbl_sig)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def mettre_a_jour_donnees(self, renivintana, zanabintana):
        try:
            reni_core = unicodedata.normalize('NFD', renivintana.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
            zana_core = unicodedata.normalize('NFD', zanabintana.split('(')[1].replace(')', '').strip().upper()).encode('ascii', 'ignore').decode('ascii')
        except: 
            reni_core = "TSY FANTATRA"
            zana_core = "TSY FANTATRA"
        self.lbl_reni_title.text = f"[b]RENIVINTANA : {renivintana}[/b]"
        self.lbl_zana_title.text = f"[b]ZANABINTANA : {zanabintana}[/b]"
        img_reni_path = os.path.join(BASE_DIR, f"{reni_core}-RENIVINTANA.jpg")
        self.img_reni.source = img_reni_path if os.path.exists(img_reni_path) else ""
        self.img_reni.opacity = 1 if os.path.exists(img_reni_path) else 0
        self.img_reni.reload()
        img_zana_path = os.path.join(BASE_DIR, f"{zana_core}-ZANABINTANA.jpg")
        self.img_zana.source = img_zana_path if os.path.exists(img_zana_path) else ""
        self.img_zana.opacity = 1 if os.path.exists(img_zana_path) else 0
        self.img_zana.reload()
    def retour_famakafakana3(self, instance): App.get_running_app().sm.current = 'ecran_famakafakana3'

class EcranFifamabinana(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T3_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl_titre = Label(text="[color=ffd700][b]FIFANAMBINANA[/b][/color]", markup=True, font_size='26sp', size_hint_y=None, height=45, halign='center')
        lbl_sous_titre = Label(text="LAHY sy VAVY", markup=True, font_size='18sp', size_hint_y=None, height=30, halign='center', color=(0.8, 0.8, 0.8, 1))
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=12)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        box_inputs = ThemedBox(bg_color=T3_CARD, orientation='vertical', size_hint_y=None, spacing=10)
        box_inputs.bind(minimum_height=box_inputs.setter('height'))
        
        box_lahy = BoxLayout(orientation='vertical', spacing=4, size_hint_y=None)
        box_lahy.bind(minimum_height=box_lahy.setter('height'))
        box_lahy.add_widget(Label(text="[b]LAHY[/b]", markup=True, size_hint_y=None, height=22, font_size='16sp', color=(0.3, 0.7, 1, 1)))
        lbl_indication_l = Label(text="Ampidiro ny Daty sy Ora nahaterahana", size_hint_y=None, height=20, font_size='12sp', color=(0.8, 0.8, 0.8, 1), halign='center')
        box_lahy.add_widget(lbl_indication_l)
        row_date_lahy = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.spin_jour_lahy = ModernDateField(values=[str(i) for i in range(1, 32)], size_hint=(0.3, 1))
        self.spin_mois_lahy = ModernDateField(values=mois_list, size_hint=(0.4, 1))
        self.spin_annee_lahy = ModernDateField(values=annees_list, size_hint=(0.3, 1))
        row_date_lahy.add_widget(self.spin_jour_lahy); row_date_lahy.add_widget(self.spin_mois_lahy); row_date_lahy.add_widget(self.spin_annee_lahy)
        box_lahy.add_widget(row_date_lahy)
        row_heure_lahy = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.spin_heure_lahy = ModernDateField(values=heures_list, size_hint=(0.5, 1))
        self.spin_min_lahy = ModernDateField(values=minutes_list, size_hint=(0.5, 1))
        row_heure_lahy.add_widget(self.spin_heure_lahy); row_heure_lahy.add_widget(self.spin_min_lahy)
        box_lahy.add_widget(row_heure_lahy)
        box_inputs.add_widget(box_lahy)
        
        box_inputs.add_widget(Label(text="", size_hint_y=None, height=5))
        
        box_vavy = BoxLayout(orientation='vertical', spacing=4, size_hint_y=None)
        box_vavy.bind(minimum_height=box_vavy.setter('height'))
        box_vavy.add_widget(Label(text="[b]VAVY[/b]", markup=True, size_hint_y=None, height=22, font_size='16sp', color=(1, 0.45, 0.55, 1)))
        lbl_indication_v = Label(text="Ampidiro ny Daty sy Ora nahaterahana", size_hint_y=None, height=20, font_size='12sp', color=(0.8, 0.8, 0.8, 1), halign='center')
        box_vavy.add_widget(lbl_indication_v)
        row_date_vavy = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.spin_jour_vavy = ModernDateField(values=[str(i) for i in range(1, 32)], size_hint=(0.3, 1))
        self.spin_mois_vavy = ModernDateField(values=mois_list, size_hint=(0.4, 1))
        self.spin_annee_vavy = ModernDateField(values=annees_list, size_hint=(0.3, 1))
        row_date_vavy.add_widget(self.spin_jour_vavy); row_date_vavy.add_widget(self.spin_mois_vavy); row_date_vavy.add_widget(self.spin_annee_vavy)
        box_vavy.add_widget(row_date_vavy)
        row_heure_vavy = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.spin_heure_vavy = ModernDateField(values=heures_list, size_hint=(0.5, 1))
        self.spin_min_vavy = ModernDateField(values=minutes_list, size_hint=(0.5, 1))
        row_heure_vavy.add_widget(self.spin_heure_vavy); row_heure_vavy.add_widget(self.spin_min_vavy)
        box_vavy.add_widget(row_heure_vavy)
        box_inputs.add_widget(box_vavy)
        
        self.btn_valiny = RoundedButton(text="[b]VALINY[/b]", markup=True, bg_color=(0.2, 0.75, 0.3, 1), color=(1,1,1,1), size_hint_y=None, height=48, font_size='16sp')
        self.btn_valiny.bind(on_press=self.calculer_compatibilite)
        self.lbl_result = DynamicLabel(text="", font_size='13sp', padding=(10, 10))
        self.btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T3_BTN2, color=(1,1,1,1), size_hint_y=None, height=44, font_size='15sp')
        self.btn_tohiny.bind(on_press=self.aller_resultat_fifam)
        self.btn_tohiny.disabled = True
        btn_retour = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='15sp', size_hint_y=None, height=44)
        btn_retour.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_accueil'))
        box_bas = BoxLayout(orientation='horizontal', size_hint_y=None, height=44, spacing=10)
        box_bas.add_widget(btn_retour)
        box_bas.add_widget(self.btn_tohiny)
        conteneur.add_widget(box_inputs)
        conteneur.add_widget(self.btn_valiny)
        conteneur.add_widget(self.lbl_result)
        conteneur.add_widget(box_bas)
        scroll.add_widget(conteneur)
        layout.add_widget(lbl_titre)
        layout.add_widget(lbl_sous_titre)
        layout.add_widget(scroll)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def get_date_parts(self, spin_jour, spin_mois, spin_annee):
        try:
            j = int(spin_jour.text.strip())
            m = mois_list.index(spin_mois.text.strip()) + 1
            a = int(spin_annee.text.strip())
            if not (1 <= j <= 31 and 1 <= m <= 12 and 1900 <= a <= 2050): return None
            return j, m, a
        except: return None
    def get_time_parts(self, spin_h, spin_m):
        try:
            h = int(spin_h.text.strip().replace("h", ""))
            m = int(spin_m.text.strip())
            if not (0 <= h <= 23 and 0 <= m <= 59): return None
            return h, m
        except: return None
    def calculer_compatibilite(self, instance):
        dl = self.get_date_parts(self.spin_jour_lahy, self.spin_mois_lahy, self.spin_annee_lahy)
        dv = self.get_date_parts(self.spin_jour_vavy, self.spin_mois_vavy, self.spin_annee_vavy)
        if not dl or not dv:
            self.lbl_result.text = "[color=ff5555][b]Misy diso :[/b][/color] Ampidiro azafady ny daty rehetra sahady."
            return
        tl = self.get_time_parts(self.spin_heure_lahy, self.spin_min_lahy)
        tv = self.get_time_parts(self.spin_heure_vavy, self.spin_min_vavy)
        dt_l = datetime(dl[2], dl[1], dl[0], tl[0] if tl else 0, tl[1] if tl else 0)
        dt_v = datetime(dv[2], dv[1], dv[0], tv[0] if tv else 0, tv[1] if tv else 0)
        date_l_str = f"{dl[0]:02d}/{dl[1]:02d}/{dl[2]}"
        date_v_str = f"{dv[0]:02d}/{dv[1]:02d}/{dv[2]}"
        reni_l = calculer_signe_solaire(dl[0], dl[1])
        elem_reni_l = SIGNES_DATA.get(reni_l, ("", ""))[0]
        zana_l = calculer_signe_lunaire(dt_l)
        elem_zana_l = SIGNES_DATA.get(zana_l, ("", ""))[0]
        _, cdv_l, elem_cdv_l, _ = calculer_chemin_de_vie(date_l_str)
        _, _, age_lune_l = calculer_details_lune(dt_l)
        tanjaka_l = get_tanjaka_status(reni_l, zana_l, age_lune_l)
        reni_v = calculer_signe_solaire(dv[0], dv[1])
        elem_reni_v = SIGNES_DATA.get(reni_v, ("", ""))[0]
        zana_v = calculer_signe_lunaire(dt_v)
        elem_zana_v = SIGNES_DATA.get(zana_v, ("", ""))[0]
        _, cdv_v, elem_cdv_v, _ = calculer_chemin_de_vie(date_v_str)
        _, _, age_lune_v = calculer_details_lune(dt_v)
        tanjaka_v = get_tanjaka_status(reni_v, zana_v, age_lune_v)
        self.reni_l = reni_l; self.zana_l = zana_l
        self.reni_v = reni_v; self.zana_v = zana_v
        self.tanjaka_l = tanjaka_l; self.tanjaka_v = tanjaka_v
        res = f"[b]LAHY :[/b]\nRenivintana: {reni_l} ({elem_reni_l})\nZanabintana: {zana_l} ({elem_zana_l})\nLalam-piainana: {cdv_l} ({elem_cdv_l})\n\n"
        res += f"[b]VAVY :[/b]\nRenivintana: {reni_v} ({elem_reni_v})\nZanabintana: {zana_v} ({elem_zana_v})\nLalam-piainana: {cdv_v} ({elem_cdv_v})\n"
        self.lbl_result.text = res
        self.btn_tohiny.disabled = False
    def aller_resultat_fifam(self, instance):
        if self.btn_tohiny.disabled: return
        app = App.get_running_app()
        ecran_res = app.sm.get_screen('ecran_resultat_fifam')
        ecran_res.mettre_a_jour_donnees(self.reni_l, self.zana_l, self.reni_v, self.zana_v, self.tanjaka_l, self.tanjaka_v)
        app.sm.current = 'ecran_resultat_fifam'

class EcranResultatFifam(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T3_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl_titre = Label(text="[color=ffd700][b]FIFANAMBINANA[/b][/color]", markup=True, font_size='28sp', size_hint_y=None, height=50, halign='center')
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='10dp', scroll_wheel_distance=100)
        conteneur = GridLayout(cols=1, size_hint_y=None, spacing=20)
        conteneur.bind(minimum_height=conteneur.setter('height'))
        card1 = ThemedBox(bg_color=T3_CARD, orientation='vertical', size_hint_y=None, spacing=10)
        card1.bind(minimum_height=card1.setter('height'))
        card1.add_widget(Label(text="Misy fifanotoana ve?", markup=True, font_size='20sp', halign='center', size_hint_y=None, height=40, color=(0.8, 0.8, 0.8, 1)))
        self.lbl_reponse1 = Label(text="", markup=True, font_size='30sp', halign='center', size_hint_y=None, height=50)
        self.lbl_detail1 = DynamicLabel(text="", font_size='14sp', halign='center')
        card1.add_widget(self.lbl_reponse1)
        card1.add_widget(self.lbl_detail1)
        conteneur.add_widget(card1)
        card2 = ThemedBox(bg_color=T3_CARD, orientation='vertical', size_hint_y=None, spacing=10)
        card2.bind(minimum_height=card2.setter('height'))
        card2.add_widget(Label(text="mahao ahoana ny tanjaky ny vintana?", markup=True, font_size='18sp', halign='center', size_hint_y=None, height=40, color=(0.8, 0.8, 0.8, 1)))
        self.lbl_reponse2 = DynamicLabel(text="", font_size='16sp')
        card2.add_widget(self.lbl_reponse2)
        conteneur.add_widget(card2)
        scroll.add_widget(conteneur)
        box_bas = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        btn_hiverina = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=(0.3, 0.3, 0.35, 1), color=(1,1,1,1), font_size='18sp')
        btn_hiverina.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_fifamabinana'))
        self.btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T3_BTN, color=(1,1,1,1), font_size='18sp')
        self.btn_tohiny.bind(on_press=self.aller_singa_fifam)
        box_bas.add_widget(btn_hiverina)
        box_bas.add_widget(self.btn_tohiny)
        layout.add_widget(lbl_titre)
        layout.add_widget(scroll)
        layout.add_widget(box_bas)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def mettre_a_jour_donnees(self, reni_l, zana_l, reni_v, zana_v, tanjaka_l, tanjaka_v):
        self.reni_l = reni_l; self.zana_l = zana_l
        self.reni_v = reni_v; self.zana_v = zana_v
        self.tanjaka_l = tanjaka_l; self.tanjaka_v = tanjaka_v
        is_opp = check_crossed_opposition(reni_l, zana_l, reni_v, zana_v)
        self.is_opp = is_opp
        if is_opp:
            self.lbl_reponse1.text = "[color=ff0000][b]ENY[/b][/color]"
            detail_text = "Misy fifanotoana ny vintana ka mipoitra ao anaty tokantrano ireto:\n\n- Ady lava tsy fantam-pototra,\n- Aretina miverim-berina\n- Vola miditra fa tsy mahatsangana\n- Mitsangana fa miharava."
            self.lbl_detail1.text = detail_text
        else:
            self.lbl_reponse1.text = "[color=00ff00][b]TSIA[/b][/color]"
            self.lbl_detail1.text = "Tsy misy ny fifanotoana ka tsy voarara ny fiarahan'ny lahy sy vavy, afaka mifanambina fa mbola mila jerena ny Tanjaky ny Vintana sy ny fahaizan'ny Singa miaraka."
        tanjaka_interp = get_tanjaka_interp(tanjaka_l, tanjaka_v)
        self.lbl_reponse2.text = f"Lahy: [b]{tanjaka_l}[/b]\nVavy: [b]{tanjaka_v}[/b]\n\n[i]{tanjaka_interp}[/i]" if tanjaka_interp else ""
    def aller_singa_fifam(self, instance):
        app = App.get_running_app()
        ecran_singa = app.sm.get_screen('ecran_singa_fifam')
        ecran_singa.mettre_a_jour_donnees(self.reni_l, self.zana_l, self.reni_v, self.zana_v, self.is_opp, self.tanjaka_l, self.tanjaka_v)
        app.sm.current = 'ecran_singa_fifam'

class EcranSingaFifam(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T3_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl_titre = Label(text="[color=ffd700][b]FIFANAMBINANA[/b][/color]", markup=True, font_size='28sp', size_hint_y=None, height=50, halign='center')
        lbl_question = Label(text="Mahay miaraka ve ny singa?", markup=True, font_size='22sp', size_hint_y=None, height=40, halign='center', color=(0.8, 0.8, 0.8, 1))
        
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='10dp', scroll_wheel_distance=100)
        card = ThemedBox(bg_color=T3_CARD, orientation='vertical', size_hint_y=None, spacing=10)
        card.bind(minimum_height=card.setter('height'))
        row_singa_icons = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=15)
        self.icon_singa_l = IconImage(size_px=36)
        lbl_singa_l_tag = Label(text="[b]Lahy[/b]", markup=True, size_hint_x=None, width=50, color=(1,1,1,1), font_size='14sp')
        self.icon_singa_v = IconImage(size_px=36)
        lbl_singa_v_tag = Label(text="[b]Vavy[/b]", markup=True, size_hint_x=None, width=50, color=(1,1,1,1), font_size='14sp')
        row_singa_icons.add_widget(lbl_singa_l_tag); row_singa_icons.add_widget(self.icon_singa_l)
        row_singa_icons.add_widget(lbl_singa_v_tag); row_singa_icons.add_widget(self.icon_singa_v)
        card.add_widget(row_singa_icons)
        self.lbl_detail = DynamicLabel(text="", font_size='16sp')
        card.add_widget(self.lbl_detail)
        
        img_fifam_path = os.path.join(BASE_DIR, 'fifanambinana.jpg')
        img_fifam = Image(source=img_fifam_path, allow_stretch=True, keep_ratio=True, size_hint_y=None, height=250)
        if not os.path.exists(img_fifam_path):
            img_fifam.opacity = 0
        card.add_widget(img_fifam)
        
        scroll.add_widget(card)
        
        self.btn_tohiny = RoundedButton(text="[b]Tohiny[/b]", markup=True, bg_color=T3_BTN, color=(1,1,1,1), size_hint_y=None, height=50, font_size='18sp')
        self.btn_tohiny.bind(on_press=self.aller_final_fifam)
        
        layout.add_widget(lbl_titre)
        layout.add_widget(lbl_question)
        layout.add_widget(scroll)
        layout.add_widget(self.btn_tohiny)
        self.add_widget(layout)
        
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def mettre_a_jour_donnees(self, reni_l, zana_l, reni_v, zana_v, is_opp, tanjaka_l, tanjaka_v):
        self.is_opp = is_opp
        self.tanjaka_l = tanjaka_l
        self.tanjaka_v = tanjaka_v
        elem_reni_l = SIGNES_DATA.get(reni_l, ("", ""))[0]
        elem_zana_l = SIGNES_DATA.get(zana_l, ("", ""))[0]
        singa_l = combine_elements(elem_reni_l, elem_zana_l)
        elem_reni_v = SIGNES_DATA.get(reni_v, ("", ""))[0]
        elem_zana_v = SIGNES_DATA.get(zana_v, ("", ""))[0]
        singa_v = combine_elements(elem_reni_v, elem_zana_v)
        fifam_name = deduce_fifamabinana(singa_l, singa_v)
        status, interp = interpret_fifamabinana(fifam_name)
        self.status_singa = status
        detail_text = f"[b]Singa Lahy:[/b] {singa_l}\n[b]Singa Vavy:[/b] {singa_v}\n\n[b]TILY SIKIDY:[/b] {fifam_name}\n[b]ENDRINY:[/b] [color=ffd700]{status}[/color]\n\n[i]{interp}[/i]"
        self.lbl_detail.text = detail_text
        self.icon_singa_l.set_source(chemin_icone_element(singa_l))
        self.icon_singa_v.set_source(chemin_icone_element(singa_v))
        p1 = 20 if self.is_opp else 80
        if tanjaka_l == "MATANJAKA" and tanjaka_v == "MATANJAKA": p2 = 75
        elif tanjaka_l == "MALEFAKA" and tanjaka_v == "MALEFAKA": p2 = 25
        else: p2 = 60
        if status == "TSARA": p3 = 80
        elif status == "ANTONONY": p3 = 75
        else: p3 = 15
        self.pourcentage_final = (p1 + p2 + p3) / 3.0
        
    def aller_final_fifam(self, instance):
        app = App.get_running_app()
        ecran_final = app.sm.get_screen('ecran_final_fifam')
        ecran_final.afficher_resultat(self.pourcentage_final, self.is_opp)
        app.sm.current = 'ecran_final_fifam'

class EcranFinalFifam(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*T3_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)
        lbl_titre = Label(text="[color=ffd700][b]VALIN'NY FIFANAMBINANA[/b][/color]", markup=True, font_size='28sp', halign='center', size_hint_y=0.1)
        box_pct = ThemedBox(bg_color=T3_CARD, orientation='vertical', padding=20, spacing=10, size_hint_y=0.3)
        lbl_pct_subtitle = Label(text="Tahan'ny Fifanaraka", markup=True, font_size='16sp', color=(0.7, 0.7, 0.8, 1), size_hint_y=0.2)
        self.lbl_pourcentage = Label(text="", markup=True, font_size='64sp', halign='center', valign='middle', size_hint_y=0.6, bold=True)
        lbl_pct_info = Label(text="Kajiana avy amin'ny Tanjaka sy Singa", markup=True, font_size='12sp', color=(0.5, 0.5, 0.5, 1), size_hint_y=0.2)
        box_pct.add_widget(lbl_pct_subtitle)
        box_pct.add_widget(self.lbl_pourcentage)
        box_pct.add_widget(lbl_pct_info)
        box_comment = ThemedBox(bg_color=T3_CARD, orientation='vertical', padding=20, size_hint_y=0.3)
        scroll_comment = ScrollView(do_scroll_x=False, scroll_type=['content', 'bars'], bar_width='8dp', scroll_wheel_distance=100)
        self.lbl_comment = DynamicLabel(text="", font_size='18sp', halign='center', color=(0.95, 0.95, 0.95, 1), padding=(10, 10))
        scroll_comment.add_widget(self.lbl_comment)
        box_comment.add_widget(scroll_comment)
        btn_retour = RoundedButton(text="[b]Hiverina[/b]", markup=True, bg_color=T1_BTN, color=(1,1,1,1), font_size='16sp', size_hint_y=0.1)
        btn_retour.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_accueil'))
        btn_refaire = RoundedButton(text="[b]Hanao Fifamabinana hafa[/b]", markup=True, bg_color=T3_BTN, color=(1,1,1,1), font_size='16sp', size_hint_y=0.1)
        btn_refaire.bind(on_press=lambda *x: setattr(App.get_running_app().sm, 'current', 'ecran_fifamabinana'))
        box_btns = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.1)
        box_btns.add_widget(btn_retour)
        box_btns.add_widget(btn_refaire)
        
        lbl_sig = DynamicLabel(text=SIGNATURE_TEXT, font_size='12sp', halign='center', size_hint_y=0.1)
        
        layout.add_widget(lbl_titre)
        layout.add_widget(box_pct)
        layout.add_widget(box_comment)
        layout.add_widget(box_btns)
        layout.add_widget(lbl_sig)
        self.add_widget(layout)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def afficher_resultat(self, pourcentage, is_opp):
        pct_str = f"{pourcentage:.2f}"
        if pourcentage >= 70:
            color = "00ff00"
            comment = "Mirary hafaliana sy fitahiana ianareo roa ! Mifanambina tsara na vola na zanaka na fahasalamana. Tsara vintana sy mifanaraka tsara ny fiainana hanangana tokantrano."
        elif pourcentage >= 50:
            color = "ffd700"
            comment = "Mifanambina ihany ianareo. Mety hiroso ho fianakaviana nefa mila fifehezana sy fifampitantanana tsara."
        else:
            color = "ff4500"
            if is_opp:
                comment = "Voarara ny fiarahana noho ny fifanotoana sady tsy mahay miaraka koa ny singa ka betsaka ny olana ho atrehina."
            else:
                comment = "latsaka kely ny antonony ny fifanambinana noho ny toetra tsy mahay miaraka fa tsy voarara ny fiarahana."
        self.lbl_pourcentage.text = f"[color={color}][b]{pct_str} %[/b][/color]"
        self.lbl_comment.text = comment

class JeryVintanaApp(App):
    def build(self):
        self.icon = os.path.join(BASE_DIR, 'icon.png')
        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(EcranAccueil(name='ecran_accueil'))
        self.sm.add_widget(EcranPrincipal(name='ecran_principal'))
        self.sm.add_widget(EcranVintanao(name='ecran_vintanao'))
        self.sm.add_widget(EcranFamakafakana(name='ecran_famakafakana'))
        self.sm.add_widget(EcranFamakafakana2(name='ecran_famakafakana2'))
        self.sm.add_widget(EcranFamakafakana3(name='ecran_famakafakana3'))
        self.sm.add_widget(EcranFamintinana(name='ecran_famintinana'))
        self.sm.add_widget(EcranManambina(name='ecran_manambina'))
        self.sm.add_widget(EcranFifamabinana(name='ecran_fifamabinana'))
        self.sm.add_widget(EcranResultatFifam(name='ecran_resultat_fifam'))
        self.sm.add_widget(EcranSingaFifam(name='ecran_singa_fifam'))
        self.sm.add_widget(EcranFinalFifam(name='ecran_final_fifam'))
        return self.sm

if __name__ == '__main__':
    JeryVintanaApp().run()