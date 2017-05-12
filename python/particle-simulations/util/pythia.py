from typing import Tuple, Iterable

import pythia8
from util import meson_codes, baryon_codes


def new_instance(collision_energy: int=None) -> pythia8.Pythia:
    p = pythia8.Pythia("", False)
    p.readFile("cfg.txt")

    if collision_energy is not None:
        if not isinstance(collision_energy, int):
            raise ValueError("`collision_energy` must be an int!")
        p.readString("Beams:eCM = {}".format(collision_energy))

    return p


def set_energy(pythia: pythia8.Pythia, energy: int) -> None:
    pythia.readString("Beams:eCM = {}".format(energy))


def count_mesons_and_baryons(event: Iterable) -> Tuple[int, int]:
    return (len(list(filter(lambda prt: prt.id() in meson_codes, event))),
            len((list(filter(lambda prt: prt.id() in baryon_codes, event)))))
