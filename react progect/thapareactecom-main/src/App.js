import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import { GlobalStyle } from "./GlobalStyle";
import styled from "styled-components";
import { FaShoppingCart, FaUser, FaHome, FaPhone, FaStore, FaBars, FaTimes } from "react-icons/fa";

// Import components
import Home from "./Home";
import Products from "./Products";
import Cart from "./Cart";
import Contact from "./Contact";
import SingleProduct from "./SingleProduct";

// Theme configuration
const theme = {
  colors: {
    heading: "rgb(24 24 29)",
    text: "rgba(29, 29, 29, .8)",
    white: "#fff",
    black: "#212529",
    helper: "#8490ff",
    bg: "#F6F8FA",
    footer_bg: "#0a1435",
    btn: "rgb(98 84 243)",
    border: "rgba(98, 84, 243, 0.5)",
    hr: "#ffffff",
    gradient: "linear-gradient(0deg, rgb(132 144 255) 0%, rgb(98 189 252) 100%)",
    shadow: "rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px",
    shadowSupport: "rgba(0, 0, 0, 0.16) 0px 1px 4px",
  },
  media: {
    mobile: "768px",
    tab: "998px",
  },
};

// Styled components
const Header = styled.header`
  padding: 0 4.8rem;
  height: 10rem;
  background-color: ${({ theme }) => theme.colors.bg};
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: ${({ theme }) => theme.colors.shadow};

  .logo {
    font-size: 3rem;
    font-weight: bold;
    color: ${({ theme }) => theme.colors.heading};
  }

  @media screen and (max-width: ${({ theme }) => theme.media.mobile}) {
    padding: 0 2.4rem;
    height: 8rem;

    .logo {
      font-size: 2.5rem;
    }
  }
`;

const Nav = styled.nav`
  display: flex;
  align-items: center;
  gap: 3rem;
`;

const NavMenu = styled.div`
  display: flex;
  gap: 3rem;

  @media screen and (max-width: ${({ theme }) => theme.media.mobile}) {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 90vh;
    position: absolute;
    top: 10rem;
    left: ${({ isOpen }) => (isOpen ? '0' : '-100%')};
    opacity: 1;
    transition: all 0.5s ease;
    background-color: ${({ theme }) => theme.colors.bg};
    padding: 2rem;
    box-shadow: ${({ theme }) => theme.colors.shadow};
  }
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: ${({ theme }) => theme.colors.text};
  font-size: 1.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s ease;

  &:hover {
    color: ${({ theme }) => theme.colors.btn};
  }

  @media screen and (max-width: ${({ theme }) => theme.media.mobile}) {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
`;

const MobileIcon = styled.div`
  display: none;

  @media screen and (max-width: ${({ theme }) => theme.media.mobile}) {
    display: block;
    font-size: 2.5rem;
    cursor: pointer;
    color: ${({ theme }) => theme.colors.text};
  }
`;

const Main = styled.main`
  min-height: calc(100vh - 10rem);
`;

const Footer = styled.footer`
  background-color: ${({ theme }) => theme.colors.footer_bg};
  color: ${({ theme }) => theme.colors.white};
  padding: 3rem 0;
  text-align: center;
  
  p {
    font-size: 1.6rem;
    margin: 0;
  }
`;

const App = () => {
  const [cartItems, setCartItems] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  const addToCart = (product) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === product.id);
      if (existingItem) {
        return prevItems.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prevItems, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCartItems(prevItems => prevItems.filter(item => item.id !== productId));
  };

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity === 0) {
      removeFromCart(productId);
      return;
    }
    setCartItems(prevItems =>
      prevItems.map(item =>
        item.id === productId ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <GlobalStyle />
        <Header>
          <div className="logo">Thapa E-Commerce</div>
          <Nav>
            <MobileIcon onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? <FaTimes /> : <FaBars />}
            </MobileIcon>
            <NavMenu isOpen={isOpen}>
              <StyledLink to="/" onClick={() => setIsOpen(false)}><FaHome /> Home</StyledLink>
              <StyledLink to="/products" onClick={() => setIsOpen(false)}><FaStore /> Products</StyledLink>
              <StyledLink to="/cart" onClick={() => setIsOpen(false)}>
                <FaShoppingCart /> Cart ({cartItems.reduce((total, item) => total + item.quantity, 0)})
              </StyledLink>
              <StyledLink to="/contact" onClick={() => setIsOpen(false)}><FaPhone /> Contact</StyledLink>
            </NavMenu>
          </Nav>
        </Header>
        
        <Main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route 
              path="/products" 
              element={<Products addToCart={addToCart} />} 
            />
            <Route 
              path="/cart" 
              element={
                <Cart 
                  cartItems={cartItems} 
                  removeFromCart={removeFromCart}
                  updateQuantity={updateQuantity}
                />
              } 
            />
            <Route path="/contact" element={<Contact />} />
            <Route 
              path="/product/:id" 
              element={<SingleProduct addToCart={addToCart} />} 
            />
          </Routes>
        </Main>
        
        <Footer>
          <p>&copy; 2024 Thapa E-Commerce. All rights reserved.</p>
        </Footer>
      </Router>
    </ThemeProvider>
  );
};

export default App;
