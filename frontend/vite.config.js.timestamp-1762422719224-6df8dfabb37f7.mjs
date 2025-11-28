// vite.config.js
import { defineConfig } from "file:///workspace/development/frappe-bench/apps/lms/frontend/node_modules/vite/dist/node/index.js";
import vue from "file:///workspace/development/frappe-bench/apps/lms/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import path from "path";
import frappeui from "file:///workspace/development/frappe-bench/apps/lms/frontend/node_modules/frappe-ui/vite/index.js";
import { VitePWA } from "file:///workspace/development/frappe-bench/apps/lms/node_modules/vite-plugin-pwa/dist/index.js";
import ui from "file:///workspace/development/frappe-bench/apps/lms/frontend/node_modules/@nuxt/ui/dist/vite.mjs";
var __vite_injected_original_dirname = "/workspace/development/frappe-bench/apps/lms/frontend";
var vite_config_default = defineConfig({
  plugins: [
    frappeui({
      frappeProxy: true,
      lucideIcons: true,
      jinjaBootData: true,
      frappeTypes: {
        input: {}
      },
      buildConfig: {
        indexHtmlPath: "../lms/www/lms.html"
      }
    }),
    vue({
      script: {
        defineModel: true,
        propsDestructure: true
      }
    }),
    VitePWA({
      registerType: "autoUpdate",
      devOptions: {
        enabled: true
      },
      workbox: {
        cleanupOutdatedCaches: true,
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024
      },
      manifest: {
        display: "standalone",
        name: "Learning",
        short_name: "Learning",
        start_url: "/lms",
        description: "Easy to use, 100% open source Learning Management System",
        theme_color: "#0f7159",
        background_color: "#ffffff",
        icons: [
          {
            src: "/assets/lms/frontend/manifest/manifest-icon-192.maskable.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable any"
          },
          {
            src: "/assets/lms/frontend/manifest/manifest-icon-512.maskable.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable any"
          }
        ]
      }
    }),
    ui({})
  ],
  server: {
    host: "0.0.0.0",
    // Accept connections from any network interface
    allowedHosts: ["ps", "fs", "home"]
    // Explicitly allow this host
  },
  resolve: {
    alias: {
      "@": path.resolve(__vite_injected_original_dirname, "src"),
      "tailwind.config.js": path.resolve(__vite_injected_original_dirname, "tailwind.config.js"),
      "@nuxtapp": path.resolve(__vite_injected_original_dirname, "../../maxlms/nuxtapp")
    }
  },
  optimizeDeps: {
    include: [
      "feather-icons",
      "showdown",
      "engine.io-client",
      "tailwind.config.js",
      "interactjs",
      "highlight.js",
      "plyr"
    ]
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvd29ya3NwYWNlL2RldmVsb3BtZW50L2ZyYXBwZS1iZW5jaC9hcHBzL2xtcy9mcm9udGVuZFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiL3dvcmtzcGFjZS9kZXZlbG9wbWVudC9mcmFwcGUtYmVuY2gvYXBwcy9sbXMvZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL3dvcmtzcGFjZS9kZXZlbG9wbWVudC9mcmFwcGUtYmVuY2gvYXBwcy9sbXMvZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnXG5pbXBvcnQgcGF0aCBmcm9tICdwYXRoJ1xuaW1wb3J0IGZyYXBwZXVpIGZyb20gJ2ZyYXBwZS11aS92aXRlJ1xuaW1wb3J0IHsgVml0ZVBXQSB9IGZyb20gJ3ZpdGUtcGx1Z2luLXB3YSdcbmltcG9ydCB1aSBmcm9tICdAbnV4dC91aS92aXRlJztcblxuLy8gaHR0cHM6Ly92aXRlanMuZGV2L2NvbmZpZy9cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG5cdHBsdWdpbnM6IFtcblx0XHRmcmFwcGV1aSh7XG5cdFx0XHRmcmFwcGVQcm94eTogdHJ1ZSxcblx0XHRcdGx1Y2lkZUljb25zOiB0cnVlLFxuXHRcdFx0amluamFCb290RGF0YTogdHJ1ZSxcblx0XHRcdGZyYXBwZVR5cGVzOiB7XG5cdFx0XHRcdGlucHV0OiB7fSxcblx0XHRcdH0sXG5cdFx0XHRidWlsZENvbmZpZzoge1xuXHRcdFx0XHRpbmRleEh0bWxQYXRoOiAnLi4vbG1zL3d3dy9sbXMuaHRtbCcsXG5cdFx0XHR9LFxuXHRcdH0pLFxuXHRcdHZ1ZSh7XG5cdFx0XHRzY3JpcHQ6IHtcblx0XHRcdFx0ZGVmaW5lTW9kZWw6IHRydWUsXG5cdFx0XHRcdHByb3BzRGVzdHJ1Y3R1cmU6IHRydWUsXG5cdFx0XHR9LFxuXHRcdH0pLFxuXHRcdFZpdGVQV0Eoe1xuXHRcdFx0cmVnaXN0ZXJUeXBlOiAnYXV0b1VwZGF0ZScsXG5cdFx0XHRkZXZPcHRpb25zOiB7XG5cdFx0XHRcdGVuYWJsZWQ6IHRydWUsXG5cdFx0XHR9LFxuXHRcdFx0d29ya2JveDoge1xuXHRcdFx0XHRjbGVhbnVwT3V0ZGF0ZWRDYWNoZXM6IHRydWUsXG5cdFx0XHRcdG1heGltdW1GaWxlU2l6ZVRvQ2FjaGVJbkJ5dGVzOiA1ICogMTAyNCAqIDEwMjQsXG5cdFx0XHR9LFxuXHRcdFx0bWFuaWZlc3Q6IHtcblx0XHRcdFx0ZGlzcGxheTogJ3N0YW5kYWxvbmUnLFxuXHRcdFx0XHRuYW1lOiAnTGVhcm5pbmcnLFxuXHRcdFx0XHRzaG9ydF9uYW1lOiAnTGVhcm5pbmcnLFxuXHRcdFx0XHRzdGFydF91cmw6ICcvbG1zJyxcblx0XHRcdFx0ZGVzY3JpcHRpb246XG5cdFx0XHRcdFx0J0Vhc3kgdG8gdXNlLCAxMDAlIG9wZW4gc291cmNlIExlYXJuaW5nIE1hbmFnZW1lbnQgU3lzdGVtJyxcblx0XHRcdFx0dGhlbWVfY29sb3I6ICcjMGY3MTU5Jyxcblx0XHRcdFx0YmFja2dyb3VuZF9jb2xvcjogJyNmZmZmZmYnLFxuXHRcdFx0XHRpY29uczogW1xuXHRcdFx0XHRcdHtcblx0XHRcdFx0XHRcdHNyYzogJy9hc3NldHMvbG1zL2Zyb250ZW5kL21hbmlmZXN0L21hbmlmZXN0LWljb24tMTkyLm1hc2thYmxlLnBuZycsXG5cdFx0XHRcdFx0XHRzaXplczogJzE5MngxOTInLFxuXHRcdFx0XHRcdFx0dHlwZTogJ2ltYWdlL3BuZycsXG5cdFx0XHRcdFx0XHRwdXJwb3NlOiAnbWFza2FibGUgYW55Jyxcblx0XHRcdFx0XHR9LFxuXHRcdFx0XHRcdHtcblx0XHRcdFx0XHRcdHNyYzogJy9hc3NldHMvbG1zL2Zyb250ZW5kL21hbmlmZXN0L21hbmlmZXN0LWljb24tNTEyLm1hc2thYmxlLnBuZycsXG5cdFx0XHRcdFx0XHRzaXplczogJzUxMng1MTInLFxuXHRcdFx0XHRcdFx0dHlwZTogJ2ltYWdlL3BuZycsXG5cdFx0XHRcdFx0XHRwdXJwb3NlOiAnbWFza2FibGUgYW55Jyxcblx0XHRcdFx0XHR9LFxuXHRcdFx0XHRdLFxuXHRcdFx0fSxcblx0XHR9KSxcblx0XHR1aSh7XG5cdFx0XHRcblx0XHR9KSxcblx0XSxcblx0c2VydmVyOiB7XG5cdFx0aG9zdDogJzAuMC4wLjAnLCAvLyBBY2NlcHQgY29ubmVjdGlvbnMgZnJvbSBhbnkgbmV0d29yayBpbnRlcmZhY2Vcblx0XHRhbGxvd2VkSG9zdHM6IFsncHMnLCAnZnMnLCAnaG9tZSddLCAvLyBFeHBsaWNpdGx5IGFsbG93IHRoaXMgaG9zdFxuXHR9LFxuXHRyZXNvbHZlOiB7XG5cdFx0YWxpYXM6IHtcblx0XHRcdCdAJzogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJ3NyYycpLFxuXHRcdFx0J3RhaWx3aW5kLmNvbmZpZy5qcyc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICd0YWlsd2luZC5jb25maWcuanMnKSxcblx0XHRcdCdAbnV4dGFwcCc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICcuLi8uLi9tYXhsbXMvbnV4dGFwcCcpLFxuXHRcdH0sXG5cdH0sXG5cdG9wdGltaXplRGVwczoge1xuXHRcdGluY2x1ZGU6IFtcblx0XHRcdCdmZWF0aGVyLWljb25zJyxcblx0XHRcdCdzaG93ZG93bicsXG5cdFx0XHQnZW5naW5lLmlvLWNsaWVudCcsXG5cdFx0XHQndGFpbHdpbmQuY29uZmlnLmpzJyxcblx0XHRcdCdpbnRlcmFjdGpzJyxcblx0XHRcdCdoaWdobGlnaHQuanMnLFxuXHRcdFx0J3BseXInLFxuXHRcdF0sXG5cdH0sXG59KVxuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUFpVixTQUFTLG9CQUFvQjtBQUM5VyxPQUFPLFNBQVM7QUFDaEIsT0FBTyxVQUFVO0FBQ2pCLE9BQU8sY0FBYztBQUNyQixTQUFTLGVBQWU7QUFDeEIsT0FBTyxRQUFRO0FBTGYsSUFBTSxtQ0FBbUM7QUFRekMsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDM0IsU0FBUztBQUFBLElBQ1IsU0FBUztBQUFBLE1BQ1IsYUFBYTtBQUFBLE1BQ2IsYUFBYTtBQUFBLE1BQ2IsZUFBZTtBQUFBLE1BQ2YsYUFBYTtBQUFBLFFBQ1osT0FBTyxDQUFDO0FBQUEsTUFDVDtBQUFBLE1BQ0EsYUFBYTtBQUFBLFFBQ1osZUFBZTtBQUFBLE1BQ2hCO0FBQUEsSUFDRCxDQUFDO0FBQUEsSUFDRCxJQUFJO0FBQUEsTUFDSCxRQUFRO0FBQUEsUUFDUCxhQUFhO0FBQUEsUUFDYixrQkFBa0I7QUFBQSxNQUNuQjtBQUFBLElBQ0QsQ0FBQztBQUFBLElBQ0QsUUFBUTtBQUFBLE1BQ1AsY0FBYztBQUFBLE1BQ2QsWUFBWTtBQUFBLFFBQ1gsU0FBUztBQUFBLE1BQ1Y7QUFBQSxNQUNBLFNBQVM7QUFBQSxRQUNSLHVCQUF1QjtBQUFBLFFBQ3ZCLCtCQUErQixJQUFJLE9BQU87QUFBQSxNQUMzQztBQUFBLE1BQ0EsVUFBVTtBQUFBLFFBQ1QsU0FBUztBQUFBLFFBQ1QsTUFBTTtBQUFBLFFBQ04sWUFBWTtBQUFBLFFBQ1osV0FBVztBQUFBLFFBQ1gsYUFDQztBQUFBLFFBQ0QsYUFBYTtBQUFBLFFBQ2Isa0JBQWtCO0FBQUEsUUFDbEIsT0FBTztBQUFBLFVBQ047QUFBQSxZQUNDLEtBQUs7QUFBQSxZQUNMLE9BQU87QUFBQSxZQUNQLE1BQU07QUFBQSxZQUNOLFNBQVM7QUFBQSxVQUNWO0FBQUEsVUFDQTtBQUFBLFlBQ0MsS0FBSztBQUFBLFlBQ0wsT0FBTztBQUFBLFlBQ1AsTUFBTTtBQUFBLFlBQ04sU0FBUztBQUFBLFVBQ1Y7QUFBQSxRQUNEO0FBQUEsTUFDRDtBQUFBLElBQ0QsQ0FBQztBQUFBLElBQ0QsR0FBRyxDQUVILENBQUM7QUFBQSxFQUNGO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDUCxNQUFNO0FBQUE7QUFBQSxJQUNOLGNBQWMsQ0FBQyxNQUFNLE1BQU0sTUFBTTtBQUFBO0FBQUEsRUFDbEM7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNSLE9BQU87QUFBQSxNQUNOLEtBQUssS0FBSyxRQUFRLGtDQUFXLEtBQUs7QUFBQSxNQUNsQyxzQkFBc0IsS0FBSyxRQUFRLGtDQUFXLG9CQUFvQjtBQUFBLE1BQ2xFLFlBQVksS0FBSyxRQUFRLGtDQUFXLHNCQUFzQjtBQUFBLElBQzNEO0FBQUEsRUFDRDtBQUFBLEVBQ0EsY0FBYztBQUFBLElBQ2IsU0FBUztBQUFBLE1BQ1I7QUFBQSxNQUNBO0FBQUEsTUFDQTtBQUFBLE1BQ0E7QUFBQSxNQUNBO0FBQUEsTUFDQTtBQUFBLE1BQ0E7QUFBQSxJQUNEO0FBQUEsRUFDRDtBQUNELENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
