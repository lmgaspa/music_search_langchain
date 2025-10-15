// src/App.tsx
import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Banner from './components/Banner';

const App: React.FC = () => {
  return (
    <div>
      <Banner />
      <main>
        <section className="section text-center py-2">
          <h2>Why use our search engine?</h2>
          <p className="lead mt-3">
            With LangChain technology and YouTube integration, you can find music in a smart, fast, and fun way.
          </p>
        </section>

        <section className="section bg-light text-center py-0">
          <h2>Features</h2>
          <div className="row mt-4 justify-content-center">
            <div className="col-md-3">
              <h5>⚡ Fast</h5>
              <p>Instant results straight from YouTube.</p>
            </div>
            <div className="col-md-3">
              <h5>🎧 Smart</h5>
              <p>Understands what you really want to hear.</p>
            </div>
            <div className="col-md-3">
              <h5>🎤 Personalized</h5>
              <p>Searches tailored to your musical taste.</p>
            </div>
          </div>
          </section>
           <section className="section text-center py-2">
            <p>⚡ Powered by °AndesCore Software. 2025</p>
          <p>✉️ Email: andescoresoftware@gmail.com</p>
        </section>
      </main>
    </div>
  );
};

export default App;
