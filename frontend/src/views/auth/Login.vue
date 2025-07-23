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
      if (data.token) {
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
        <CCol :md="6" :lg="4">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm class="form-horizontal" @submit.prevent="login">
                  <div class="text-center mb-4">
                    <h2>Login</h2>
                    <p class="text-body-secondary small mb-0">Sign In to your account</p>
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
                      size="sm"
                      @keydown.enter="login"
                    />
                  </CInputGroup>
                  <CInputGroup class="mb-3">
                    <CInputGroupText>
                      <CIcon icon="cil-lock-locked" />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      autocomplete="current-password"
                      v-model="password"
                      size="sm"
                      @keydown.enter="login"
                    />
                  </CInputGroup>
                  <CRow class="align-items-center">
                    <CCol :xs="6">
                      <CButton color="primary" class="px-3 py-2" size="sm" @click="login"> 
                        Login 
                      </CButton>
                    </CCol>
                    <CCol :xs="6" class="text-right">
                      <CButton color="link" class="px-0 py-0" size="sm">
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