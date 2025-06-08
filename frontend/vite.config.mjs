import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'node:path'
import autoprefixer from 'autoprefixer'


export default defineConfig(() => {
    return {
    plugins: [vue()],
    base: './',
    css: {
      postcss: {
        plugins: [
          autoprefixer({}), // add options if needed
        ],
      },
    },
    resolve: {
      alias: [
        // webpack path resolve to vitejs
        {
          find: /^~(.*)$/,
          replacement: '$1',
        },
        {
          find: '@/',
          replacement: `${path.resolve(__dirname, 'src')}/`,
        },
        {
          find: '@',
          replacement: path.resolve(__dirname, '/src'),
        },
      ],
      extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue', '.scss'],
    },
    build: {
      outDir: "../brigantes/static",
      emptyOutDir: true,
      target: "es2015",
      sourcemap: true,
      commonjsOptions: {
        include: [/node_modules/],
      },
      rollupOptions: {
        output: {
          // Remove hashes from filenames
          entryFileNames: 'assets/[name].js',
          chunkFileNames: 'assets/[name].js',
          assetFileNames: 'assets/[name].[ext]',
          manualChunks: {
            // You can define custom chunk splitting here if needed
          },
        },
      },
    },
    server: {
      port: 3000,
      proxy: getProxyOptions()
    },
  }
})


function getProxyOptions() {
	const webserver_port = 8000
	
	return {
		"^/(app|login|api|assets|files|private)": {
			target: `http://127.0.0.1:${webserver_port}`,
			ws: true,
      rewrite: (path) => path.replace(/^\//, ''),
			// router: function (req) {
			// 	const site_name = req.headers.host.split(":")[0]
			// 	console.log(`Proxying ${req.url} to ${site_name}:${webserver_port}`)
			// 	return `http://${site_name}:${webserver_port}`
			// },
		},
	}
}
