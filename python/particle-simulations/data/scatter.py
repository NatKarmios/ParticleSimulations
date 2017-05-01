import util
import pythia8

DEFAULT_ENERGY_STEP = 100
DEFAULT_EVENTS_PER_ENERGY_STEP = 10000


def get_scatter_data(
        energy_step: int=DEFAULT_ENERGY_STEP,
        events_per_energy_step: int=DEFAULT_EVENTS_PER_ENERGY_STEP,
        pid: int=None
) -> str:
    p = util.new_pythia_instance()

    filename = util.create_file()

    for energy in range(7000, 14000, energy_step):
        if pid is not None:
            print("{}: step {}/{}".format(pid, energy, 14000))

        p.readString("Beams:eCM = {}".format(energy))
        p.init()

        for i in range(events_per_energy_step):
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

            util.write_line_to_file(filename, (energy, meson_count, baryon_count))

    return util.upload_file_to_gists(filename)
