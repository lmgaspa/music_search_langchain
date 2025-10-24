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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setShowResults(false);

    try {
      // Use environment variables for API configuration
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'https://music-search-langchain.onrender.com';
      const endpoint = import.meta.env.VITE_API_ENDPOINT || '/api/search';
      const response = await fetch(`${baseUrl}${endpoint}?q=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('🎶 Resultado:', data);
      setResults(data.results || []);
      setShowResults(true);
    } catch (err) {
      console.error('Erro ao buscar:', err);
      setError(err instanceof Error ? err.message : 'Erro desconhecido ao buscar música');
      setResults([]);
      setShowResults(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Banner com input */}
      <div className="banner bg-dark text-white py-5">
        <div className="container">
          <h1 className="fw-bold text-center mb-4">Search for your favorite music</h1>

          {/* Input centralizado e responsivo */}
          <div className="d-flex justify-content-center">
            <div className="input-group" style={{ maxWidth: '600px', width: '100%' }}>
              <input
                type="text"
                className="form-control"
                placeholder="Search for your favorite music 🎵"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              />
              <button 
                className="btn btn-primary" 
                onClick={handleSearch}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Searching...
                  </>
                ) : (
                  'Search'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="container my-3">
          <div className="alert alert-danger text-center" role="alert">
            <strong>Erro ao buscar música:</strong> {error}
            <br />
            <small>
              Possíveis causas: 
              <br />• Backend Render indisponível ou em manutenção
              <br />• Problema de conectividade com a internet
              <br />• Configuração de proxy do Vercel
              <br />
              <br />Tente novamente em alguns minutos ou verifique se o backend está funcionando.
            </small>
          </div>
        </div>
      )}

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