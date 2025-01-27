// src/utils/validation.js
 
export const validateRegistrationForm = (formData) => {
    const errors = {};

    if (!formData.username) errors.username = "Username is required.";
    if (!formData.email) {
        errors.email = "Email is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        errors.email = "Invalid email format.";
    }
    // if (!formData.firstname) errors.firstname = "First Name is required.";
    // if (!formData.lastname) errors.lastname = "Last Name is required.";
    if (!formData.password) {
        errors.password = "Password is required.";
    } else if (formData.password.length < 6) {
        errors.password = "Password must be at least 6 characters.";
    }

    return errors;
  };

