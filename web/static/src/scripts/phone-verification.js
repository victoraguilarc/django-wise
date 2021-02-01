const PHONE_VERIFICATION = '/me/phone-verification/';

const PhoneVerification = {
  data() {
    return {
      hasCompleted: false,
      phoneNumber:  null,
      pendingAction: null,
      verificationCode: null,
      errors: {
        phoneNumber: null,
        verificationCode: null,
      }
    }
  },
  mounted() {
    this.$refs.form.classList.remove('hidden');
  },
  methods: {
    requestPhoneNumberVerification(event) {
      event.preventDefault();
      // this.pendingAction = '12';
      const self = this;
      const payload = { phoneNumber: this.phoneNumber };
      apiClient.post(PHONE_VERIFICATION, payload)
      .then(function (response) {
        self.pendingAction = response.data.pendingAction;
      })
      .catch(function (error) {
        self.errors = error.response.data;
      });
    },
    resetPhoneVerification() {
      this.pendingAction = null;
      this.verificationCode = null;
      this.phoneNumber = null;
    },
    completePhoneNumberVerification(event) {
      event.preventDefault();
      const self = this;
      const payload = {
        pendingAction: this.pendingAction,
        verificationCode: this.verificationCode,
      };
      apiClient.put(PHONE_VERIFICATION, payload)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        self.errors = error.response.data;
      });
    }
  }
}
Vue.createApp(PhoneVerification).mount('#phone-verification')
