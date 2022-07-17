<template>
  <q-page class="column text-white">
    <div class="col-grow row content-center q-mb-xl">

      <div class="col-12 row justify-center items-end text-center text-h4 text-weight-light">
        <div>Choose your destination: </div>
      </div>

      <div class="col-12 row justify-center items-begin q-mt-xl q-mb-xl">

        <q-input class="col-2 q-pr-sm" dark label-color="grey-5" filled v-model="departurePlace" label="Departure" />
        <q-input class="col-2 q-pr-sm" dark label-color="grey-5" filled v-model="arrivalPlace" label="Arrival" />

        <q-input class="col-2 text-white" dark placeholder="Date" filled v-model="dateRangeFormat2" :mask="YYYY-MM-DD-YYYY-MM-DD">
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                <q-date v-model="dateRangeFormat1" range mask="D MMM YYYY" :options="date => date >= this.formattedTimestamp">
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="primary" flat />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

      </div>
    </div>

    <div v-for="results in result" :key="result.id"  class="queryResult">

    </div>

  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import {date} from 'quasar'

export default {

  name: 'IndexPage',

  data: function() {
    return {

      timestamp: Date.now(),
      formattedTimestamp: '',

      dateRangeFormat1: null, // basic format of date
      dateRangeFormat2: null, // user-friendly format of date
      departureDate: null,
      arrivalDate: null,

      departurePlace: null,
      arrivalPlace: null,

      results: [],
    }
  },

  watch: {
    dateRangeFormat1: {
      immediate: true,
      handler() {

        this.formattedTimestamp = date.formatDate(this.timestamp, 'YYYY/MM/DD')

        if (this.dateRangeFormat1) {
        // check if user has chosen some date

          this.departureDate = this.dateRangeFormat1.from
          this.arrivalDate = this.dateRangeFormat1.to
          this.dateRangeFormat2 = `${this.departureDate} — ${this.arrivalDate}`

          console.log("Departure: " + this.dateRangeFormat1.from)
          console.log("Arrival: " + this.dateRangeFormat1.to)
          console.log("Another formatting: " + this.dateRangeFormat2)

        }
        else {
          this.departureDate = null
          this.arrivalDate = null
          this.dateRangeFormat2 = null
        }
      }
    }
  }
}
</script>

<style lang="sass">

</style>
