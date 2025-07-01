import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
// https://vite.dev/config/
export default defineConfig({
	plugins: [tailwindcss(), react()],
	server: {host: '10.147.17.201', port: 3000}
})
