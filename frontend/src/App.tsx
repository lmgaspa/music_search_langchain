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
          <h2>Por que usar nosso buscador?</h2>
          <p className="lead mt-3">Com tecnologia LangChain e integração com YouTube, você encontra músicas de forma inteligente, rápida e divertida.</p>
          <p>Powered by °Simple Software. 2025</p>
        </section>

        <section className="section bg-light text-center py-0">
          <h2>Recursos</h2>
          <div className="row mt-4 justify-content-center">
            <div className="col-md-3">
              <h5>⚡ Rápido</h5>
              <p>Resultados instantâneos direto do YouTube.</p>
            </div>
            <div className="col-md-3">
              <h5>🎧 Inteligente</h5>
              <p>Entende o que você realmente quer ouvir.</p>
            </div>
            <div className="col-md-3">
              <h5>🎤 Personalizado</h5>
              <p>Buscas adaptadas ao seu gosto musical.</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default App;
