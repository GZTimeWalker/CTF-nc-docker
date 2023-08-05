import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig(({ mode }) => {
  return {
    base: "/wnc/",
    build: {
      outDir: 'build',
      target: ['es2020'],
      assetsDir: 'static',
      chunkSizeWarningLimit: 2000,
      rollupOptions: {
        output: {
          chunkFileNames: 'static/[hash].js',
          assetFileNames: 'static/[hash].[ext]',
          entryFileNames: 'static/[name].[hash].js',
          compact: true,
        },
      },
    },
    plugins: [
      react(),
    ],
  }
})
