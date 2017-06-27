import util
from pythia8 import Pythia
from data.data_getter import DataGetter

DEFAULT_ENERGY_LEVEL = 10500
DEFAULT_NUMBER_OF_COLLISIONS = 5000


class Hist(DataGetter):
    def __init__(self,
                 energy_level: int = DEFAULT_ENERGY_LEVEL,
                 number_of_collisions: int = DEFAULT_NUMBER_OF_COLLISIONS):
        super().__init__({
            "ratio_hist": ("mesons", "baryons"),
            "mesons_eta_hist": ("mesons_eta",),
            "baryons_eta_hist": ("baryons_eta",)
        })
        self.energy_level = energy_level
        self.number_of_collisions = number_of_collisions

    def get_data(self):
        ratio_hist_file = self.files["ratio_hist"]  # type: util.DataFile
        mesons_eta_hist_file = self.files["mesons_eta_hist"]  # type: util.DataFile
        baryons_eta_hist_file = self.files["baryons_eta_hist"]  # type: util.DataFile

        p = util.new_pythia_instance()  # type: Pythia
        util.set_energy(p, self.energy_level)
        p.init()

        for i in range(self.number_of_collisions):
            self._update(i / self.number_of_collisions)
            p.next()

            counts, mesons_eta, baryons_eta \
                = util.count_mesons_and_baryons(list(p.event), eta=True)

            ratio_hist_file.write(counts)
            mesons_eta_hist_file.write((",\n".join(map(str, mesons_eta)), ))
            baryons_eta_hist_file.write((",\n".join(map(str, baryons_eta)), ))
