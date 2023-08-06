# stoy
Application for shutting down kernels and terminals in Jupyter Lab after they were idle for a specified period of time.
Jupyter Lab itself is terminated when no kernels and terminals were open for some time.

# Installation
Install with `pip`
```commandline
pip install stoy
```

# Usage
Define the three timeouts, in seconds, as demonstrated in the example below:
```commandline
stoy --kernel-idle=3600 --terminal-idel=3600 --server-idle=1800
```


