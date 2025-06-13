import React, { useState } from 'react';
import './Banner.css';

interface Video {
  title: string;
  url: string;
  channel: string;
  thumbnail?: string;
}

const Banner: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Video[]>([]);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = () => {
    if (!query.trim()) return;

    fetch(`https://musicsearchlangchain-d42cb3d95536.herokuapp.com/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => {
        console.log('🎶 Resultado:', data);
        setResults(data.results || []);
        setShowResults(true);
      })
      .catch((err) => {
        console.error('Erro ao buscar:', err);
        setResults([]);
        setShowResults(false);
      });
  };

  return (
    <>
      {/* Banner com input */}
      <div className="banner bg-dark text-white py-5">
        <div className="container">
          <h1 className="fw-bold text-center mb-4">Busque sua música favorita</h1>

          {/* Input centralizado e responsivo */}
          <div className="d-flex justify-content-center">
            <div className="input-group" style={{ maxWidth: '600px', width: '100%' }}>
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
      </div>

      {/* Resultados fora do banner */}
      {showResults && (
        <div className="container my-5">
          {results.length > 0 ? (
            <>
              <h3 className="text-center mb-4">Resultados encontrados:</h3>
              <div className="row g-4">
                {results.map((video, index) => (
                  <div key={index} className="col-sm-6 col-md-4 col-lg-3">
                    <div className="card h-100 shadow-sm">
                      {video.thumbnail && (
                        <img
                          src={video.thumbnail}
                          className="card-img-top"
                          alt={video.title}
                          style={{ height: '180px', objectFit: 'cover' }}
                        />
                      )}
                      <div className="card-body d-flex flex-column">
                        <h6 className="card-title">{video.title}</h6>
                        <p className="card-text text-muted">
                          Canal: <strong>{video.channel}</strong>
                        </p>
                        <a
                          href={video.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn btn-outline-primary btn-sm mt-auto"
                        >
                          Assistir no YouTube
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="text-center">Nenhum resultado encontrado.</p>
          )}
        </div>
      )}
    </>
  );
};

export default Banner;