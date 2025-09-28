// App.jsx
// Single-file React + Tailwind template for a Professional Entertainment Programs website.
// - Default export a React component
// - Tailwind CSS utility classes used (ensure Tailwind is set up in your project)
// - Replace placeholder images/text with real content
// - This file is designed to be a starting point and is responsive & accessible

import React from 'react';
import { motion } from 'framer-motion';

export default function EntertainmentSite() {
  const services = [
    { id: 1, title: 'Street Shows', desc: 'High-energy street performances engaging neighbourhoods and festivals.' },
    { id: 2, title: 'Puppet Shows', desc: 'Traditional & contemporary puppet stories for all ages.' },
    { id: 3, title: 'Bhavai & Folk', desc: 'Authentic Gujarati folk theatre for cultural programs.' },
    { id: 4, title: 'Orchestra', desc: 'Professional bands & DJs for weddings and corporate events.' },
  ];

  const gallery = Array.from({ length: 6 }).map((_, i) => ({
    id: i,
    alt: `Gallery image ${i + 1}`,
    src: `https://via.placeholder.com/600x400?text=Image+${i + 1}`,
  }));

  const testimonials = [
    { id: 1, name: 'Meera', role: 'Community Organizer', text: 'Amazing show — connected with our audience and raised awareness.' },
    { id: 2, name: 'Raj', role: 'Festival Director', text: 'Professional, timely and creative. Highly recommended.' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 text-slate-900">
      <header className="max-w-7xl mx-auto p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold">EP</div>
          <div>
            <h1 className="text-xl font-semibold">Entertainment Programs</h1>
            <p className="text-sm text-slate-600">Cultural & awareness performances — Gujarat</p>
          </div>
        </div>
        <nav className="hidden md:flex gap-6 items-center text-sm">
          <a href="#services" className="hover:underline">Services</a>
          <a href="#gallery" className="hover:underline">Gallery</a>
          <a href="#testimonials" className="hover:underline">Testimonials</a>
          <a href="#contact" className="bg-indigo-600 text-white px-4 py-2 rounded-md shadow-sm">Contact</a>
        </nav>
        <button className="md:hidden p-2 rounded-md bg-slate-100">☰</button>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {/* Hero */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center py-8">
          <motion.div initial={{ x: -30, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ duration: 0.6 }}>
            <h2 className="text-3xl md:text-4xl font-extrabold leading-tight">Bring Culture to Your Community</h2>
            <p className="mt-4 text-slate-700">We create memorable events — dramas, folk performances, puppet shows, and interactive street theatre focused on public awareness and engagement.</p>

            <div className="mt-6 flex flex-wrap gap-3">
              <a href="#contact" className="px-5 py-3 bg-indigo-600 text-white rounded-md shadow">Book a Show</a>
              <a href="#gallery" className="px-5 py-3 border border-slate-200 rounded-md">See Our Work</a>
            </div>

            <div className="mt-6 text-sm text-slate-500">Serving communities across Gujarat — customizable programs for festivals, schools, NGOs, and corporate CSR.</div>
          </motion.div>

          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.6 }}>
            <img src="https://via.placeholder.com/800x520?text=Hero+Performance" alt="Hero performance" className="w-full rounded-2xl shadow-lg object-cover" />
          </motion.div>
        </section>

        {/* Services */}
        <section id="services" className="py-12">
          <h3 className="text-2xl font-semibold">Our Services</h3>
          <p className="text-slate-600 mt-2">A mix of traditional and contemporary formats tailored to event goals.</p>

          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {services.map(s => (
              <article key={s.id} className="p-5 bg-white rounded-xl shadow-sm hover:shadow-md transition">
                <div className="w-12 h-12 rounded-md bg-indigo-50 flex items-center justify-center font-semibold text-indigo-600">{s.title[0]}</div>
                <h4 className="mt-4 font-semibold">{s.title}</h4>
                <p className="mt-2 text-sm text-slate-600">{s.desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* Gallery */}
        <section id="gallery" className="py-12">
          <h3 className="text-2xl font-semibold">Gallery</h3>
          <p className="text-slate-600 mt-2">A few snapshots from recent programs.</p>

          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {gallery.map(g => (
              <div key={g.id} className="rounded-lg overflow-hidden bg-white shadow-sm">
                <img src={g.src} alt={g.alt} className="w-full h-48 object-cover" />
                <div className="p-3 text-sm text-slate-600">{g.alt}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Testimonials & Brochure CTA */}
        <section id="testimonials" className="py-12 grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          <div className="lg:col-span-2">
            <h3 className="text-2xl font-semibold">Testimonials</h3>
            <div className="mt-4 space-y-4">
              {testimonials.map(t => (
                <blockquote key={t.id} className="p-4 bg-white rounded-lg shadow-sm">
                  <p className="text-slate-700">“{t.text}”</p>
                  <footer className="mt-2 text-sm text-slate-500">— {t.name}, {t.role}</footer>
                </blockquote>
              ))}
            </div>
          </div>

          <aside className="p-6 bg-indigo-600 text-white rounded-xl">
            <h4 className="font-bold text-lg">Download Brochure</h4>
            <p className="mt-2 text-sm opacity-90">One-pager PDF with program types, pricing, and logistics checklist.</p>
            <button className="mt-4 px-4 py-2 bg-white text-indigo-600 rounded-md font-medium">Download</button>
          </aside>
        </section>

        {/* Contact Form */}
        <section id="contact" className="py-12">
          <h3 className="text-2xl font-semibold">Contact Us</h3>
          <p className="text-slate-600 mt-2">Tell us about your event — date, place, audience size, and goal.</p>

          <form className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4" onSubmit={(e) => { e.preventDefault(); alert('Form submitted (replace with real submit).'); }}>
            <input required type="text" placeholder="Your name" className="p-3 rounded-md border border-slate-200" />
            <input required type="email" placeholder="Email" className="p-3 rounded-md border border-slate-200" />
            <input type="tel" placeholder="Phone (optional)" className="p-3 rounded-md border border-slate-200" />
            <input type="text" placeholder="Event location (city)" className="p-3 rounded-md border border-slate-200" />

            <textarea required placeholder="Tell us about the event, audience & objective" className="md:col-span-2 p-3 rounded-md border border-slate-200 min-h-[120px]"></textarea>

            <div className="md:col-span-2 flex items-center gap-3">
              <button type="submit" className="px-5 py-3 bg-indigo-600 text-white rounded-md">Send Inquiry</button>
              <button type="button" className="px-4 py-2 border rounded-md" onClick={() => alert('Call or WhatsApp: +91 99999 99999')}>Call / WhatsApp</button>
            </div>
          </form>
        </section>
      </main>

      <footer className="border-t mt-12 py-6">
        <div className="max-w-7xl mx-auto p-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-slate-600">© {new Date().getFullYear()} Entertainment Programs — Bringing culture to communities.</div>
          <div className="flex gap-4 text-sm">
            <a href="#" className="hover:underline">Privacy</a>
            <a href="#" className="hover:underline">Terms</a>
            <a href="#" className="hover:underline">Instagram</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
