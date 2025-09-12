import React from 'react';

const Hero = () => {
    return (
        <section id="home" className="relative bg-cover bg-center h-[80vh] flex items-center justify-center text-center text-white" style={{ backgroundImage: "linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('/web.jpg')" }}>
            <div className="max-w-2xl px-4">
                <h1 className="text-4xl md:text-5xl font-bold mb-6">Drama, Films and Cultural events</h1>
                <p className="text-lg mb-8">Delivering impactful performances that blend entertainment with awareness for businesses, communities & organizations.</p>
                <a href="#contact" className="btn-primary">Get in Touch</a>
            </div>
        </section>
    );
};

export default Hero;
