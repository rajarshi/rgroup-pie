import math

from openeye import oechem, oedepict, oegrapheme
from openeye.oechem import OEBlack, OEGraphMol, OEReadMolecule, OEWhite
from openeye.oedepict import OE2DMolDisplay

# Constants
RGRP_IDX = 1
WEDGE_WIDTH = 30
RADIUS_BASE = 40
START_ANGLE = 5
SEGMENT_LABEL_SCALE_FACTOR = 1.3

ifs = oechem.oemolistream()
ifs.open("rgrouppie.mol")
mol = OEGraphMol()
OEReadMolecule(ifs, mol)

######################################

oedepict.OEPrepareDepiction(mol)
mdisp = OE2DMolDisplay(mol)

# Get display coordinates of the R group atom
r_coords = None
for atom in mol.GetAtoms():
    if atom.GetMapIdx() == 1:
        r_coords = mdisp.GetAtomDisplay(atom).GetCoords()

# Create base image
image = oedepict.OEImage(300, 300)

# Draw pie segments
vals = [[100, ">99", 50, 12],
        [78, 12, 34, 77]]
n_ring = len(vals)

# Get the layer into which we will draw the pie chart
layer = mdisp.GetLayer(oedepict.OELayerPosition_Below)

# Set up pens
pen_green = oedepict.OEPen(oechem.OELightGreen, oechem.OEBlack, oedepict.OEFill_On, 1.0)
pen_red = oedepict.OEPen(oechem.OELightPurple, oechem.OEBlack, oedepict.OEFill_On, 1.0)
pens = [pen_green, pen_red]

gradients = [oechem.OELinearColorGradient(oechem.OEColorStop(0, oechem.OEWhite), oechem.OEColorStop(100, oechem.OEGreen)),
             oechem.OELinearColorGradient(oechem.OEColorStop(0, oechem.OEWhite), oechem.OEColorStop(100, oechem.OERed))]

# Draw rings from outside inwards
for ring_num in range(n_ring):
    starting_angle = START_ANGLE
    ring = vals[ring_num]
    for value in ring:
        radius = (n_ring - ring_num) * RADIUS_BASE

        if isinstance(value, str) and ">" in value:
            value_for_color = 100
        else: value_for_color = value
        gradient = gradients[ring_num]
        color = gradient.GetColorAt(value_for_color)
        pen = oedepict.OEPen(color, oechem.OEBlack, oedepict.OEFill_On, 1.0)

        layer.DrawPie(r_coords, starting_angle, starting_angle + WEDGE_WIDTH, radius, pen)

        # Write value in segment - based on
        # https://docs.eyesopen.com/toolkits/cookbook/python/_downloads/properties2img.py
        p = oedepict.OE2DPoint(0, -radius * 0.75)
        midangle = (starting_angle + starting_angle + WEDGE_WIDTH) / 2.0
        rad = math.radians(midangle)
        cosrad = math.cos(rad)
        sinrad = math.sin(rad)
        txt_coord = r_coords + oedepict.OE2DPoint(cosrad * p.GetX() - sinrad * p.GetY(),
                                                  sinrad * p.GetX() + cosrad * p.GetY())

        fontsize = int(SEGMENT_LABEL_SCALE_FACTOR * math.sqrt(radius))
        font = oedepict.OEFont(oedepict.OEFontFamily_Default, oedepict.OEFontStyle_Bold, fontsize,
                               oedepict.OEAlignment_Center, oechem.OEBlack)
        label = oedepict.OEHighlightLabel(str(value), font)
        label.SetBoundingBoxPen(oedepict.OETransparentPen)
        oedepict.OEAddLabel(layer, txt_coord, label)

        starting_angle += WEDGE_WIDTH

# Draw circle round R atom on top of pie chart center
pen = oedepict.OEPen(OEWhite, OEBlack, oedepict.OEFill_On, 1)
glyph = oegrapheme.OEAtomGlyphCircle(pen, oegrapheme.OECircleStyle_Default, 1.5)
oegrapheme.OEAddGlyph(mdisp, glyph, oechem.OEHasMapIdx(1))

# Render molecule
oedepict.OERenderMolecule(image, mdisp)


# Write out images
oedepict.OEWriteImage("MolWithWedgeChart.svg", image)
oedepict.OEWriteImage("MolWithWedgeChart.png", image)
