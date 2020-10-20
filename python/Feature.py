import csv

class Feature:

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.label_from_string = {s:i for i,s in enumerate(values)}
        self.images_paths = []
        self.labels = []

    def add_image(self, path, label):
        self.images_paths += [path]
        self.labels += [label]

    def to_csv(self, file_name):
        with open(file_name, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Path', 'Label'])
            writer.writerows(zip(self.images_paths, self.labels))

class Features:
    rims = Feature("Rims", ["BBS", "Nautilus", "Hoggar", "Tacoma", "Other"])
    front_bumper = Feature("Front Bumper", ["Phase 1", "Phase 2", "Other"])
    interior = Feature('Interior', ["Abricot", "Amarante", "Ouragan", "Nil Bleu", "Alezan", "Salzbourg Astrakan", "Cobalt", "Ouragan Salzbourg", "Creme", "Chess"])
    exterior = Feature("Exterior", ["Cendré", "Thallium", "Hadès", "Cosmos", "Riviera", "Hypérion", "Bysance", "Récife", "Ecarlate", "Lucifer", "Lugano", "Polo", "Solstice", "Louxor", "Granit", "Other"])
    dict = {'rims':rims, 'front_bumper':front_bumper, 'interior':interior, 'exterior':exterior}
    list = list(dict.keys())

    @classmethod
    def from_string(cls, s):
        return cls.dict[s]
