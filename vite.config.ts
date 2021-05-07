import { defineConfig } from "vite";
import path from "path";

export default ({ command, mode }) => {
  const baseConfig = {
    base: "/static/",
    root: "",
  };

  if (mode === "lib") {
    return {
      ...baseConfig,
      build: {
        outDir: "dist",
        manifest: false,
        lib: {
          entry: path.resolve(__dirname, "kontrasto/static/kontrasto.ts"),
          name: "kontrasto",
        },
      },
    };
  }

  return {
    ...baseConfig,
    build: {
      outDir: "demo/static_vite",
      manifest: true,
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, "demo/js/main.ts"),
        },
      },
    },
  };
};
