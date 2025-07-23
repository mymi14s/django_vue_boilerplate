import axios from 'axios';
import alertify from 'alertifyjs';
import Utils from './Utils';

const validator = new Utils();

class Brigantes {
  constructor(baseURL = '') {
    baseURL = window.location.host.includes(':3000') ? 'http://'+window.location.host.replace('3000', '8000') : baseURL;
    this.api = axios.create({
      baseURL, 
      headers: {
        'Content-Type': 'application/json',
      },
      xsrfCookieName: 'csrftoken',
      xsrfHeaderName: 'X-CSRFTOKEN',
      withCredentials: true,
    });

    // Global response error interceptor
    this.api.interceptors.response.use(
        (response) => { 
        const statusCode = response.status;
        if (![200, 201, 202].includes(statusCode)) {
            const msg = response.data?.error || 'Unexpected response from server';
            alertify.error('Error', msg);
            return Promise.reject({ ...response, message: msg });
        }
        return response;
        },
        (error) => {
        const msg = error.response?.data?.detail || error.message || 'API request failed';
        return Promise.reject(error);
        }
    );

    // Request interceptor to inject Authorization header
    this.api.interceptors.request.use(
      (config) => {
        let token = sessionStorage.getItem('token');
        const excludedEndpoints = ['/user/login', '/get_csrf_token'];
        const requestUrl = config.url?.replace(baseURL, '') || '';

        // Only add token if request is not excluded and token exists
        if (token && !excludedEndpoints.some(endpoint => requestUrl.startsWith(endpoint))) {
          config.headers['Authorization'] = `Token ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
  }

  async getCSRFToken() {
    // 'X-CSRFToken'
    try {
        const response = await this.api.get('/get_csrf_token');
        this.api.defaults.headers['X-CSRFToken'] = response.data.token
        return response.data.token;
      
    } catch (err) {
      // error handled globally
      validator.error('Error', String(err));
      throw err;
    }
  }

  // Login with credentials; expects { username, password }
  async login(email, password) {
    
    try {
        let token = await this.getCSRFToken();
        if (token) {
            if (!email || !password ) {
                validator.error("Email and password are required!");
            } else if (!validator.isValidEmail(email)){
                validator.error("Email is invalid!");
            } else {
                const response = await this.api.post('/user/login', {
                    email: email, password: password
                });
                sessionStorage.setItem('user', JSON.stringify(response.data.user));
                sessionStorage.setItem('is_authenticated', response.data.token ? 1 : 0 );
                sessionStorage.setItem('token', response.data.token ? response.data.token : '' );
                this.api.defaults.headers['Authorization'] = `Token ${response.data.token}`;
                alertify.success('Logged in successfully');
                return response.data;
            }
        } else {
            this.login(email, password);
        }      
    } catch (err) {
      // error handled globally
      alertify.alert('Error', err.response.data.error);
      throw err;
    }
  }


    // Update socketio SID
  async set_sio_sid(sid) {
    
    try {
        let token = await this.getCSRFToken();
        if (token && sid) {
            const response = await this.api.post('/user/sio-sid', {
                sid: sid
            });
            if (response.data) {
              sessionStorage.setItem('sio_sid', sid);
            }
        } else {
            validator.error("Socket IO SID not found!");
        }
            
    } catch (err) {
      // error handled globally
      alertify.alert('Error', err.response.data.error);
      throw err;
    }
  }

  // Logout current session
  async logout() {
    try {
      sessionStorage.clear();
      await this.api.post('/user/logout');
      alertify.success('Logged out successfully');
      window.location.href = '/'; // Redirect to login page
    } catch (err) {
      throw err;
    }
  }

  // Fetch settings from Django endpoint
  async fetchSettings() {
    try {
      const response = await this.api.get('/api/settings/');
      return response.data;
    } catch (err) {
      throw err;
    }
  }
}

export default Brigantes;