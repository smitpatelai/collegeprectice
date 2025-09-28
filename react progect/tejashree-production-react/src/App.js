import React from "react";

// PerfectReactTemplate.jsx
// Single-file React template containing Header, Hero, About, Services, Gallery, Contact, Footer
// Tailwind CSS utility classes are used throughout. Paste this into src/App.jsx (or App.js) in a Vite/CRA + Tailwind project.

const Header = () => (
  <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white sticky top-0 z-50 shadow-md">
    <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center font-bold">EP</div>
        <div>
          <h1 className="font-semibold text-lg">Entertainment Programs</h1>
          <p className="text-xs opacity-80">Professional • Cultural • Social Awareness</p>
        </div>
      </div>

      <nav className="hidden md:flex gap-6 items-center">
        <a href="#about" className="hover:underline">About</a>
        <a href="#services" className="hover:underline">Services</a>
        <a href="#gallery" className="hover:underline">Gallery</a>
        <a href="#contact" className="hover:underline">Contact</a>
        <button className="ml-2 bg-white text-indigo-600 px-4 py-1.5 rounded-lg shadow-sm font-medium">Book Now</button>
      </nav>

      <div className="md:hidden">
        {/* Mobile burger (non-interactive in single-file template) */}
        <button aria-label="open menu" className="p-2 rounded-md bg-white/10">☰</button>
      </div>
    </div>
  </header>
);

const Hero = () => (
  <section className="bg-white/80 py-20">
    <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-8 items-center">
      <div>
        <h2 className="text-4xl md:text-5xl font-extrabold leading-tight">Bring your event to life with authentic cultural performances</h2>
        <p className="mt-4 text-lg text-gray-700">We produce professional dramas, street shows, puppet performances, garba, orchestras, and community awareness programs tailored for Gujarat and beyond.</p>
        <div className="mt-6 flex gap-3">
          <a href="#contact" className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg shadow hover:scale-[1.02] transition">Get a Quote</a>
          <a href="#gallery" className="inline-block border border-indigo-600 text-indigo-600 px-6 py-3 rounded-lg">View Gallery</a>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-3 text-sm text-gray-600">
          <div className="bg-gray-50 p-4 rounded-lg shadow-sm">
            <strong>150+</strong>
            <div>Shows performed</div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg shadow-sm">
            <strong>50+</strong>
            <div>Community campaigns</div>
          </div>
        </div>
      </div>

      <div className="rounded-2xl overflow-hidden shadow-lg bg-gradient-to-br from-indigo-50 to-purple-50 p-6">
        <div className="h-64 bg-gray-200 rounded-lg flex items-center justify-center text-gray-400">Hero image placeholder</div>
        <div className="mt-4 text-sm text-gray-600">Replace this with an image or carousel. Recommended: 1200×800 JPG/WEBP</div>
      </div>
    </div>
  </section>
);

const About = () => (
  <section id="about" className="py-16 bg-gray-50">
    <div className="max-w-5xl mx-auto px-6 text-center">
      <h3 className="text-3xl font-bold">About Us</h3>
      <p className="mt-3 text-gray-700">We are a team of performers, directors, writers and technicians focused on delivering high-impact cultural programs that educate and entertain. Our work is rooted in local traditions while meeting modern production standards.</p>

      <div className="mt-8 grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h4 className="font-semibold">Mission</h4>
          <p className="mt-2 text-sm text-gray-600">Raise awareness through storytelling and cultural expression.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h4 className="font-semibold">Vision</h4>
          <p className="mt-2 text-sm text-gray-600">Sustainable community engagement using traditional arts.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h4 className="font-semibold">Values</h4>
          <p className="mt-2 text-sm text-gray-600">Authenticity, quality, and respect for local culture.</p>
        </div>
      </div>
    </div>
  </section>
);

const servicesData = [
  { title: "Street Shows (Bhavai)", desc: "Mobile, high-energy performances for marketplaces and public spaces." },
  { title: "Puppet Shows", desc: "Educational puppet dramas for schools and community centers." },
  { title: "Professional Dramas", desc: "Stage productions with lighting, sound and complete crew." },
  { title: "Garba & Folk Dances", desc: "Traditional dance troupes for festivals and weddings." },
  { title: "Orchestra & Music", desc: "Live music bands and orchestra arrangements." },
  { title: "Community Campaigns", desc: "Awareness programs (health, environment, safety) with trained actors." }
];

const Services = () => (
  <section id="services" className="py-16">
    <div className="max-w-6xl mx-auto px-6">
      <h3 className="text-3xl font-bold text-center">Our Services</h3>
      <p className="text-center text-gray-600 mt-2">Full production, or one-time performances — we adapt to your needs.</p>

      <div className="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {servicesData.map((s) => (
          <div key={s.title} className="bg-white p-6 rounded-xl shadow hover:shadow-md transition">
            <h4 className="font-semibold">{s.title}</h4>
            <p className="mt-2 text-sm text-gray-600">{s.desc}</p>
            <div className="mt-4">
              <a href="#contact" className="text-indigo-600 text-sm">Enquire →</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

const Gallery = () => (
  <section id="gallery" className="py-16 bg-gray-50">
    <div className="max-w-6xl mx-auto px-6">
      <h3 className="text-3xl font-bold text-center">Gallery</h3>
      <p className="text-center text-gray-600 mt-2">A selection of photos and short videos from our recent shows.</p>

      <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-40 bg-gray-200 rounded-lg flex items-center justify-center text-gray-400">Image {i + 1}</div>
        ))}
      </div>
    </div>
  </section>
);

const Contact = () => (
  <section id="contact" className="py-16">
    <div className="max-w-3xl mx-auto px-6">
      <h3 className="text-3xl font-bold text-center">Contact Us</h3>
      <p className="text-center text-gray-600 mt-2">Tell us about your event and we’ll prepare a proposal.</p>

      <form className="mt-8 grid grid-cols-1 gap-4">
        <div className="grid sm:grid-cols-2 gap-4">
          <input className="p-3 border rounded-lg" placeholder="Your name" />
          <input className="p-3 border rounded-lg" placeholder="Phone or WhatsApp" />
        </div>
        <input className="p-3 border rounded-lg" placeholder="Email" />
        <textarea className="p-3 border rounded-lg" rows={5} placeholder="Tell us about the event (date, location, audience)" />
        <div className="flex items-center gap-3">
          <button type="submit" className="bg-indigo-600 text-white px-6 py-3 rounded-lg">Send Message</button>
          <div className="text-sm text-gray-500">Or call us: <strong>+91 99999 99999</strong></div>
        </div>
      </form>
    </div>
  </section>
);

const Footer = () => (
  <footer className="bg-indigo-900 text-white py-8">
    <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-6">
      <div>
        <h4 className="font-semibold">Entertainment Programs</h4>
        <p className="text-sm text-white/80 mt-2">Capturing culture, empowering communities.</p>
      </div>
      <div>
        <h4 className="font-semibold">Quick Links</h4>
        <ul className="mt-2 text-sm space-y-1">
          <li><a href="#about" className="underline">About</a></li>
          <li><a href="#services" className="underline">Services</a></li>
          <li><a href="#gallery" className="underline">Gallery</a></li>
        </ul>
      </div>
      <div>
        <h4 className="font-semibold">Social</h4>
        <p className="text-sm mt-2">Follow us on social media for updates.</p>
      </div>
    </div>

    <div className="mt-8 text-center text-xs text-white/60">© {new Date().getFullYear()} Entertainment Programs — All rights reserved.</div>
  </footer>
);

const App = () => {
  return (
    <div className="min-h-screen font-sans antialiased text-gray-900">
      <Header />
      <main>
        <Hero />
        <About />
        <Services />
        <Gallery />
        <Contact />
      </main>
      <Footer />
    </div>
  );
};

export default App;
