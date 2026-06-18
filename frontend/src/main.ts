/**
 * Vue application bootstrap.
 *
 * Author: HAMAILI Ahmed-Imad
 */

import 'bootstrap/dist/css/bootstrap.min.css'
import './styles.css'

import { createApp } from 'vue'
import App from './App.vue'

// The dashboard is a single-page application mounted on the root element from
// `index.html`.
createApp(App).mount('#app')
