# Human cursor motion for demo recordings

**As whoever records or edits the Flatland demo GIFs, I need to know how a real hand moves a mouse, with
numbers, so the scripted cursor reads as a person working and not as a robot, while staying clean enough
for a portfolio.**

The recorder's `move()` in `drv.py` follows the recipe below. Every demo calls it, so a change there
changes every GIF.

## The short version

1. Never a straight line. Every move bows gently to one side.
2. Never a constant speed. Every move speeds up, peaks a little early, and settles into the target.
3. Long reaches carry on a little past the target in the direction they were travelling, then come back.
   They rarely leave the target to do it.
4. Short moves often stop a hair short and creep in.
5. Never the same landing spot twice: each object gets its own point, not the same offset every time.
6. A short pause before each click.
7. No jitter, no wandering, no visible zigzags. Those read as sloppy, not human.

## What the research says

### Speed: a bell curve that peaks a little early

Smooth reaching movements follow the minimum-jerk profile: the hand's speed over time is a bell curve,
and its peak is about 1.875 times the average speed ([Flash and Hogan 1985](https://newmanlab-mit-edu.ezproxyberklee.flo.org/wp-content/uploads/2017/09/1985-the-coordination-of-arm-movements-an-experimentally-confirmed-mathematical-model.pdf)).
Measured rapid movements have a bell that is skewed rather than symmetric, which Plamondon's kinematic
theory models with lognormal curves ([lognormality review 2017](https://eprints-gro.gold.ac.uk/20616/1/lognormality_2017.pdf)).
Motion designers reached the same rule by eye: "slow in and slow out," now called easing
([Twelve basic principles of animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)).

What we take: minimum-jerk easing with time warped so the peak lands near 40% of the move.

### Paths: curved, but only slightly

The minimum-jerk model predicts straight hand paths, but real mouse paths are not straight. MacKenzie,
Kauppinen and Silfverberg measured mouse paths and found an average distance from the straight line of
11.6 px, a spread of 10.5 px, and a consistent lean to one side of 2.5 px, at 0.43 mm per pixel
([MacKenzie et al. 2001](https://www.yorku.ca/mack/CHI01.htm)). The arcs principle of animation says the
same: natural motion follows arcs ([Twelve basic principles of animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)).
Tools that fake human motion agree on two points: straight lines and uniform angles are what give a
script away ([Ben Land, WindMouse](https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/)),
and a curve that bows to one side looks right where an S-curve looks wrong
([ghost-cursor](https://github.com/Xetera/ghost-cursor)).

What we take: one gentle arc per move, bowing to one side, with a peak distance from the straight line of
3 to 5% of the move. That is about 10 to 15 px on a 300 px move, in line with MacKenzie's numbers.

### Corrections: overshoot is common, leaving the target is rare

Aimed movements are a main move plus, often, a small corrective move (Meyer et al. 1988, the optimized
submovement model). Roberts, Burkitt and Elliott found a correction after an overshoot in about 60 to 78% of trials, and
more often for fast movements ([Roberts et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10973010)).
Final endpoints landed within about 2% of the distance moved (our arithmetic from that study's radial
error). But with a mouse, the cursor leaves the target and comes back in only 0.07 of trials
([MacKenzie et al. 2001](https://www.yorku.ca/mack/CHI01.htm)). So most overshoots stay inside the target.

What we take: on long reaches, land 1 to 2% past the target, mostly still on it, and correct in a short
second move. The overshoot follows the heading the hand had as it arrived (the tangent of the arc), not
the straight line from the start, because momentum carries the hand the way it was already going. A visible exit and return is rare and small. Short moves stop 1 to 3 px short and creep in.

### Timing: farther and smaller takes longer

Fitts's law sets how long a move takes: time = a + b × log2(distance / width + 1)
([MacKenzie 1992](https://www.yorku.ca/mack/gi92.pdf)). For pointing with a mouse, MacKenzie and Buxton
measured 177 ms + 169 ms per bit ([MacKenzie and Buxton 1994](https://www.billbuxton.com/IWC.html)): a
500 px reach to a 20 px button is about 4.7 bits, so about 0.97 s.

What we take: the demos keep their choreographed timings, since a GIF needs pacing a viewer can follow
(the recordings also play back 1.5 times faster). Use Fitts's law as a check when editing a demo: a long
reach to a small button should get more time than a short hop to a big one.

### Rhythm: repeats speed up, and no two pauses match

A demo that repeats an action (Pathfinder does it four times) gives its timing away if every repeat takes
the same time. Human interval timing varies by about 10 to 20% of the interval each time
([Wearden 1991](https://www.keele.ac.uk/media/keeleuniversity/facnatsci/schpsych/weardenpublications/wearden1991.pdf);
[Lewis and Miall 2009](https://orca.cardiff.ac.uk/id/eprint/86700/)), and response times are skewed: mostly
quick, with the odd longer one ([Liu et al.](https://arxiv.org/pdf/1510.04245)). People also get faster as
they repeat a task, the law of practice ([Evans et al. 2018](https://dare.uva.nl/id/717fcfb1-edf1-4010-9959-2b0acccb9c8b)).
The Keystroke-Level Model adds a pause to think (1.35 s) before a step that is not predictable, and drops
it when the next step is obvious ([Keystroke-Level Model](https://en.wikipedia.org/wiki/Keystroke-level_model)).

What we take: every pause comes from `jit()` in `common.py`, a lognormal draw that varies 15 to 20% around
its base. Repeats get quicker (Pathfinder's four pairs run at 100, 90, 82 and 76% of the first pair's
pace). The look at each result stays the longest pause, so a viewer can take it in. The second click of a
pair is quicker than the first, since it is the predictable step. Repeats also vary what the hand does:
the order of clicks changes, and one pair is picked with a box drag.

### Before the click: a short pause

People pause to aim before clicking. Pauses over 0.2 s are already counted as hesitation in HCI work
([Leuphana HCI 2019 slides](https://ml3.leuphana.de/team/content/HCI2019.pdf)).

What we take: 0.1 to 0.2 s of stillness before a click, no longer.

### Tremor: real, but invisible here

Hand tremor sits at 8 to 12 Hz with an RMS amplitude of 50 to 200 micrometres at the hand
([Wells et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3989364)). At normal mouse speed that is a pixel
or less on screen, and less again in a GIF shown at half size.

What we take: no jitter. Added shake would be bigger than real tremor and would read as noise.

## The recipe

| Setting | Value | Why |
|---|---|---|
| Speed curve | minimum jerk, time warped by t^0.8 | bell curve, peak near 40% |
| Arc | control point 6 to 10% of the distance off the midpoint, one side per move | peak bow of 3 to 5% |
| Long-reach overshoot | moves over 260 px land 1 to 2% past along the arriving heading, then a 0.1 to 0.15 s correction | overshoot is common, leaving the target is rare |
| Exit and return | at most 1 in 8 long reaches, 3% past | target re-entry is rare |
| Short-move settle | most moves over 30 px stop 1 to 3 px short along the arriving heading, then creep in | the small corrective move |
| Landing spots | each demo picks a different point on each object (and a few px of play on buttons) | repeated identical landings read as a script |
| Pause before click | 0.1 to 0.2 s | aiming pause, below hesitation |
| Sampling | 60 positions per second | smooth at the GIF's 12 frames per second |
| Jitter | none | tremor is under a pixel |
| Randomness | seeded by each move's start and end | a rerun records the same take |
| Pauses | `jit(base)`: lognormal, about 15% (20% for a look at a result) | timing varies, skewed to the odd long pause |
| Repeats | each repeat about 10% quicker than the last, down to about 75% | the law of practice |
| Cursor | a standard white arrow drawn on afterwards (`cursor.py`) | Xvfb only has the X11 'X' cursor |

## Sources

- Flash and Hogan 1985, The coordination of arm movements: [PDF](https://newmanlab-mit-edu.ezproxyberklee.flo.org/wp-content/uploads/2017/09/1985-the-coordination-of-arm-movements-an-experimentally-confirmed-mathematical-model.pdf)
- Plamondon's kinematic theory, lognormality review 2017: [PDF](https://eprints-gro.gold.ac.uk/20616/1/lognormality_2017.pdf)
- MacKenzie, Kauppinen and Silfverberg 2001, Accuracy measures for evaluating computer pointing devices: [page](https://www.yorku.ca/mack/CHI01.htm)
- Roberts, Burkitt and Elliott 2024, The type 1 submovement conundrum: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10973010)
- MacKenzie 1992, Fitts' law as a research and design tool in HCI: [PDF](https://www.yorku.ca/mack/gi92.pdf)
- MacKenzie and Buxton 1994, The prediction of pointing and dragging times in graphical user interfaces: [page](https://www.billbuxton.com/IWC.html)
- Leuphana HCI 2019, hesitation measures: [PDF](https://ml3.leuphana.de/team/content/HCI2019.pdf)
- Wells et al. 2013, Comparison of baseline tremor under various microsurgical conditions: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3989364)
- Ben Land 2021, WindMouse: [post](https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/)
- ghost-cursor: [repo](https://github.com/Xetera/ghost-cursor)
- Wearden 1991, human chronometric counting: [PDF](https://www.keele.ac.uk/media/keeleuniversity/facnatsci/schpsych/weardenpublications/wearden1991.pdf)
- Lewis and Miall 2009, timing across intervals: [page](https://orca.cardiff.ac.uk/id/eprint/86700/)
- Liu et al., Modeling response time with power-law distributions: [arXiv](https://arxiv.org/pdf/1510.04245)
- Evans, Brown, Mewhort and Heathcote 2018, Refining the law of practice: [page](https://dare.uva.nl/id/717fcfb1-edf1-4010-9959-2b0acccb9c8b)
- Keystroke-Level Model (Card, Moran and Newell 1980): [article](https://en.wikipedia.org/wiki/Keystroke-level_model)
- Twelve basic principles of animation: [article](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)
