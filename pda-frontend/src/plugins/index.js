/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
import router from '../router'
import VueSocketIO from 'vue-3-socket.io'

export function registerPlugins (app) {
	const socketioo = new VueSocketIO({
		debug: true,
		connection: 'http://127.0.0.1:8000'
	})
  loadFonts()
  app
    .use(vuetify)
    .use(router)
		.use(socketioo)
}
