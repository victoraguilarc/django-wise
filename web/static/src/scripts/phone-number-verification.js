const PhoneNumberVerification = {
  data() {
    return {
      confirmationCode: null,
    }
  },
  mounted() {
    console.log('Mounted!');
  },
  methods: {
    requestValidation() {

    },
    sendConfirmationCode() {

    }
  }
}
Vue.createApp(PhoneNumberVerification).mount('#phone-number-verification')
