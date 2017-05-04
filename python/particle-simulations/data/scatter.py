from data.data_getter import DataGetter

import util
import pythia8

DEFAULT_ENERGY_STEP = 100
DEFAULT_EVENTS_PER_ENERGY_STEP = 10000


class Scatter(DataGetter):

    def __init__(self, energy_step: int = DEFAULT_ENERGY_STEP,
                 events_per_energy_step: int = DEFAULT_EVENTS_PER_ENERGY_STEP, type_="scatter"):
        super().__init__(type_)
        self.energy_step = energy_step
        self.events_per_energy_step = events_per_energy_step

    def get_data(self):
        p = util.new_pythia_instance()

        for energy in range(7000, 14000, self.energy_step):
            self.progress = (energy - 7000) / 7000

            self._update(progress=(energy - 7000) / 7000, message="step {}/{}".format(energy, 14000))

            p.readString("Beams:eCM = {}".format(energy))
            p.init()

            for i in range(self.events_per_energy_step):
                p.next()

                meson_count = 0
                baryon_count = 0

                lst = list(p.event)

                mesons = list(filter(lambda prt: prt.id() in util.meson_codes, lst))
                for _ in mesons:  # type: pythia8.Particle
                    meson_count += 1

                baryons = list(filter(lambda prt: prt.id() in util.baryon_codes, lst))
                for _ in baryons:  # type: pythia8.Particle
                    baryon_count += 1

                util.write_line_to_file(self.filename, (energy, meson_count, baryon_count))

