import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'


import App from './App.vue'
import router from './router'

import CoreuiVue from '@coreui/vue'
import CIcon from '@coreui/icons-vue'
import { iconsSet as icons } from '@/assets/icons'
import DocsComponents from '@/components/DocsComponents'
import DocsExample from '@/components/DocsExample'
import DocsIcons from '@/components/DocsIcons'


// import 'alertifyjs/build/css/alertify.min.css';
// import 'alertifyjs/build/alertify.min.js';
import axios from 'axios';
import alertify from 'alertifyjs';


import Brigantes from './utils/Brigantes';
import Utils from './utils/Utils';

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)


const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(CoreuiVue)
app.provide('icons', icons)
app.component('CIcon', CIcon)
app.component('DocsComponents', DocsComponents)
app.component('DocsExample', DocsExample)
app.component('DocsIcons', DocsIcons)

app.config.globalProperties.$brigantes = new Brigantes('/'); // global api call to django
app.config.globalProperties.$validator = new Utils();

app.mount('#app')
