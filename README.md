# ml-demo
HEP machine-learning demos.


## `diboson`

This is stolen from [`richstu/diboson_ml`](https://github.com/richstu/diboson_ml),
with tweaks to work with newer version of libraries.


### Usage on NixOS

Enter a nix shell with the following command:

```shell
nix develop --impure
```

**Note the `--impure` flag!**

Go into `diboson` folder, then:

```shell
./train_dnn.py
# or
./train_dnn.py --cpu
```

### Usage on non-NixOS

Enter a nix shell with the following command:

```shell
nix develop --impure
```

**Note the `--impure` flag!**

Go into `diboson` folder, then:

```shell
nixGL ./train_dnn.py
# or
./train_dnn.py --cpu
```

**Note the `nixGL` wrapper, which makes the script recognize the GPU!**
