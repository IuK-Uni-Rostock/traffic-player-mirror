<template>
    <div>
        <v-slider
        :min="min"
        :max="max"
        v-model="value"
        append-icon="mdi-calendar-clock"
        :label='label'>
        </v-slider>
        <div class="time-hint">
            <input type="number" v-model="days"> days
            <input type="number" v-model="hours"> hours
            <input type="number" v-model="minutes"> minutes
            <input type="number" v-model="seconds"> seconds
        </div>
    </div>
</template>

<script>
export default {
  name: 'TimeSlider',
  props: {
    value: Number,
    label: String,
    min: Number,
    max: Number,
  },
  data: function() {
    return {
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0
    }
  },
  mounted: function() {
        let s = this.splitTime(this.value);
        this.days = s[0];
        this.hours = s[1];
        this.minutes = s[2];
        this.seconds = s[3];
  },
  watch: {
      value: function(val, oldvalue) {
          let s = this.splitTime(val);
          this.days = s[0];
          this.hours = s[1];
          this.minutes = s[2];
          this.seconds = s[3];
      },
      days: function(val) {
          this.$emit('value-change', this.unsplitTime());
      },
      hours: function(val) {
          this.$emit('value-change', this.unsplitTime());
      },
      minutes: function(val) {
          this.$emit('value-change', this.unsplitTime());
      },
      seconds: function(val) {
          this.$emit('value-change', this.unsplitTime());
      }
  },
  methods: {
    splitTime: function(temp) {
      let out = ""
      let del = "";

      var days = Math.floor((temp %= 31536000) / 86400);

      var hours = Math.floor((temp %= 86400) / 3600);

      var minutes = Math.floor((temp %= 3600) / 60);

      var seconds = temp % 60;


      return [days, hours, minutes, seconds];
      },
    unsplitTime: function() {
        return Math.round(this.seconds) + 60 * Math.round(this.minutes) + 60*60 * Math.round(this.hours) + 60*60*24 * this.days;
    }
  }
}
</script>

<style scoped>
.time-hint {
  text-align: center;
  color: rgba(0,0,0,.54);
}

.time-hint input {
  width: 50px;
  border: 1px solid grey;
  margin-left: 20px;
  padding: 3px 0;
}
</style>