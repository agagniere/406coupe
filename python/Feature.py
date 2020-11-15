START = 1997
END   = 2004

class Feature:

    def __init__(self, name, values, years = None):
        self.name   = name
        self.values = values
        self.years  = years

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return "Feature('{}', {} values)".format(self.name, len(self.values))

class Features:
    rims = Feature(
        "Rims",
        ["BBS",         "Nautilus",  "Hoggar",    "Tacoma", "Custom"],
        [(START, 2001), (2002, END), (2001, END), (2003,END)])

    front_bumper = Feature(
        "Front Bumper",
        ["Phase 1",     "Phase 2", "Custom"],
        [(START, 2003), (2003, END)])

    interior = Feature(
        "Interior",
        ["Abricot",     "Amarante",    "Ouragan",    "Nil Bleu",    "Alezan",    "Salzbourg Astrakan", "Cobalt",    "Ouragan Salzbourg", "Creme",      "Chess"],
        [(START, 2000), (START, 2003), (START, END), (START, 2000), (2000, END), (2000, 2003),         (2003, END), (2003, END),         (2000, 2000), (2002, 2002)])

    exterior = Feature(
        "Exterior",
        ["Cendré",  "Thallium", "Hadès",   "Cosmos",    "Riviera",   "Hypérion","Bysance",   "Récife",  "Ecarlate", "Lucifer",   "Lugano",   "Polo",      "Solstice", "Louxor",    "Granit"],
        [(2004,END),(START,END),(2000,END),(START,2002),(START,2001),(2001,END),(START,2002),(2002,END),(START,END),(START,2003),(START,200),(START,2003),(2001,2004),(START,2001),(2002,END)])

    engine = Feature(
        "Engine",
        ["XU10J4R 135", "EW10J4 137", "HDi",       "2.2 160",   "V6 194",      "V6 210"],
        [(START, 1999), (1999, 2002), (2001, END), (2002, END), (START, 1999), (1999, END)])

    options = Feature(
        "Options",
        ["Wing", "Sunroof", "Speed regulator", "Hitch", "Oil thermometer", "Electric seats", "Heated seats"])

    dict = {'rims':rims, 'front_bumper':front_bumper, 'interior':interior, 'exterior':exterior, 'engine':engine, 'options':options}
    list = list(dict.values())

    @classmethod
    def from_string(cls, s):
        return cls.dict[s]
