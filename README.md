Elcellomata
===========

![onefifty](https://user-images.githubusercontent.com/9569246/97764435-f8a53200-1b0e-11eb-988b-e0e17fac4b09.png)

Elcellomata is a small tool to visualize elementeray cellular automata. The
visualization is intended to be somewhat "artistic" in style (inspired by
[Micheal Fogelman](https://store.michaelfogleman.com/)): lines are drawn between
active neighbor cells and single active cells with no neighbors are drawn with a
filled circle. The rule pattern is also drawn at the bottom.

# Dependencies

Elcellomata needs [pycairo](https://github.com/pygobject/pycairo) for drawing.
Install that with:

```
python3 -m pip install pycairo
```
# Example

```
./elcellomata.py 150 -o onefifty.svg
```

You can change the values of the variables `GRID_WIDTH`, `GRID_HEIGHT`,
`DRAW_WIDTH_STEP`, `DRAW_HEIGHT_STEP` and `RULE_PATTERN_SCALE` in the script to
change the size of the output to your liking.
