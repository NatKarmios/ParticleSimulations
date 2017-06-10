import util
from pythia8 import Pythia
from data.data_getter import DataGetter

DEFAULT_ENERGY_LEVEL = 10500
DEFAULT_NUMBER_OF_COLLISIONS = 5000


class Hist(DataGetter):
    def __init__(self, type_="hist",
                 energy_level: int = DEFAULT_ENERGY_LEVEL,
                 number_of_collisions: int = DEFAULT_NUMBER_OF_COLLISIONS):
        super().__init__(type_, ("mesons", "baryons", "eta"))
        self.energy_level = energy_level
        self.number_of_collisions = number_of_collisions

    def get_data(self):
        p = util.new_pythia_instance()  # type: Pythia
        util.set_energy(p, self.energy_level)
        p.init()

        for i in range(self.number_of_collisions):
            self._update(i / self.number_of_collisions)
            p.next()

            meson_count, baryon_count = util.count_mesons_and_baryons(list(p.event))
            eta = util.get_pseudorapidity(p.event)
            self.write((meson_count, baryon_count, eta))
