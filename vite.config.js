import { defineConfig } from 'vite';
import path from 'path';

// Vite config to ensure compatibility with Firefox module loading
export default defineConfig({
  server: {
    fs: {
      strict: false,
    },
  },
  optimizeDeps: {
    include: ['lucide-react'],
  },
  resolve: {
    alias: {
      // Use absolute path for lucide-react to avoid duplication
      'lucide-react': path.resolve(__dirname, 'node_modules/lucide-react/dist/esm/lucide-react.js'),
    },
  },
});
