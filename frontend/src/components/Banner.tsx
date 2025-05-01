import React, { useState } from 'react';
import './Banner.css';

const Banner: React.FC = () => {
  const [query, setQuery] = useState('');
  interface Result {
    thumbnail: string;
    title: string;
    channel: string;
    url: string;
  }

  const [results, setResults] = useState<Result[]>([]);
  const [error, setError] = useState('');

  const handleSearch = () => {
    if (!query.trim()) return;

    fetch(`https://music-search-langchain-f613d142ae31.herokuapp.com/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => {
        console.log('🎶 Resultado:', data);
        if (data.results?.error) {
          setError(data.results.error);
          setResults([]);
        } else {
          setError('');
          setResults(data.results);
        }
      })
      .catch((err) => {
        console.error('Erro ao buscar:', err);
        setError('Erro ao buscar músicas');
        setResults([]);
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

        {error && <p className="text-danger mt-3">{error}</p>}

        {/* Resultados */}
        <div className="row mt-4">
          {results.map((item, index) => (
            <div className="col-md-4 mb-4" key={index}>
              <div className="card h-100">
                <img src={item.thumbnail} className="card-img-top" alt={item.title} />
                <div className="card-body">
                  <h5 className="card-title">{item.title}</h5>
                  <p className="card-text text-muted">{item.channel}</p>
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-outline-primary"
                  >
                    Assistir no YouTube
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Banner;
