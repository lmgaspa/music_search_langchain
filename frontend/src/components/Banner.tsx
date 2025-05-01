// src/components/Banner.tsx
import React, { useState } from 'react';
import './Banner.css';

const Banner: React.FC = () => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    if (!query.trim()) return;
  
    fetch(`https://music-search-langchain-f613d142ae31.herokuapp.com/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => {
        console.log('🎶 Resultado:', data);
        
      })
      .catch((err) => {
        console.error('Erro ao buscar:', err);
      });
  };
  

  return (
    <div className="banner">
      <div className="overlay">
        <h1 className="fw-bold">Busque sua música favorita</h1>
        <div className="input-group mt-3">
          <input
            type="text"
            className="form-control"
            placeholder="Digite aqui sua busca..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button className="btn btn-primary" onClick={handleSearch}>
            Buscar
          </button>
        </div>
      </div>
    </div>
  );
};

export default Banner;
