// add the beginning of your app entry
import "vite/dynamic-import-polyfill";

import {
  wcag_2_contrast_light_or_dark,
  wcag_3_contrast_light_or_dark,
} from "../../kontrasto/js/kontrasto";

import "./style.css";

const images = [].slice.call(document.querySelectorAll("img"));
const demoText = [].slice.call(document.querySelectorAll("[data-demo-text]"));
const test_image_text = document.querySelector<HTMLInputElement>(
  "#test_image_text",
);

declare global {
  interface Window {
    requestIdleCallback(
      callback: () => void,
      options?: { timeout: number },
    ): void;
  }
}

const applyContrastBackground = () => {
  images.forEach((img) => {
    const testElt = [].slice.call(
      img.closest("div").querySelectorAll("[data-client-only]"),
    );

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
  });
};

/**
 * Delays an operation by 1-2x the given timeout, then requests
 * idle time so the operation doesn’t affect app performance.
 */
const delayAndIdle = (callback, timeoutHandle, timeout) => {
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

let timeoutHandle;

if (test_image_text) {
  test_image_text.addEventListener(
    "keyup",
    (e: Event) => {
      const target = e.target as HTMLInputElement;

      timeoutHandle = delayAndIdle(
        () => {
          demoText.forEach((elt) => (elt.innerText = target.value));
          applyContrastBackground();
        },
        timeoutHandle,
        100,
      );
    },
    { passive: true },
  );
}

delayAndIdle(
  () => {
    applyContrastBackground();
  },
  null,
  100,
);

window.addEventListener("resize", () => {
  delayAndIdle(
    () => {
      applyContrastBackground();
    },
    null,
    100,
  );
});
