import React, { useState } from 'react';

const Header = () => {
    const [menuOpen, setMenuOpen] = useState(false);

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);
    };

    return (
        <header className="bg-gray-100 shadow-md sticky top-0 z-50">
            <div className="container mx-auto px-6 flex justify-between items-center py-4">
                <div className="flex items-center space-x-3">
                    <img src="/logo.png" alt="Logo" className="h-12 w-auto" />
                    <span className="font-bold text-xl text-gray-800">Tejashree Production</span>
                </div>
                <nav className={`md:flex space-x-8 font-medium ${menuOpen ? 'block' : 'hidden'} absolute md:static bg-gray-100 md:bg-transparent top-full left-0 w-full md:w-auto shadow-md md:shadow-none`}>
                    <a href="#home" className="nav-link block md:inline-block px-4 py-2 md:p-0" onClick={() => setMenuOpen(false)}>Home</a>
                    <a href="#about" className="nav-link block md:inline-block px-4 py-2 md:p-0" onClick={() => setMenuOpen(false)}>About</a>
                    <a href="#services" className="nav-link block md:inline-block px-4 py-2 md:p-0" onClick={() => setMenuOpen(false)}>Services</a>
                    <a href="#gallery" className="nav-link block md:inline-block px-4 py-2 md:p-0" onClick={() => setMenuOpen(false)}>Gallery</a>
                    <a href="#video" className="nav-link block md:inline-block px-4 py-2 md:p-0" onClick={() => setMenuOpen(false)}>Video</a>
                    <a href="#contact" className="nav-link block md:inline-block px-4 py-2 md:p-0" onClick={() => setMenuOpen(false)}>Contact</a>
                </nav>
                <a href="#contact" className="btn-primary hidden md:block">Request Proposal</a>
                <button className="md:hidden" onClick={toggleMenu} aria-label="Toggle menu">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 text-gray-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={menuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
                    </svg>
                </button>
            </div>
        </header>
    );
};

export default Header;
