Particle Simulations
====================

***Edit: the paper is now available [here in the repository](https://github.com/NatKarmios/ParticleSimulations/blob/master/paper.pdf).***

#### *Used as part of the CREST project by Nat Karmios, Nima Sahba, Carlos Barredo, and Lucas George.*

Generates specifically-purposed data using the 
[Pythia 8 monte-carlo generator](http://home.thep.lu.se/~torbjorn/pythia81html/Welcome.html).

This consists of an API server (built with Flask) which serves JSON objects via HTTP,
and the webpage with which to use the API server. If you host the API server with HTTPS, 
then you can use the interface [here](https://natkarmios.github.io/ParticleSimulations), 
otherwise you must host the interface page with regular HTTP.

The API server's [Docker container](https://hub.docker.com/r/natk/particles/) 
can have an open port to be either directly accessed by clients 
***(not reccommended)*** or used in conjunction with a webserver (e.g. Apache or nginx).

The Docker container requires a volume at `/root/cfg`, which must contain:
- `pythia_cfg.txt`, which specifies parameters to be fed into the Pythia generator
- `cfg.py`, which requires a variable, `PASSWD`, which serves as the password for the API authentication.

*Side note: a `pythia_cfg.txt` is provided in `python/cfg/pythia_cfg.txt`,
and an example of `cfg.py` is at `python/cfg/cfg.py`*

Example `docker run` command:
<br />
`$ docker run -d -p 127.0.0.1:5000:5000 -v $PWD/cfg:/root/cfg --name particles natk/particles`
<br />
There is also a provided `run.sh` which should work, provided the necessary config files are present..

