from typing import Iterable, Union, List, Tuple

import pythia8
from util import meson_codes, baryon_codes


def new_instance(collision_energy: int=None) -> pythia8.Pythia:
    p = pythia8.Pythia("", False)
    p.readFile("./cfg/pythia_cfg.txt")

    if collision_energy is not None:
        if not isinstance(collision_energy, int):
            raise ValueError("`collision_energy` must be an int!")
        p.readString("Beams:eCM = {}".format(collision_energy))

    return p


def set_energy(pythia: pythia8.Pythia, energy: int) -> None:
    pythia.readString("Beams:eCM = {}".format(energy))


def count_mesons_and_baryons(event: Iterable[pythia8.Particle], eta=False) \
        -> Union[Tuple[int, int], Tuple[Tuple[int, int], List[float], List[float]]]:
    mesons = list(filter(lambda prt: prt.id() in meson_codes, event))
    baryons = list(filter(lambda prt: prt.id() in baryon_codes, event))

    meson_count, baryon_count = len(mesons), len(baryons)

    if eta:
        mesons_eta = [meson.eta() for meson in mesons]
        baryons_eta = [baryon.eta() for baryon in baryons]

        return (meson_count, baryon_count), mesons_eta, baryons_eta

    return meson_count, baryon_count
