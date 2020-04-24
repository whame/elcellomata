#!/usr/bin/env python3

"""
Visualize elementary cellular automata.

Copyright (c) 2020 Waqar Hameed

SPDX-License-Identifier: MIT
"""

__version__ = "0.1"
__url__ = "https://www.github.com/whame/elcellomata"

import argparse
import random
import math
import cairo


def transition(config, rules):
    """Get next state of cell for a rule (Wolfram code).

    :param config: Neighbor configuration.
    :param rules: Rule for state transistion.
    :returns: Next state.
    :raises ValueError: If config is invalid.
    """
    assert len(rules) == 8

    if config == [1, 1, 1]:
        return rules[0]
    elif config == [1, 1, 0]:
        return rules[1]
    elif config == [1, 0, 1]:
        return rules[2]
    elif config == [1, 0, 0]:
        return rules[3]
    elif config == [0, 1, 1]:
        return rules[4]
    elif config == [0, 1, 0]:
        return rules[5]
    elif config == [0, 0, 1]:
        return rules[6]
    elif config == [0, 0, 0]:
        return rules[7]

    raise ValueError(f"Invalid config argument: {config}")


def draw_circle(cairo_context, x, y, radius, fill):
    """Draw a circle.

    :param cairo_context: Cairo context to use when drawing.
    :param x: X center coordinate for the circle.
    :param y: Y center coordinate for the circle.
    :param radius: Radius for the circle.
    :param fill: True if circle should be filled, otherwise false.
    """
    cairo_context.arc(x, y, radius, 0, 2 * math.pi)
    if fill:
        cairo_context.fill()

    cairo_context.stroke()


def draw_line(cairo_context, from_x, from_y, to_x, to_y):
    """Draw a line.

    :param cairo_context: Cairo context to use when drawing.
    :param from_x: Start drawing the line from this X coordinate.
    :param from_y: Start drawing the line from this Y coordinate.
    :param to_x: End drawing the line at this X coordinate.
    :param to_y: End drawing the line at this Y coordinate.
    """
    cairo_context.move_to(from_x, from_y)
    cairo_context.line_to(to_x, to_y)
    cairo_context.stroke()


def print_grid(grid):
    """Print a grid.
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print("¤" if grid[i][j] else ".", end="")

        print()


# Argument parsing.
arg_parser = argparse.ArgumentParser(
    description="Visualize elementary cellular automata.",
    epilog=f"Report bugs to {__url__}.")
arg_parser.add_argument(
    "rule", metavar="RULE", type=int, choices=range(0, 256),
    help="Rule for the cellular automaton.")
arg_parser.add_argument("-o", "--output", metavar="FILE", dest="output_file",
                        help="Output SVG image to FILE. Default is "
                        "\"ruleN.svg\", where N is the rule number RULE.")
arg_parser.add_argument("-p", "--print", action="store_true",
                        help="Print the visualization to stdout.")
arg_parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s" + " " + __version__)
args = arg_parser.parse_args()

# Rule value for the configurations [111, 110, 101, 100, 011, 010, 001, 000].
RULES = [int(c) for c in bin(args.rule)[2:].zfill(8)]

# The cells is represented by a grid of nodes.
GRID_WIDTH = 100
GRID_HEIGHT = 120
GRID_LEFT_RIGHT_PAD = 10
GRID_TOP_BOTTOM_PAD = 20

DRAW_WIDTH_STEP = 15  # Points (pt) between each node on the same grid row.
DRAW_HEIGHT_STEP = 15  # Points (pt) between each node on the same grid column.
DRAW_WIDTH = (GRID_WIDTH - 1 + GRID_LEFT_RIGHT_PAD * 2) * DRAW_WIDTH_STEP
DRAW_HEIGHT = (GRID_HEIGHT - 1 + GRID_TOP_BOTTOM_PAD * 2) * DRAW_HEIGHT_STEP

if not args.output_file:
    args.output_file = "rule" + str(args.rule) + ".svg"

# Initialize Cairo.
crsfc = cairo.SVGSurface(args.output_file, DRAW_WIDTH, DRAW_HEIGHT)
crctx = cairo.Context(crsfc)

crctx.set_source_rgb(1, 1, 1)
crctx.rectangle(0, 0, DRAW_WIDTH, DRAW_HEIGHT)
crctx.fill()
crctx.set_source_rgb(0, 0, 0)
crctx.set_line_cap(cairo.LINE_CAP_ROUND)

# Calculate and draw nodes.
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
grid[0][:] = [random.randint(0, 1) for i in range(GRID_WIDTH)]

for i in range(len(grid) - 1):
    for j in range(len(grid[i])):
        if j == 0:
            # Wrap left edge with right ("infinite plane").
            grid[i + 1][j] = transition([grid[i][-1], *grid[i][0: j + 2]],
                                        RULES)
        elif j == len(grid[i]) - 1:
            # Wrap right edge with left ("infinite plane").
            grid[i + 1][j] = transition([*grid[i][j - 1:], grid[i][0]],
                                        RULES)
        else:
            grid[i + 1][j] = transition(grid[i][j - 1:j + 2], RULES)

        if not grid[i + 1][j]:
            continue

        # Draw lines from previous row neighbors.
        if j and grid[i][j - 1]:
            draw_line(crctx, (j - 1 + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                      (i + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP,
                      (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                      (i + 1 + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP)

        if grid[i][j]:
            draw_line(crctx, (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                      (i + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP,
                      (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                      (i + 1 + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP)

        if j < len(grid[i]) - 1 and grid[i][j + 1]:
            draw_line(crctx, (j + 1 + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                      (i + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP,
                      (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                      (i + 1 + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP)

# Mark nodes with only one neighbor.
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if not grid[i][j]:
            continue

        start_slice = max(0, j - 1)
        stop_slice = min(j + 2, len(grid[i]))
        if i == 0:
            if sum(grid[i + 1][start_slice:stop_slice]) == 1:
                draw_circle(crctx, (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                            (i + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP, 4,
                            True)
        elif i == len(grid) - 1:
            if sum(grid[i - 1][start_slice:stop_slice]) == 1:
                draw_circle(crctx, (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                            (i + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP, 4,
                            True)
        elif sum(grid[i - 1][start_slice:stop_slice]) + \
                sum(grid[i + 1][start_slice:stop_slice]) == 1:
            draw_circle(crctx, (j + GRID_LEFT_RIGHT_PAD) * DRAW_WIDTH_STEP,
                        (i + GRID_TOP_BOTTOM_PAD) * DRAW_HEIGHT_STEP, 4, True)

# Draw rule pattern.
RULE_PATTERN_SCALE = 0.85
RULE_PATTERN_RADIUS = RULE_PATTERN_SCALE * DRAW_WIDTH_STEP
RULE_PATTERN_SPACE = 10 * RULE_PATTERN_RADIUS
RULE_PATTERN_CIRCLE_PAD = 2.5 * RULE_PATTERN_RADIUS
RULE_PATTERN_WIDTH = (7 * RULE_PATTERN_SPACE + 2 * RULE_PATTERN_CIRCLE_PAD +
                      RULE_PATTERN_RADIUS) / DRAW_WIDTH_STEP
RULE_PATTERN_WIDTH = round(RULE_PATTERN_WIDTH)
RULE_PATTERN_X_POS = ((GRID_WIDTH + 2 * GRID_LEFT_RIGHT_PAD -
                       RULE_PATTERN_WIDTH) / 2) * DRAW_WIDTH_STEP
RULE_PATTERN_Y_POS = (DRAW_HEIGHT - GRID_TOP_BOTTOM_PAD * 0.7 *
                      DRAW_HEIGHT_STEP)

for j, rule in enumerate(RULES):
    draw_circle(crctx, RULE_PATTERN_X_POS + j * RULE_PATTERN_SPACE,
                RULE_PATTERN_Y_POS, RULE_PATTERN_RADIUS, (7 - j) & (1 << 2))

    draw_circle(crctx, RULE_PATTERN_X_POS +
                j * RULE_PATTERN_SPACE + RULE_PATTERN_CIRCLE_PAD,
                RULE_PATTERN_Y_POS, RULE_PATTERN_RADIUS, (7 - j) & (1 << 1))

    draw_circle(crctx, RULE_PATTERN_X_POS +
                j * RULE_PATTERN_SPACE + 2 * RULE_PATTERN_CIRCLE_PAD,
                RULE_PATTERN_Y_POS, RULE_PATTERN_RADIUS, (7 - j) & (1 << 0))

    draw_circle(crctx, RULE_PATTERN_X_POS +
                j * RULE_PATTERN_SPACE + RULE_PATTERN_CIRCLE_PAD,
                RULE_PATTERN_Y_POS + RULE_PATTERN_CIRCLE_PAD,
                RULE_PATTERN_RADIUS, rule)

if args.print:
    print_grid(grid)
