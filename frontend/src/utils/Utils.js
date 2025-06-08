import alertify from 'alertifyjs';

class Validator {
  constructor() {}

  isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }

  error(text) {
    alertify.alert('Error', text).set('modal', true)
  }
}


export default Validator;