import pythia8


def new_instance(collision_energy: int=None) -> pythia8.Pythia:
    p = pythia8.Pythia("", False)
    p.readFile("cfg.txt")

    if collision_energy is not None:
        if not isinstance(collision_energy, int):
            raise ValueError("`collision_energy` must be an int!")
        p.readString("Beams:eCM = {}".format(collision_energy))

    return p
