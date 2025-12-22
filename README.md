# Whistle for VF

A loud and safe whistle which can be customized with a name.

![Whistle with name ANNA](pictures/01-ANNA.jpg)


## Main features:

- Nice loud sound.
- Lanyard Ring – attaches the whistle safely and securely to a lanyard.
- Makes sound from relatively low air flow to extremely high air flow. I tested some other whisles, that stop making noise at high air flow. See my test of several 3D printed whistles.
- Incision for teeth – prevents the whistle from blowing away.
- Customizable – a name can be put on side. Currently there is no published support for the customization, but you can download a whistle with ANNA on side.

Can be easily used by children from 2 years.


## How to use

There are several options:

### 1. Get the file and print it

Download [whistle.step](whistle.step).

### 2. Add a name to the model

1. Setup

```
git clone https://github.com/jmalenko/whistle.git
chmod a+x *.py *.sh
source .venv/bin/activate
```

2. Create the model with *ANNA* by running with

```
./whistle.py ANNA
```

The output is stored in `whistle.step`.


### 3. Optional: advanced example

To create a whistle model with name *A N N A* (with spaces between letters) that is saved to file `my_whistle.step `, run:

```
./whistle.py -o my_whistle.step "A N N A"
```


### 4. Generate several models with names

1. Setup as in previous step 2.

2. Put the names to `names.txt`. For example:
```
ANNA
Betty
E V A
```

3. Generate models
```
./generate.sh
```

The generated models are stored in `models` directory with the following names:
```
whistle-ANNA.step
whistle-Betty.step
whistle-E_V_A.step
```

## Print instructions

- Use at least 4 perimeters &mdash; even three layers sometimes leave micro holes between the strings of filament.
- No supports needed.
- Rotate such that the potential name is on top. (This should be the default orientation.)
- Add color change (for name) at layer just above 10 mm.

Besides that, there are no special conditions. I print this whistle with PLA, 0.2 layer height.
