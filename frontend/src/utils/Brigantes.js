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
        const statusCode = response.data?.status_code;
        if (![200, 201, 202].includes(statusCode)) {
            const msg = response.data?.error || 'Unexpected response from server';
            alertify.error('Error', msg);
            return Promise.reject({ ...response, message: msg });
        }
        return response;
        },
        (error) => {
        const msg = error.response?.data?.detail || error.message || 'API request failed';
        alertify.error('Error', msg);
        return Promise.reject(error);
        }
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
                alertify.success('Logged in successfully');
                return response.data.data;
            }
        } else {
            this.login(email, password);
        }      
    } catch (err) {
      // error handled globally
      console.log(err.data.error)
      alertify.alert('Error', err.data.error);
      throw err;
    }
  }

  // Logout current session
  async logout() {
    try {
      await this.api.post('/logout/');
      alertify.success('Logged out successfully');
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
