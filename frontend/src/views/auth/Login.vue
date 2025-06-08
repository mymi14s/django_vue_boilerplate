<script>
import { useSessionStore } from '@/stores/session'

const session = useSessionStore()

export default {
  name: 'Login',

  // Component data
  data() {
    return {
      message: 'Hello Vue!',
      count: 0,
      email: "",
      password: "",
    };
  },

  // Props received from parent
  props: {
    title: {
      type: String,
      required: true,
    },
    isVisible: {
      type: Boolean,
      default: true,
    },
  },

  // Computed properties
  computed: {
    reversedMessage() {
      return this.message.split('').reverse().join('');
    },
  },

  // Methods (event handlers, business logic)
  methods: {
    async login() {
      let data = await this.$brigantes.login(this.email, this.password);
      sessionStorage.setItem('user', JSON.stringify(data.user));
      sessionStorage.setItem('is_authenticated', data.is_authenticated ? 1 : '' );
      if (data.is_authenticated){
        this.$router.push('/');
      }
    },

  },

  // Watchers for reactive changes
  watch: {
    count(newVal, oldVal) {
      console.log(`Count changed from ${oldVal} to ${newVal}`);
    },
  },

  // Lifecycle hooks
  beforeCreate() {
    console.log('beforeCreate');
  },
  created() {
    console.log('created');
  },
  beforeMount() {
    console.log('beforeMount');
  },
  beforeUpdate() {
    console.log('beforeUpdate');
  },
  updated() {
    console.log('updated');
  },
  beforeUnmount() {
    console.log('beforeUnmount');
  },
  unmounted() {
    console.log('unmounted');
  },

  // Components used inside this component
  components: {
    // ExampleChildComponent
  },

  // Custom directives used in this component
  directives: {
    // ExampleDirective
  },

  // Provide/inject (for dependency injection)
  provide() {
    return {
      someService: this.someService,
    };
  },
  inject: ['someService'],

  // Template render function (optional alternative to <template>)
  // render(h) {
  //   return h('div', this.message);
  // },

  // Mixins (shared functionality)
  mixins: [
    // someMixin
  ],

  // Emits (declare custom events)
  emits: ['update', 'submit'],

  // Template refs
  mounted() {
    this.$refs.myRef?.focus();
    this.$brigantes.getCSRFToken();
    const is_authenticated = sessionStorage.getItem('is_authenticated');
    if (is_authenticated && window.location.href.includes('/auth/login')){
      router.push('/')
    }
  },
};
</script>





<template>
  <div class="wrapper min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol :md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <div class="text-center">
                  <h1>Login</h1>
                  <p class="text-body-secondary">Sign In to your account</p>
                  </div>
                  <CInputGroup class="mb-3">
                    <CInputGroupText>
                      <CIcon icon="cil-user" />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Email"
                      autocomplete="email"
                      v-model="email"
                      type="email"
                      required
                    />
                  </CInputGroup>
                  <CInputGroup class="mb-4">
                    <CInputGroupText>
                      <CIcon icon="cil-lock-locked" />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      autocomplete="current-password"
                      v-model="password"
                    />
                  </CInputGroup>
                  <CRow>
                    <CCol :xs="6">
                      <CButton color="primary" class="px-4"  @click="login"> Login </CButton>
                    </CCol>
                    <CCol :xs="6" class="text-right">
                      <CButton color="link" class="px-0">
                        Forgot password?
                      </CButton>
                    </CCol>
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
