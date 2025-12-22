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

- Use "Whistle for VF.step".

### 2. Add a name to the model

Setup

```
git clone https://github.com/jmalenko/whistle.git
source .venv/bin/activate
chmod a+x whistle.py
```

Create modele with name

```
./whistle.py ANNA
```


### 3. Generate several models with names

TODO

## Print instructions:

- use at least 4 perimeters. 
- no supports, print on side (so the potential name is at the top).

Besides that, there are no special conditions. I print this whistle with PLA, 0.2 layer height.



# Development tips

Run in terminal:
```
.venv/bin/python whistle.py
```
or
```
source .venv/bin/activate
chmod a+x whistle.py
./whistle.py
```

# Development tips

## Show part as the code is updated

Configure IDE to save file immediately. Add to `settings.json`:
```
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 500
```
