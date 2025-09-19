import React, { useState } from "react";
import styled from "styled-components";
import { Container } from "./styles/Container";
import { Button } from "./styles/Button";

const Contact = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    console.log("Form submitted:", formData);
    alert("Thank you for your message! We'll get back to you soon.");
    setFormData({ name: "", email: "", message: "" });
  };

  return (
    <Wrapper>
      <Container>
        <h2 className="common-heading">Contact Us</h2>
        <div className="container">
          <div className="contact-form">
            <form onSubmit={handleSubmit} className="contact-inputs">
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={formData.name}
                onChange={handleChange}
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Your Email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <textarea
                name="message"
                placeholder="Your Message"
                rows="5"
                value={formData.message}
                onChange={handleChange}
                required
              ></textarea>
              <input type="submit" value="Send Message" />
            </form>
          </div>
        </div>
      </Container>
    </Wrapper>
  );
};

const Wrapper = styled.section`
  padding: 9rem 0 5rem 0;
  text-align: center;

  .container {
    margin-top: 6rem;

    .contact-form {
      max-width: 50rem;
      margin: auto;

      .contact-inputs {
        display: flex;
        flex-direction: column;
        gap: 3rem;

        input, textarea {
          width: 100%;
          padding: 1.6rem 2.4rem;
          border: 1px solid ${({ theme }) => theme.colors.border};
          border-radius: 0.5rem;
          font-size: 1.6rem;
        }

        input[type="submit"] {
          cursor: pointer;
          transition: all 0.2s;
          background-color: ${({ theme }) => theme.colors.btn};
          color: ${({ theme }) => theme.colors.white};
          border: none;
          padding: 1.4rem 2.2rem;
          font-size: 1.8rem;

          &:hover {
            background-color: ${({ theme }) => theme.colors.white};
            border: 1px solid ${({ theme }) => theme.colors.btn};
            color: ${({ theme }) => theme.colors.btn};
            transform: scale(0.9);
          }
        }
      }
    }
  }
`;

export default Contact;
