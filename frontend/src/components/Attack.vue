<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <h2>{{attack.name}}</h2>
        <v-flex xs12 sm6 md3 v-for="p in attack.parameters" :key="JSON.stringify(p)">
          <v-slider v-if="p['__name__'] == 'SliderType'"
            thumb-label="always"
            :min="p.min"
            :max="p.max"
            v-model="p.default"
            :label='p.name.replace("_", " ")'>
          </v-slider>
          <v-text-field v-else
            :label='p.name.replace("_", " ")'
            placeholder="Placeholder"
          ></v-text-field>
        </v-flex>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
export default {
  name: 'Attack',
  props: {
    attack: Object
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.v-label {
    text-transform:capitalize;
}
</style>
