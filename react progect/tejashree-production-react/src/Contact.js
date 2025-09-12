import React, { useState } from 'react';

const Contact = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // For now, just log the data. In a real app, you'd send it to a server.
        console.log('Form submitted:', formData);
        alert('Thank you for your message! We will get back to you soon.');
        setFormData({ name: '', email: '', message: '' });
    };

    return (
        <section id="contact" className="py-20">
            <div className="container mx-auto px-6 grid md:grid-cols-2 gap-12">
                <div>
                    <h2 className="text-3xl font-bold mb-6">Contact Us</h2>
                    <p className="mb-4">We would love to discuss how we can make your event memorable and impactful.</p>
                    <p><strong>Address:</strong> C/804, Shreeji Towers, Opp. Himalaya Mall, Ahmedabad - 380052</p>
                    <p><strong>Phone:</strong> +91 98255 88922, +91 99744 42337</p>
                    <p><strong>Email:</strong> tejashreeproductions@gmail.com</p>
                </div>
                <div>
                    <form className="bg-white shadow-lg p-6 rounded-lg" onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label className="block mb-2 font-medium">Your Name</label>
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                className="w-full border rounded px-4 py-2"
                                required
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block mb-2 font-medium">Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="w-full border rounded px-4 py-2"
                                required
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block mb-2 font-medium">Message</label>
                            <textarea
                                rows="4"
                                name="message"
                                value={formData.message}
                                onChange={handleChange}
                                className="w-full border rounded px-4 py-2"
                                required
                            ></textarea>
                        </div>
                        <button type="submit" className="btn-primary w-full">Send Message</button>
                    </form>
                </div>
            </div>
        </section>
    );
};

export default Contact;
