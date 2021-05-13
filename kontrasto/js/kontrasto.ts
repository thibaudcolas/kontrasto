import ColorThief from "./color-thief";
import { wcag2_contrast } from "./wcag_2";
import { APCAcontrast } from "./wcag_3";
import { rgbToHex } from "./convert";

interface KontrastoResult {
  text_color: string;
  text_theme: "light" | "dark";
  bg_color: string;
  bg_theme: "light" | "dark";
}

interface KontrastoTarget {
  minX: number;
  maxX: number;
  minY: number;
  maxY: number;
}

export const wcag_2_contrast_light_or_dark = (
  image: HTMLImageElement,
  light_color: string,
  dark_color: string,
  elt: HTMLElement | null = null,
): KontrastoResult => {
  const colorThief = new ColorThief();
  let filterFunction = undefined;
  const target: KontrastoTarget = { minX: 0, maxX: 0, minY: 0, maxY: 0 };
  if (elt) {
    const imageRect = image.getBoundingClientRect();
    const eltRect = elt.getBoundingClientRect();
    target.minX = eltRect.x - imageRect.x;
    target.maxX = target.minX + eltRect.width;
    target.minY = eltRect.y - imageRect.y;
    target.maxY = target.minY + eltRect.height;
    filterFunction = (x: number, y: number) => {
      return (
        x >= target.minX &&
        x <= target.maxX &&
        y >= target.minY &&
        y <= target.maxY
      );
    };
  }

  const rgb: [number, number, number] = colorThief.getColor(
    image,
    10,
    filterFunction,
  );
  const dominant = rgbToHex(...rgb);
  const light_contrast = wcag2_contrast(dominant, light_color);
  const dark_contrast = wcag2_contrast(dominant, dark_color);
  const lighter = light_contrast > dark_contrast;
  return {
    text_color: lighter ? light_color : dark_color,
    text_theme: lighter ? "light" : "dark",
    bg_color: dominant,
    bg_theme: lighter ? "dark" : "light",
  };
};

export const wcag_3_contrast_light_or_dark = (
  image: HTMLImageElement,
  light_color: string,
  dark_color: string,
  elt: HTMLElement | null = null,
): KontrastoResult => {
  const colorThief = new ColorThief();
  let filterFunction = undefined;
  const target: KontrastoTarget = { minX: 0, maxX: 0, minY: 0, maxY: 0 };
  if (elt) {
    const imageRect = image.getBoundingClientRect();
    const eltRect = elt.getBoundingClientRect();
    target.minX = eltRect.x - imageRect.x;
    target.maxX = target.minX + eltRect.width;
    target.minY = eltRect.y - imageRect.y;
    target.maxY = target.minY + eltRect.height;
    filterFunction = (x: number, y: number) => {
      return (
        x >= target.minX &&
        x <= target.maxX &&
        y >= target.minY &&
        y <= target.maxY
      );
    };
  }

  const rgb: [number, number, number] = colorThief.getColor(
    image,
    10,
    filterFunction,
  );
  const dominant = rgbToHex(...rgb);
  const dominantInt = parseInt(dominant.replace(/^#/, ""), 16);
  const light_color_int = parseInt(light_color.replace(/^#/, ""), 16);
  const dark_color_int = parseInt(dark_color.replace(/^#/, ""), 16);
  const light_contrast = Math.abs(APCAcontrast(dominantInt, light_color_int));
  const dark_contrast = Math.abs(APCAcontrast(dominantInt, dark_color_int));
  const lighter = light_contrast > dark_contrast;
  return {
    text_color: lighter ? light_color : dark_color,
    text_theme: lighter ? "light" : "dark",
    bg_color: dominant,
    bg_theme: lighter ? "dark" : "light",
  };
};
