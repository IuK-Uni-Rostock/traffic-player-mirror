import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import de from 'vuetify/es5/locale/de'

Vue.use(Vuetify, {
  theme: {
    primary: '#1d3dba',
    secondary: '#ffdd0a',
    accent: '#dd6f00',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107'
  },
  iconfont: 'mdi',
  lang: {
    locales: { de },
    current: 'de'
  },
})
