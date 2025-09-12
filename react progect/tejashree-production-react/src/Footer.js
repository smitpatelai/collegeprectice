import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-gray-800 text-white py-6">
            <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
                <p>&copy; 2025 Tejashree Production. All Rights Reserved.</p>
                <div className="flex space-x-4 mt-4 md:mt-0">
                    <a href="#facebook" className="social-icon text-white-400 hover:text-white-400" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="h-6 w-6" viewBox="0 0 24 24">
                            <path d="M22.675 0h-21.35C.6 0 0 .6 0 1.325v21.351C0 23.4.6 24 1.325 24H12.82v-9.294H9.692v-3.622h3.128V8.413c0-3.1 1.894-4.788 4.659-4.788 1.325 0 2.466.099 2.797.143v3.24l-1.918.001c-1.504 0-1.796.715-1.796 1.763v2.312h3.59l-.467 3.622h-3.123V24h6.116C23.4 24 24 23.4 24 22.675v-21.35C24 .6 23.4 0 22.675 0z"/>
                        </svg>
                    </a>
                    <a href="#instagram" className="social-icon text-white-400 hover:text-white-400" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="h-6 w-6" viewBox="0 0 24 24">
                            <path d="M7.75 2h8.5A5.75 5.75 0 0122 7.75v8.5A5.75 5.75 0 0116.25 22h-8.5A5.75 5.75 0 012 16.25v-8.5A5.75 5.75 0 017.75 2zm0 1.5A4.25 4.25 0 003.5 7.75v8.5A4.25 4.25 0 007.75 20.5h8.5a4.25 4.25 0 004.25-4.25v-8.5A4.25 4.25 0 0016.25 3.5h-8.5zM12 7a5 5 0 110 10 5 5 0 010-10zm0 1.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7zm4.75-.88a1.12 1.12 0 110 2.25 1.12 1.12 0 010-2.25z"/>
                        </svg>
                    </a>
                    <a href="#whatsapp" className="social-icon text-white-400 hover:text-white-400" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="h-6 w-6" viewBox="0 0 24 24">
                            <path d="M20.52 3.48A11.88 11.88 0 0012 0C5.373 0 0 5.373 0 12a11.88 11.88 0 001.64 6.04L0 24l5.96-1.64A11.88 11.88 0 0012 24c6.627 0 12-5.373 12-12 0-3.2-1.25-6.2-3.48-8.52zm-8.52 17.52a8.4 8.4 0 01-4.5-1.3l-.32-.2-3.54.98.95-3.45-.21-.34a8.4 8.4 0 1111.62 4.3zm4.3-6.1c-.23-.12-1.35-.67-1.56-.75-.21-.08-.36-.12-.51.12s-.58.75-.71.9c-.13.15-.26.17-.49.06-.23-.12-1-.37-1.9-1.17-.7-.62-1.17-1.38-1.31-1.6-.14-.23-.02-.35.1-.47.1-.1.23-.26.35-.39.12-.13.16-.22.25-.37.08-.12.04-.22-.02-.37-.06-.12-.51-1.23-.7-1.68-.18-.44-.36-.38-.51-.38-.13 0-.28 0-.43 0-.14 0-.37.05-.56.27-.19.23-.72.7-.72 1.7 0 1 .74 1.97.84 2.1.1.13 1.45 2.22 3.52 3.11 2.07.9 2.93.8 3.36.72.43-.08 1.35-.55 1.54-1.08.19-.53.19-.98.13-1.08-.06-.1-.21-.15-.44-.27z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
