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
            @focus="show"
            data-layout="normal"
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
      <vue-touch-keyboard :options="options" v-if="visible" :layout="layout" :cancel="hide" :accept="accept" :input="input" :next="next" />
      <v-footer class="pa-3">
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <h3 v-show="status > 0">Angriff läuft</h3>
        <v-spacer></v-spacer>
        <v-progress-linear v-bind:value="status" style="width: 20vw" v-if="status > 0"></v-progress-linear>
        <v-spacer></v-spacer>
        <v-btn fab dark small :disabled="status == undefined || status < 0" @click="stopAttack()">
          <v-icon dark>stop</v-icon>
        </v-btn>
        <v-btn fab dark small color="primary" :disabled="status > 0" @click="startAttack()">
          <v-icon dark>mdi-play</v-icon>
        </v-btn>
    </v-footer>
  </v-container>
</template>

<script>
import Vue from 'vue'
import TimeSlider from './TimeSlider'
import VueTouchKeyboard from "vue-touch-keyboard";
import style from "vue-touch-keyboard/dist/vue-touch-keyboard.css"; // load default style

Vue.use(VueTouchKeyboard);

export default {
  name: 'Attack',
  components: {
    TimeSlider
  },
  props: {
    attack: Object,
    status: -1
  },
  data: function() {return {
      values: {},
      visible: false,
      layout: "normal",
      input: null,
      options: {
        useKbEvents: true,
        preventClickEvent: true
      }
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
    accept(text) {
       this.hide();
       let input = this.input;
       setTimeout(function(){input.value = text;}, 200);
    },
    show(e) {
       this.input = e.target;
       this.layout = e.target.dataset.layout;

       if (!this.visible)
          this.visible = true
    },
    hide() {
       this.visible = false;
    },
    next() {
       let inputs = document.querySelectorAll("input");
       let found = false;
       [].forEach.call(inputs, (item, i) => {
          if (!found && item == this.input && i < inputs.length - 1) {
             found = true;
             this.$nextTick(() => {
                inputs[i+1].focus();
             });
          }
       });
       if (!found) {
          this.input.blur();
          this.hide();
       }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.v-label {
    text-transform:capitalize;
}
.keyboard {
   position: fixed;
   bottom: 0;
   width: 50%;
   z-index: 9;
}
.layout .flex {
  width: 70vw;
  padding: 4vh 0;
}
</style>
