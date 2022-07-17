<template lang="html">
  <q-page class="row text-white items-stretch justify-center">
    <div class="row col-5 left justify-center">

        <div class="row col-12 text-weight-light text-h5 q-pt-md q-pl-md">
          <div>
            <q-btn class="row" flat to="/">
              <span><q-icon name="keyboard_backspace" /></span>
              <span class="q-pl-xs">Back to main page</span>
            </q-btn>
          </div>
        </div>

        <div class="col-6">
          <div class="col-7 text-h4 text-center text-weight-light q-pb-xl">
            Log in form
          </div>

          <form @submit.prevent.stop="onSubmit" @reset.prevent.stop="onReset" class="q-gutter-md q-pb-xl">

            <div class="row items-center">
              <div class="col-12 q-pl-md">Don't have an account?</div>
              <q-btn flat unelevated class="col-shrink text-blue" to="/signup">Sign up!</q-btn>
            </div>

            <q-input dark label-color="grey-5"
              ref="emailRef"
              filled
              label="Your email *"
              v-model="email"
              type="email"
              hint="Email"
              lazy-rules
              :rules="emailRules"
            >
              <template v-slot:before>
                <q-icon name="mail" />
              </template>
            </q-input>

            <q-input dark label-color="grey-5"
              ref="passwordRef"
              label="Your password *"
              v-model="password"
              filled
              :type="isPwd ? 'password' : 'text'"
              hint="Password (more than 6 characters)"
              lazy-rules
              :rules="[function() {
                if (password) { if (password.length > 6) {return true} else {return 'Password length should be more than 6 symbols'} } return 'Please, fill in the form'
              }]"
              >
              <template v-slot:before>
                <q-icon name="lock" />
              </template>
              <template v-slot:append>
                <q-icon v-if="password"
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>

            <div>
              <q-btn label="Submit" type="submit" color="primary" />
              <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
            </div>

          </form>
        </div>
    </div>

    <div class="col-7 right">
    </div>

    Firstname: {{ this.user.firstnameChecked }}
    <br>
    Lastname: {{ this.user.lastnameChecked }}
    <br>
    Email: {{ this.user.emailChecked }}
    <br>
    Password: {{ this.user.passwordChecked }}

  </q-page>
</template>

<script>

import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
  name: 'SignupPage',

  setup () {
    const $q = useQuasar()

    const email = ref(null)
    const emailRef = ref(null)

    const password = ref(null)
    const passwordRef = ref(null)

    const user = ref({
      firstnameChecked: '',
      lastnameChecked: '',
      emailChecked: '',
      passwordChecked: '',
    }) // contains the user information received after clicking 'submit' in the registration form

    return {
      email,
      emailRef,

      password,
      passwordRef,

      user,

      onSubmit () {
        emailRef.value.validate()
        passwordRef.value.validate()

        if (emailRef.value.hasError || passwordRef.value.hasError) {
          // form has error
        }
        else {
          this.user.emailChecked = this.email
          this.user.passwordChecked = this.password

          $q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Submitted'
          })
        }
      },

      onReset () {
        email.value = null
        password.value = null

        emailRef.value.resetValidation()
        passwordRef.value.resetValidation()
      }
    }
  },

  data: function() {
    return {
      isPwd: true,

      emailRules: [
        () => {
          if (this.email) {
            const reg = /^[^@]+@[^@]+$/
            if (reg.test(this.email)) {
              return true
            }
          } return 'Please, type the valid email'
        }
      ],
    }
  },
}
</script>

<style>

  .right {
    background: no-repeat url(~assets/locomotive.svg);
    background-size: 100%;
    background-position: center;
    background-size: cover;
  }

  [role=alert] {
    color: rgb(29, 156, 173)
  }

</style>
