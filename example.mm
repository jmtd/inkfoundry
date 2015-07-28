# this is an example instruction file

# first, source files
t/colormap.lmp
t/lavamap.lmp

# then, mapping instructions
# 1. source file
# 2. source range map start (0-33)
# 4. source range map end   (0-33)
# 5. dest range map start (0-33)
# (dest range length derived from source range, overflows are reported)
# 7+ ?

# initialise with base colormap
0   0 33  0
# map the darkest range one up
0  31 31 30
# brightest lavamap -> darkest
1   0  0 31
