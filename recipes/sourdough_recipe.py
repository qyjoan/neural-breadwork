from collections import defaultdict


class FlourMix(object):
    def __init__(self, **kwargs):
        assert(sum(kwargs.values()) == 1)
        self.flour_mix = kwargs


class Starter(object):
    def __init__(self, hydration, **kwargs):
        '''
        :param hydration: float, hydration percentage
        :param flour_mix: FlourMix
        '''
        self.hydration = hydration
        self.flour_mix = FlourMix(**kwargs)


class SourdoughRecipe(object):

    def __init__(self):
        # dough formula variables
        self.dough_water = None
        self.dough_flour = defaultdict(int)
        self.salt = None
        self.levain = None
        # baker's percentage variables
        self.total_flour = defaultdict(float)
        self.total_water = None
        self.hydration = None

    def create(
            self,
            final_dough_weight: float,
            final_flour_mix: FlourMix,
            starter: Starter,
            hydration: float,
            salt_percentage: float,
            starter_percentage: float):

        self.hydration = hydration * 100
        # calculate total flour weight
        r = hydration + salt_percentage + 1
        flour_weight = final_dough_weight / r

        final_flour = final_flour_mix.flour_mix
        for flour_type, perc in final_flour.items():
            self.total_flour[flour_type] = flour_weight * final_flour[flour_type]
        self.total_water = flour_weight * hydration
        self.salt = flour_weight * salt_percentage
        self.levain = flour_weight * starter_percentage

        # calculate flour mix for mixing
        starter_water = self.levain / (1.0+starter.hydration)
        self.dough_water = self.total_water - starter_water
        starter_flour_mix = starter.flour_mix.flour_mix
        for flour_type in self.total_flour:
            w = starter_flour_mix.get(flour_type, 0) * (self.levain - starter_water)
            if w > self.total_flour[flour_type]:
                raise Exception("Starter contains too much %s flour" % flour_type)
            self.dough_flour[flour_type] = self.total_flour[flour_type] - w

    def print_bakers_perc(self):
        print("========== Baker's Percentage ==========")
        total_flour_weight = round(sum(self.total_flour.values()))
        print("Flour: %sg" % total_flour_weight)
        for flour in self.total_flour:
            w = round(self.total_flour[flour])
            print(" - %s: %sg (%s%%)" % (flour, w, round(w*100./total_flour_weight)))
        print("Water: %sg (%s%%)" % (round(self.total_water),self.hydration))
        print("Salt: %sg (%s%%)" % (round(self.salt), round(self.salt * 100. / total_flour_weight)))

    def print_dough_formula(self):
        print("========== Dough Formula ==========")
        print("Levain %sg" % round(self.levain))
        for flour in self.dough_flour:
            print("%s: %sg" % (flour, round(self.dough_flour[flour])))
        print("Water %sg" % round(self.dough_water))
        print("Salt %sg" % round(self.salt))

    def print_recipe(self):
        self.print_bakers_perc()
        self.print_dough_formula()


if __name__=="__main__":
    my_starter = Starter(1, whole_wheat=0.5, white_flour=0.5)
    flour = FlourMix(whole_wheat=0.10, rye=0.05, white_flour=0.85)
    sd = SourdoughRecipe()
    sd.create(
        final_dough_weight=600,
        final_flour_mix=flour,
        starter=my_starter,
        hydration=.85,
        salt_percentage=.02,
        starter_percentage=.2)
    sd.print_recipe()