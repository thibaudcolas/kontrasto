import math
from typing import Iterable

from .convert import to_rgb
from .lookup_table import get_apca_font_styles

# Python port of: https://github.com/Myndex/SAPC-APCA/blob/master/JS/APCAonly.98e_d12e.js
def apca_contrast(background, text):
    if isinstance(background, str):
        background = to_rgb(background)
    if isinstance(text, str):
        text = to_rgb(text)

    Rbg, Gbg, Bbg = background
    Rtxt, Gtxt, Btxt = text

    # /////  MAGICAL NUMBERS  ///////////////////////////////

    # /////  sRGB Conversion to Relative Luminance (Y)  /////

    mainTRC = 2.4  # Transfer Curve (aka "Gamma") for sRGB linearization
    # // Simple power curve vs piecewise described in docs
    # // Essentially, 2.4 best models actual display
    # // characteristics in combination with the total method

    mainTRCencode = 0.41666666666666666667  # = 1.0/mainTRC;

    Rco = 0.2126729  # sRGB Red Coefficient (from matrix)
    Gco = 0.7151522  # sRGB Green Coefficient (from matrix)
    Bco = 0.072175  # sRGB Blue Coefficient (from matrix)

    # /////  For Finding Raw SAPC Contrast from Relative Luminance (Y)  /////

    normBG = 0.55  # Constants for SAPC Power Curve Exponents
    normTXT = 0.58  # One pair for normal text, and one for reverse
    revTXT = 0.57  # These are the "beating heart" of SAPC
    revBG = 0.62

    # /////  For Clamping and Scaling Values  /////

    blkThrs = 0.03  # Level that triggers the soft black clamp
    blkClmp = 1.45  # Exponent for the soft black clamp curve
    deltaYmin = 0.0005  # Lint trap
    scaleBoW = 1.25  # Scaling for dark text on light
    scaleWoB = 1.25  # Scaling for light text on dark
    loConThresh = 0.078  # Threshold for new simple offset scale
    loConFactor = 12.82051282051282  # = 1/0.078,
    loConOffset = 0.06  # The simple offset
    loClip = 0.001  # Output clip (lint trap #2)

    # // We are only concerned with Y at this point
    # // Ybg and Ytxt: divide sRGB to 0.0-1.0 range, linearize,
    # // and then apply the standard coefficients and sum to Y.
    # // Note that the Y we create here is unique and designed
    # // exclusively for SAPC. Do not use Y from other methods.

    Ybg = (
        math.pow(Rbg / 255.0, mainTRC) * Rco
        + math.pow(Gbg / 255.0, mainTRC) * Gco
        + math.pow(Bbg / 255.0, mainTRC) * Bco
    )

    Ytxt = (
        math.pow(Rtxt / 255.0, mainTRC) * Rco
        + math.pow(Gtxt / 255.0, mainTRC) * Gco
        + math.pow(Btxt / 255.0, mainTRC) * Bco
    )

    SAPC = 0.0  # For holding raw SAPC values
    outputContrast = 0.0  # For weighted final values

    # ///// TUTORIAL  /////

    # // Take Y and soft clamp black, return 0 for very close luminances
    # // determine polarity, and calculate SAPC raw contrast
    # // Then apply the output scaling

    # // Note that reverse contrast (white text on black)
    # // intentionally returns a negative number
    # // Proper polarity is important!

    # //////////   BLACK SOFT CLAMP & INPUT CLIP  ////////////////////////////////

    # // Soft clamp Y when near black.
    # // Now clamping all colors to prevent crossover errors
    Ytxt = (
        Ytxt if (Ytxt > blkThrs) else Ytxt + math.pow(blkThrs - Ytxt, blkClmp)
    )
    Ybg = Ybg if (Ybg > blkThrs) else Ybg + math.pow(blkThrs - Ybg, blkClmp)

    # /////   Return 0 Early for extremely low ∆Y (lint trap #1) /////
    if math.fabs(Ybg - Ytxt) < deltaYmin:
        return 0.0

    # //////////   SAPC CONTRAST   ///////////////////////////////////////////////

    if Ybg > Ytxt:
        # // For normal polarity, black text on white

        # ///// Calculate the SAPC contrast value and scale

        SAPC = (math.pow(Ybg, normBG) - math.pow(Ytxt, normTXT)) * scaleBoW

        # ///// NEW! SAPC SmoothScale™
        # // Low Contrast Smooth Scale Rollout to prevent polarity reversal
        # // and also a low clip for very low contrasts (lint trap #2)
        # // much of this is for very low contrasts, less than 10
        # // therefore for most reversing needs, only loConOffset is important
        if SAPC < loClip:
            outputContrast = 0.0
        elif SAPC < loConThresh:
            outputContrast = SAPC - SAPC * loConFactor * loConOffset
        else:
            outputContrast = SAPC - loConOffset
    else:
        # // For reverse polarity, light text on dark
        # // WoB should always return negative value.

        SAPC = (math.pow(Ybg, revBG) - math.pow(Ytxt, revTXT)) * scaleWoB

        if SAPC > -loClip:
            outputContrast = 0.0
        elif SAPC > -loConThresh:
            outputContrast = SAPC - SAPC * loConFactor * loConOffset
        else:
            outputContrast = SAPC + loConOffset

    return outputContrast * 100


def format_contrast(score: float) -> str:
    score = abs(score)
    return score


def get_font_styles(score: float, weights: Iterable[int], sizes: Iterable[int]):
    styles = get_apca_font_styles(score)
    if len(styles) == 0:
        return False
    matching_styles = []
    for style in styles:
        if style["weight"] >= weights[0] and style["weight"] <= weights[-1]:
            if style["size"] >= sizes[0] and style["size"] <= sizes[-1]:
                matching_styles.append((style["size"], style["weight"]))

    return matching_styles
