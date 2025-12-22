# Whistle for VF

A loud and safe whistle which can be customized with a name.

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

- Download [whistle.step](https://raw.githubusercontent.com/jmalenko/whistle/refs/heads/main/whistle.step)

### 2. Add a name to the model

1. Setup

```
git clone https://github.com/jmalenko/whistle.git
chmod a+x *.py *.sh
source .venv/bin/activate
```

2. Create the model with NAME by running with

```
./whistle.py NAME
```

The output is stored in `whistle.step`.


Alternatively, you can define the output file with `-o` parameter:

```
./whistle.py -o my_whistle.step NAME
```


### 3. Generate several models with names

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

- use at least 4 perimeters. 
- no supports, print on side (so the potential name is at the top).

Besides that, there are no special conditions. I print this whistle with PLA, 0.2 layer height.
