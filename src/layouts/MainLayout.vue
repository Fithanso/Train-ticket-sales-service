<template>
  <q-layout view="lHh Lpr lFf">

    <q-header elevated>
      <div class="col-2 row justify-start items-center text-h3 text-weight-light text-white bg-dark text-center">
        <q-btn class="col-grow row justify-start items-center q-pl-xl text-h3 text-weight-light" flat no-caps to="/">
          <span><q-icon size="2em" name="train"/></span>
          <span> Train Itinerary App</span>
        </q-btn>

        <q-btn @click="test" flat>
          <q-icon left size="3em" name="language" />
          <div>Language</div>
        </q-btn>

        <q-btn to="/signup" flat>
          <q-icon left size="3em" name="login" />
          <div>Sign up</div>
        </q-btn>

        <q-btn class="q-mr-md" flat>
          <q-icon left size="3em" name="help" />
          <div>Help</div>
        </q-btn>
      </div>
    </q-header>

    <q-page-container>
        <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default {
  name: 'MainLayout',
  data: function () {
    return {

    }
  }
}
</script>

<style lang="sass">

  .q-page
    // background: linear-gradient(to bottom, #360033, #0b8793)
    // background: linear-gradient(to top, #654ea3, #eaafc8)
    // background: linear-gradient(to top, #8a2387, #e94057, #f27121)
    // background: linear-gradient(to top, #ad5389, #3c1053)
    // background: linear-gradient(to top, #c94b4b, #4b134f)
    background: linear-gradient(to top, #0f0c29, #302b63, #24243e)

</style>
