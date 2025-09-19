import React from "react";
import styled from "styled-components";
import { Container } from "./styles/Container";
import { Button } from "./styles/Button";

const Products = ({ addToCart }) => {
  // Sample product data
  const products = [
    {
      id: 1,
      name: "Premium Headphones",
      price: 199.99,
      description: "High-quality wireless headphones",
      image: "/images/hero.jpg"
    },
    {
      id: 2,
      name: "Smart Watch",
      price: 299.99,
      description: "Feature-rich smartwatch",
      image: "/images/hero.jpg"
    },
    {
      id: 3,
      name: "Wireless Earbuds",
      price: 99.99,
      description: "Compact wireless earbuds",
      image: "/images/hero.jpg"
    },
    {
      id: 4,
      name: "Gaming Mouse",
      price: 79.99,
      description: "High-performance gaming mouse",
      image: "/images/hero.jpg"
    }
  ];

  return (
    <Wrapper>
      <Container>
        <h2 className="common-heading">Our Products</h2>
        <div className="grid grid-three-column">
          {products.map((product) => (
            <div key={product.id} className="card">
              <div className="card-img">
                <img src={product.image} alt={product.name} />
              </div>
              <div className="card-data">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <p className="price">${product.price}</p>
                <Button 
                  className="btn" 
                  onClick={() => addToCart(product)}
                >
                  Add to Cart
                </Button>
              </div>
            </div>
          ))}
        </div>
      </Container>
    </Wrapper>
  );
};

const Wrapper = styled.section`
  padding: 9rem 0;

  .grid-three-column {
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
  }

  .card {
    background: #fff;
    border-radius: 1rem;
    box-shadow: ${({ theme }) => theme.colors.shadow};
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }
  }

  .card-img {
    height: 20rem;
    overflow: hidden;
    border-radius: 1rem 1rem 0 0;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .card-data {
    padding: 2rem;

    h3 {
      font-size: 2rem;
      margin-bottom: 1rem;
    }

    p {
      font-size: 1.6rem;
      margin-bottom: 1rem;
    }

    .price {
      font-weight: bold;
      color: ${({ theme }) => theme.colors.btn};
      font-size: 2rem;
    }
  }

  @media (max-width: ${({ theme }) => theme.media.mobile}) {
    .grid-three-column {
      grid-template-columns: 1fr;
    }
  }
`;

export default Products;
