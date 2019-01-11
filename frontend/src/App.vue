<template>
  <v-app>
    <v-snackbar
      v-model="snackbar"
      multi-line
      auto-height
      top
      :timeout="100000"
    >
    <pre>{{ errorText }}</pre>
    <v-btn
        color="pink"
        flat
        @click="snackbar = false"
      >
        Close
      </v-btn>
      
    </v-snackbar>
    <v-navigation-drawer
      persistent
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >
      <v-list>
        <v-list-tile v-for="a in attacks" :key="JSON.stringify(a)"
          :value="selectedAttack['__name__'] == a['__name__']" @click="selectedAttack = a; drawer = !drawer">
          <v-list-tile-action>
            <v-icon v-html="a.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{a.name}}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      app
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <h1><v-icon color="primary">mdi-play-network</v-icon> KNX-Player</h1>
    </v-toolbar>
    <v-content>
      <Attack v-for="a in this.attacks" :key="a.name" :status="runningAttacks[a['__name__']]" :attack="a" v-show="a.name == selectedAttack.name"/>

    </v-content>

 
  </v-app>
</template>

<script>
import Attack from './components/Attack'
import Vue from 'vue'

export default {
  name: 'App',
  components: {
    Attack
  },
  data () {
    return {
      drawer: true,
      selectedAttack: {},
      right: true,
      title: 'KNX-Player',
      attacks: [],
      runningAttacks: {},
      errorText: "",
      snackbar: false
    }
  },
  methods: {
  },
  mounted: function() {
    window.sio.on('attacks', a => {
      Vue.set(this, 'attacks', a);
      Vue.set(this, 'selectedAttack', a[0]);
      });
      window.sio.on('attack status', a => {
        console.log(a);
        this.runningAttacks[a["name"]] = a["status"];
      })
      window.sio.on('error', a => {
        this.snackbar = true;
        this.errorText = a;
      })
    window.sio.emit('get attacks');
  }
}
</script>

<style>
footer {
  height: 70px !important
}
.v-snack__content {
  font-size: 8px;
}

.v-snack__wrapper {
  max-width: 100vw !important;
}
</style>
