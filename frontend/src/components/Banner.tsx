import React, { useState } from "react";
import "./Banner.css";

interface Result {
  thumbnail: string;
  title: string;
  channel: string;
  url: string;
}

const Banner: React.FC = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [error, setError] = useState("");

  const handleSearch = () => {
    if (!query.trim()) return;

    fetch(
      `https://music-search-langchain-f613d142ae31.herokuapp.com/search?q=${encodeURIComponent(
        query
      )}`
    )
      .then((res) => res.json())
      .then((data) => {
        console.log("🎶 Resultado:", data);
        if (data.results?.error) {
          setError(data.results.error);
          setResults([]);
        } else {
          setError("");
          setResults(data.results.slice(0, 8)); // Limita a 8 vídeos
        }
      })
      .catch((err) => {
        console.error("Erro ao buscar:", err);
        setError("Erro ao buscar músicas");
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
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
          <button className="btn btn-primary" onClick={handleSearch}>
            Buscar
          </button>
        </div>

        {error && <p className="text-danger mt-3">{error}</p>}

        {results.length > 0 && (
          <div className="video-grid mt-4 container">
            {results.map((video, index) => (
              <div key={index} className="video-card">
                <a href={video.url} target="_blank" rel="noopener noreferrer">
                  <img
                    src={video.thumbnail}
                    alt={video.title}
                    className="img-fluid"
                  />
                  <h5 className="mt-2">{video.title}</h5>
                  <p className="text-muted">{video.channel}</p>
                </a>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Banner;
