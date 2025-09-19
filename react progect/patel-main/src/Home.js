import React from "react";
import styled from "styled-components";
import { Container } from "./styles/Container";

const Home = () => {
  return (
    <Wrapper>
      <Container>
        <h1>Welcome to Thapa E-Commerce</h1>
        <p>Your one-stop shop for all your needs!</p>
        <p>Explore our wide range of products and enjoy great deals.</p>
      </Container>
    </Wrapper>
  );
};

const Wrapper = styled.section`
  padding: 9rem 0;
  text-align: center;

  h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  p {
    font-size: 1.5rem;
    color: ${({ theme }) => theme.colors.text};
  }
`;

export default Home;
