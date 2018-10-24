<template>
  <v-app>
    <v-navigation-drawer
      persistent
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >
      <v-list>
        <v-list-tile v-for="a in attacks" :key="JSON.stringify(a)"
          :value="selectedAttack['__name__'] == a['__name__']" @click="selectedAttack = a">
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
      <Attack v-for="a in this.attacks" :key="a.name" :attack="a" v-show="a.name == selectedAttack.name"/>

    </v-content>

    <v-footer class="pa-3">
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <h3 v-show="runningAttack != false">Aktueller Angriff: {{ runningAttack.name }}</h3>
      <v-spacer></v-spacer>
      <v-progress-linear v-model="runningAttack.progress" style="width: 20vw" v-show="runningAttack != false"></v-progress-linear>
      <v-spacer></v-spacer>
      <v-btn fab dark small :disabled="runningAttack == false" @click="stopAttack()">
        <v-icon dark>stop</v-icon>
      </v-btn>
      <v-btn fab dark small color="primary" :disabled="runningAttack != false" @click="startAttack()">
        <v-icon dark>mdi-play</v-icon>
      </v-btn>
    </v-footer>
  
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
      runningAttack: false
    }
  },
  methods: {
    stopAttack: function() {
      this.runningAttack = false;
    },
    startAttack: function() {

    }
  },
  mounted: function() {
    window.sio.on('attacks', a => {
      Vue.set(this, 'attacks', a);
      Vue.set(this, 'selectedAttack', a[0]);
      });
    window.sio.emit('get attacks');
  }
}
</script>

<style>
footer {
  height: 70px !important
}
</style>