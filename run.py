
# <editor-fold desc="Setup">


from pythia_lib import pythia8

# <editor-fold desc="Helper Functions">


def pretty_print(obj, indent: int=2) -> None:
    from pprint import pprint
    pprint(obj, indent=indent)


def _print(*args, **kwargs):
    if len(args) == 0:
        args = ""
    print(*args, **kwargs)
    return args[0]


def create_file() -> str:
    from datetime import datetime
    filename = "particle-data_" + datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S" + ".csv")
    open(filename, "w+").close()
    return filename


def write_line_to_file(filename, data) -> None:
    with open(filename, "a+") as file:
        file.write(",".join(map(str, data)) + "\n")


# </editor-fold>

# http://www.thefullwiki.org/List_of_mesons
meson_codes = {
    # 211: "pi+",
    # 213: "rho+",
    # 311: "K0",
    # 313: "K*0",
    # 321: "K+",
    # 323: "K*+",
    # 411: "D+",
    # 413: "D*+",
    # 421: "D0",
    # 423: "D*0",
    # 431: "D_s+",
    # 433: "D*_s+",
    511: "B0",
    513: "B*0",
    521: "B+",
    523: "B*+",
    531: "B_s0",
    533: "B*_s0",
    541: "B_c+",
    543: "B*_c+",
    # 111: "pi0",
    # 113: "rho0",
    # 221: "eta",
    # 223: "omega",
    # 331: "eta'",
    # 333: "phi",
    # 441: "eta_c",
    # 443: "J/psi",
    551: "eta_b",
    553: "Upsilon",
    # 130: "K_L0",
    # 310: "K_S0",

    # 10211: "a_0+",  # ?
    # 10213: "b_1+",  # ?
    # 10311: "K*_00",
    # 10313: "K_10",
    # 10321: "K*_0+",
    # 10323: "K_1+",
    # 10411: "D*_0+",
    # 10413: "D_1+",
    # 10421: "D*_00",
    # 10423: "D_10",
    # 10431: "D*_0s+",
    # 10433: "D_1s+",
    # 10111: "a_00",  # ?
    # 10113: "b_10",  # ?
    # 10221: "f_00",  # ?
    # 10223: "h_10",  # ?
    # 10331: "f'_00",  # ?
    # 10333: "h'_10",  # ?
    # 10441: "chi_0c0",  # ?
    # 10443: "h_1c0",  # ?
    # 215: "a_2+",  # ?
    # 20213: "a_1+",  # ?
    # 315: "K*_20",
    # 20313: "K*+10",
    # 325: "K*_2+",
    # 20323: "K*_1+",
    # 415: "D*_2+",
    # 20413: "D*_1+",
    # 425: "D*_20",
    # 20423: "D*_10",
    # 435: "D*_2s+",
    # 20433: "D*_1s+",
    # 115: "a_20",  # ?
    # 20113: "a_10",  # ?
    # 225: "f_20",  # ?
    # 20223: "f_10",  # ?
    # 335: "f'_20",  # ?
    # 20333: "f'_10",  # ?
    # 445: "chi_2c0",  # ?
    # 20443: "chi_1c0",  # ?
    # 100443: "psi'",
    100553: "Upsilon'"
}

# http://www.thefullwiki.org/List_of_baryons
baryon_codes = {
 # 1114:  "Delta-",
 # 2112:  "n0",
 # 2114:  "Delta0",
 # 2212:  "p+",
 # 2214:  "Delta+",
 # 2224:  "Delta++",
 # 3112:  "Sigma-",
 # 3114:  "Sigma*-",
 # 3122:  "Lambda0",
 # 3212:  "Sigma0",
 # 3214:  "Sigma*0",
 # 3222:  "Sigma+",
 # 3224:  "Sigma*+",
 # 3312:  "Xi-",
 # 3314:  "Xi*-",
 # 3322:  "Xi0",
 # 3324:  "Xi*0",
 # 3334:  "Omega-"
 # 4112:  "Sigma_c0",
 # 4114:  "Sigma*_c0",
 # 4122:  "Lambda_c+",
 # 4212:  "Sigma_c+",
 # 4214:  "Sigma*_c+",
 # 4222:  "Sigma_c++",
 # 4224:  "Sigma*_c++",
 # 4132:  "Xi_c0",
 # 4312:  "Xi'_c0",
 # 4314:  "Xi*_c0",
 # 4232:  "Xi_c+",
 # 4322:  "Xi'_c+",
 # 4324:  "Xi*_c+",
 # 4332:  "Omega_c0",
 # 4334:  "Omega*_c0",
 5112:  "Sigma_b-",
 5114:  "Sigma*_b-",
 5122:  "Lambda_b0",
 5212:  "Sigma_b0",
 5214:  "Sigma*_b0",
 5222:  "Sigma_b+",
 5224:  "Sigma*_b+",
}


# </editor-fold>

ENERGY_STEP = 100
EVENTS_PER_ENERGY_STEP = 10000

p = pythia8.Pythia("", False)
p.readFile("cfg.txt")

particle_data_filename = create_file()
particle_data = []

for energy in range(7000, 14000, ENERGY_STEP):

    p.readString("Beams:eCM = {}".format(energy))
    print("\n\n\n== Beam energy set to {} ==\n".format(p.parm("Beams:eCM")))

    p.init()

    meson_count = 0
    baryon_count = 0
    total_particles = 0

    for i in range(EVENTS_PER_ENERGY_STEP):
        p.next()

        print("Event {}/{}...".format(i+1, EVENTS_PER_ENERGY_STEP))

        lst = list(p.event)
        total_particles += len(lst)

        mesons = list(filter(lambda prt: prt.id() in meson_codes, lst))
        for meson in mesons:  # type: pythia8.Particle
            meson_count += 1

        baryons = list(filter(lambda prt: prt.id() in baryon_codes, lst))
        for baryon in baryons:  # type: pythia8.Particle
            baryon_count += 1

    print("\nFinal Totals")
    print("   mesons: {}".format(meson_count))
    print("  baryons: {}".format(baryon_count))
    print()
    print("  ignored: {}".format(total_particles-(meson_count+baryon_count)))

    particle_data.append((energy, meson_count, baryon_count))
    write_line_to_file(particle_data_filename, (energy, meson_count, baryon_count))

pretty_print(particle_data)
