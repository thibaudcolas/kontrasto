// See https://github.com/tmcw/relative-luminance/blob/c44102403b588ee584752d4fd5f703bac6f87910/index.js.
// # Relative luminance
//
// http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
// https://en.wikipedia.org/wiki/Luminance_(relative)
// https://en.wikipedia.org/wiki/Luminosity_function
// https://en.wikipedia.org/wiki/Rec._709#Luma_coefficients

// red, green, and blue coefficients
const rc = 0.2126;
const gc = 0.7152;
const bc = 0.0722;
// low-gamma adjust coefficient
const lowc = 1 / 12.92;

function adjustGamma(_) {
  return Math.pow((_ + 0.055) / 1.055, 2.4);
}

/**
 * Given a 3-element array of R, G, B varying from 0 to 255, return the luminance
 * as a number from 0 to 1.
 * @param {Array<number>} rgb 3-element array of a color
 * @returns {number} luminance, between 0 and 1
 * @example
 * var luminance = require('relative-luminance');
 * var black_lum = luminance([0, 0, 0]); // 0
 */
export function relativeLuminance(rgb) {
  const rsrgb = rgb[0] / 255;
  const gsrgb = rgb[1] / 255;
  const bsrgb = rgb[2] / 255;

  const r = rsrgb <= 0.03928 ? rsrgb * lowc : adjustGamma(rsrgb);
  const g = gsrgb <= 0.03928 ? gsrgb * lowc : adjustGamma(gsrgb);
  const b = bsrgb <= 0.03928 ? bsrgb * lowc : adjustGamma(bsrgb);

  return r * rc + g * gc + b * bc;
}

/**
 * See https://github.com/tmcw/wcag-contrast/blob/11c1a9036a716ef0cb553c8f805b64b9945eb50b/index.js.
 */

const hexChars = "a-f\\d";
const match3or4Hex = `#?[${hexChars}]{3}[${hexChars}]?`;
const match6or8Hex = `#?[${hexChars}]{6}([${hexChars}]{2})?`;

function hexRgb(hex: string) {
  hex = hex.replace(/^#/, "");
  let alpha = 255;

  if (hex.length === 8) {
    alpha = parseInt(hex.slice(6, 8), 16);
    hex = hex.substring(0, 6);
  }

  if (hex.length === 4) {
    alpha = parseInt(hex.slice(3, 4).repeat(2), 16);
    hex = hex.substring(0, 3);
  }

  if (hex.length === 3) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }

  const num = parseInt(hex, 16);
  const red = num >> 16;
  const green = (num >> 8) & 255;
  const blue = num & 255;

  return [red, green, blue, alpha];
}

// http://www.w3.org/TR/WCAG20/#contrast-ratiodef

/**
 * Get the contrast ratio between two relative luminance values
 * @param {number} a luminance value
 * @param {number} b luminance value
 * @returns {number} contrast ratio
 * @example
 * luminance(1, 1); // = 1
 */
export function luminance(a, b) {
  const l1 = Math.max(a, b);
  const l2 = Math.min(a, b);
  return (l1 + 0.05) / (l2 + 0.05);
}

/**
 * Get a score for the contrast between two colors as rgb triplets
 * @param {array} a
 * @param {array} b
 * @returns {number} contrast ratio
 * @example
 * rgb([0, 0, 0], [255, 255, 255]); // = 21
 */
export function rgb(a, b) {
  return luminance(relativeLuminance(a), relativeLuminance(b));
}

/**
 * Get a score for the contrast between two colors as hex strings
 * @param {string} a hex value
 * @param {string} b hex value
 * @returns {number} contrast ratio
 * @example
 * hex('#000', '#fff'); // = 21
 */
export function hex(a: string, b: string) {
  return rgb(hexRgb(a), hexRgb(b));
}

/**
 * Get a textual score from a numeric contrast value
 * @param {number} contrast
 * @returns {string} score
 * @example
 * score(10); // = 'AAA'
 */
export function score(contrast) {
  if (contrast >= 7) {
    return "AAA";
  }

  if (contrast >= 4.5) {
    return "AA";
  }

  if (contrast >= 3) {
    return "AA Large";
  }

  return "Fail";
}

export const wcag2_contrast = hex;
