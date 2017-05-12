import util
from data.data_getter import DataGetter

DEFAULT_ENERGY_STEP = 100
DEFAULT_EVENTS_PER_ENERGY_STEP = 10000


class Scatter(DataGetter):
    def __init__(self, type_: str="scatter",
                 energy_step: int = DEFAULT_ENERGY_STEP,
                 events_per_energy_step: int = DEFAULT_EVENTS_PER_ENERGY_STEP):
        super().__init__(type_, ("energy", "mesons", "baryons"))
        self.energy_step = energy_step
        self.events_per_energy_step = events_per_energy_step

    def get_data(self):
        p = util.new_pythia_instance()

        for energy in range(7000, 14000, self.energy_step):
            self.progress = (energy - 7000) / 7000

            self._update(progress=(energy - 7000) / 7000)

            if self.cancelled:
                return

            p.readString("Beams:eCM = {}".format(energy))
            p.init()

            for i in range(self.events_per_energy_step):
                p.next()
                meson_count, baryon_count = util.count_mesons_and_baryons(list(p.event))
                self.write((energy, meson_count, baryon_count))
                if self.cancelled:
                    return
