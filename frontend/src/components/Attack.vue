<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <h2>{{attack.name}}</h2>
        <br>
        <v-flex v-for="p in attack.parameters" :key="JSON.stringify(p)">
          <v-slider v-if="p['__name__'] == 'SliderType'"
            thumb-label="always"
            :min="p.min"
            :max="p.max"
            v-model="values[p.name]"
            :label='p.name.replace("_", " ")'>
          </v-slider>
          <v-text-field v-if="p['__name__'] == 'TextfieldType'"
            :label='p.name.replace("_", " ")'
            :placeholder="String(p.default)"
            v-model="values[p.name]"
          ></v-text-field>
          <div v-if="p['__name__'] == 'TimeSliderType'">
            <time-slider
              @value-change="values[p.name] = $event"
              :value="values[p.name]"
              :min="p.min"
              :max="p.max"
              :label='p.name.replace("_", " ")'>  
            </time-slider>
          </div>
          <div v-if="p['__name__'] =='LogPlayerType' || p['__name__'] == 'MultipleChoiceType'">
            <v-select
              v-model="values[p.name]"
              :items="p['choices']"
              attach
              chips
              :label='p.name.replace("_", " ")'
              multiple
          ></v-select>
          </div>
          <div v-if="p['__name__'] =='SingleChoiceType'">
            <v-select
              v-model="values[p.name]"
              :items="p['choices']"
              attach
              chips
              :label='p.name.replace("_", " ")'
          ></v-select>
          </div>
        </v-flex>
      </v-layout>
    </v-slide-y-transition>
      <v-footer class="pa-3">
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <h3 v-show="status > 0">Angriff läuft</h3>
        <v-spacer></v-spacer>
        <v-progress-linear v-model="status" style="width: 20vw" v-if="status > 0"></v-progress-linear>
        <v-spacer></v-spacer>
        <v-btn fab dark small :disabled="status == undefined" @click="stopAttack()">
          <v-icon dark>stop</v-icon>
        </v-btn>
        <v-btn fab dark small color="primary" :disabled="status != undefined" @click="startAttack()">
          <v-icon dark>mdi-play</v-icon>
        </v-btn>
    </v-footer>
  </v-container>
</template>

<script>
import Vue from 'vue'
import TimeSlider from './TimeSlider'

export default {
  name: 'Attack',
  components: {
    TimeSlider
  },
  props: {
    attack: Object,
    status: Number
  },
  data: function() {return {
    values: {}
  }},
  mounted: function() {
    for (let p of this.attack.parameters) {
      console.log(p);
      Vue.set(this.values, p.name, p.default);
    }
  },
  methods: {
    startAttack: function() {
      window.sio.emit('start attack', this.attack["__name__"],  this.values);
    },
    stopAttack: function() {
       window.sio.emit('stop attack', this.attack["__name__"]);
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.v-label {
    text-transform:capitalize;
}

.layout .flex {
  width: 70vw;
  padding: 4vh 0;
}
</style>
