import { validateRegistrationForm } from "../src/app/utils/validation";

describe("validateRegistrationForm", () => {
  it("should return no errors for valid input", () => {
    const validData = {
      username: "testuser",
      email: "test@example.com",
      firstname: "Test",
      lastname: "User",
      password: "password123",
    };

    const errors = validateRegistrationForm(validData);
    expect(errors).toEqual({});
  });

  it("should return an error if username is missing", () => {
    const invalidData = {
      username: "",
      email: "test@example.com",
      firstname: "Test",
      lastname: "User",
      password: "password123",
    };

    const errors = validateRegistrationForm(invalidData);
    expect(errors.username).toBe("Username is required.");
  });

  it("should return an error for invalid email format", () => {
    const invalidData = {
      username: "testuser",
      email: "invalidemail",
      firstname: "Test",
      lastname: "User",
      password: "password123",
    };

    const errors = validateRegistrationForm(invalidData);
    expect(errors.email).toBe("Invalid email format.");
  });

  it("should return an error if password is too short", () => {
    const invalidData = {
      username: "testuser",
      email: "test@example.com",
      firstname: "Test",
      lastname: "User",
      password: "123",
    };

    const errors = validateRegistrationForm(invalidData);
    expect(errors.password).toBe("Password must be at least 6 characters.");
  });

  it("should return multiple errors for multiple invalid fields", () => {
    const invalidData = {
      username: "",
      email: "",
      firstname: "",
      lastname: "",
      password: "",
    };

    const errors = validateRegistrationForm(invalidData);
    expect(errors).toEqual({
      username: "Username is required.",
      email: "Email is required.",
      // firstname: "First Name is required.",
      // lastname: "Last Name is required.",
      password: "Password is required.",
    });
  });
});
