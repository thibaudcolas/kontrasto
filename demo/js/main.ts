// add the beginning of your app entry
import "vite/dynamic-import-polyfill";

import {
  wcag_2_contrast_light_or_dark,
  wcag_3_contrast_light_or_dark,
} from "../../kontrasto/js/kontrasto";

import "./style.css";

const images = [...document.querySelectorAll<HTMLImageElement>("img")];
const demoText = [
  ...document.querySelectorAll<HTMLElement>("[data-demo-text]"),
];

declare global {
  interface Window {
    requestIdleCallback(
      callback: () => void,
      options?: { timeout: number },
    ): void;
  }
}

const applyContrastBackgroundImage = (img: HTMLImageElement) => {
  const imgParent = img.closest("[data-demo-parent]");
  const testElt = imgParent
    ? [...imgParent.querySelectorAll<HTMLElement>("[data-client-only]")]
    : [];

  testElt.forEach((elt) => {
    let result;
    if (elt.hasAttribute("data-wcag-next")) {
      result = wcag_3_contrast_light_or_dark(img, "#ffffff", "#000000", elt);
    } else {
      result = wcag_2_contrast_light_or_dark(img, "#ffffff", "#000000", elt);
    }
    // console.log(elt.getBoundingClientRect(), img.getBoundingClientRect());
    elt.style.setProperty("--kontrasto-bg", `${result.bg_color}99`);
    elt.style.setProperty("--kontrasto-text", result.text_color);
  });
};
const applyContrastBackground = () => {
  images.forEach((img, i) => {
    if (img.complete) {
      delayAndIdle(() => applyContrastBackgroundImage(img), 0, 300 + i * 300);
    } else {
      img.addEventListener("load", () => {
        delayAndIdle(() => applyContrastBackgroundImage(img), 0, 100);
      });
    }
  });
};

/**
 * Delays an operation by 1-2x the given timeout, then requests
 * idle time so the operation doesn’t affect app performance.
 */
const delayAndIdle = (
  callback: () => void,
  timeoutHandle: number,
  timeout: number,
) => {
  if (timeoutHandle) {
    window.clearTimeout(timeoutHandle);
  }

  return window.setTimeout(() => {
    if (window.requestIdleCallback) {
      window.requestIdleCallback(callback, { timeout });
    } else {
      callback();
    }
  }, timeout);
};

applyContrastBackground();

window.addEventListener("resize", applyContrastBackground, { passive: true });
