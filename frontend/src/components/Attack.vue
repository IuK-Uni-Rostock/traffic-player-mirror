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
            placeholder="p.default"
            v-model="values[p.name]"
          ></v-text-field>
          <div v-if="p['__name__'] == 'TimeSliderType'">
          <v-slider
            :min="p.min"
            :max="p.max"
            v-model="values[p.name]"
            append-icon="mdi-calendar-clock"
            :label='p.name.replace("_", " ")'>
          </v-slider>
          <div class="time-hint">{{ toReadableTime(values[p.name]) }}</div>
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
  </v-container>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'Attack',
  props: {
    attack: Object
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
    toReadableTime: function(temp) {
      function numberEnding (number) {
          return (number > 1) ? 's' : '';
      }

      let out = ""
      let del = "";

      var years = Math.floor(temp / 31536000);
      if (years) {
          out += del + years + ' year' + numberEnding(years);
          del = ", ";
      }
      //TODO: Months! Maybe weeks? 
      var days = Math.floor((temp %= 31536000) / 86400);
      if (days) {
          out += del + days + ' day' + numberEnding(days);
          del = ", ";
      }
      var hours = Math.floor((temp %= 86400) / 3600);
      if (hours) {
          out += del + hours + ' hour' + numberEnding(hours);
          del = ", ";
      }
      var minutes = Math.floor((temp %= 3600) / 60);
      if (minutes) {
          out += del + minutes + ' minute' + numberEnding(minutes);
          del = ", ";
      }
      var seconds = temp % 60;
      if (seconds) {
          out += del + seconds + ' second' + numberEnding(seconds);
      }

      return out;
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.v-label {
    text-transform:capitalize;
}
.time-hint {
  text-align: center;
  color: rgba(0,0,0,.54);
}

.layout .flex {
  width: 70vh;
  padding: 4vh 0;
}
</style>
