import { useEffect, useState } from "react";
import { fetchArticles } from "./api";
import { Skeleton } from "@/components/ui/skeleton"; // Assuming Skeleton component is available

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadArticles() {
      const data = await fetchArticles();
      setArticles(data);
      setLoading(false);
    }
    loadArticles();
  }, []);

  const filteredArticles = articles
    .filter(a => !filter || a.source === filter)
    .filter(a => !search || a.title.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="App">
      <header className="App-header">
        <h1>Inventors</h1>
        <div className="controls">
          <input
            type="text"
            placeholder="Search articles..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          {articles.length > 0 && (
            <select
              className="filter-dropdown"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="">All Sources</option>
              {Array.from(new Set(articles.map((a) => a.source))).map((src) => (
                <option key={src} value={src}>{src}</option>
              ))}
            </select>
          )}
        </div>
      </header>

      {loading ? (
        <div className="loading">
          <Skeleton className="skeleton-card" />
          <Skeleton className="skeleton-card" />
          <Skeleton className="skeleton-card" />
        </div>
      ) : (
        <main className="article-container">
          {filteredArticles.length === 0 ? (
            <p className="no-articles">No articles found.</p>
          ) : (
            filteredArticles.map((article) => (
              <div key={article.id} className="article-item">
                <a href={article.url} target="_blank" rel="noopener noreferrer">
                  <h2>{article.title}</h2>
                </a>
                <div className="article-meta">
                  <span>{article.source}</span>
                  <span>
                    {new Date(article.published_date).toLocaleString(undefined, {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </span>
                </div>
                {article.summary && <p className="article-summary">{article.summary}</p>}
              </div>
            ))
          )}
        </main>
      )}
    </div>
  );
}

export default App;
