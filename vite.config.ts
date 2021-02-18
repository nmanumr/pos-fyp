import {defineConfig} from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [reactRefresh()],
    server: {
        proxy: {
            '^/api': {
                target: 'http://pos_primary:8000',
                changeOrigin: false,
            },
            '^/admin': {
                target: 'http://pos_primary:8000',
                changeOrigin: false,
            },
            '^/static': {
                target: 'http://pos_primary:8000',
                changeOrigin: false,
            },
        },
    }
})
