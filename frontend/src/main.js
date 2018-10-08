import '@babel/polyfill'
import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'

Vue.config.productionTip = false

import io from 'socket.io-client';

window.sio = io("http://127.0.0.1:8080/");

new Vue({
  render: h => h(App)
}).$mount('#app')
