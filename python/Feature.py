import csv

class Feature:

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.label_from_string = {s:i for i,s in enumerate(values)}
        self.images_paths = []
        self.labels = []
        self.not_visible = []

    def add_image(self, path, label):
        self.images_paths += [path]
        self.labels += [label]

    def add_not_visible(self, path):
        self.not_visible += [path]

    def to_csv(self, file_name):
        with open(file_name, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Path', 'Label'])
            writer.writerows(zip(self.images_paths, self.labels))

    def from_csv(self, file_name):
        with open(file_name, mode='r') as f:
            self.from_opened_csv(f)

    def from_opened_csv(self, csv_file):
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        for row in reader:
            self.add_image(*row)

    def boolean_training_balanced(self):
        return (self.images_paths + self.not_visible[:len(self)], [True] * len(self) + [False] * min(len(self), len(self.not_visible)))
    def boolean_training(self):
        return (self.images_paths + self.not_visible, [True] * len(self) + [False] * len(self.not_visible))

    def __len__(self):
        return len(self.images_paths)

    def __str__(self):
        return "Feature('{}', {} values, {} images)".format(self.name, len(self.values), len(self))


class Features:
    rims = Feature("Rims", ["BBS", "Nautilus", "Hoggar", "Tacoma", "Other"])
    front_bumper = Feature("Front Bumper", ["Phase 1", "Phase 2", "Other"])
    interior = Feature('Interior', ["Abricot", "Amarante", "Ouragan", "Nil Bleu", "Alezan", "Salzbourg Astrakan", "Cobalt", "Ouragan Salzbourg", "Creme", "Chess"])
    exterior = Feature("Exterior", ["Cendré", "Thallium", "Hadès", "Cosmos", "Riviera", "Hypérion", "Bysance", "Récife", "Ecarlate", "Lucifer", "Lugano", "Polo", "Solstice", "Louxor", "Granit", "Other"])
    engine = Feature("Engine", ["XU10J4R 135", "EW10J4 137", "HDi", "2.2 160", "V6 194", "V6 210"])
    dict = {'rims':rims, 'front_bumper':front_bumper, 'interior':interior, 'exterior':exterior, 'engine':engine}
    list = list(dict.keys())

    @classmethod
    def from_string(cls, s):
        return cls.dict[s]
