import { useEffect, useState } from "react";
import "./App.css";
import { fetchArticles } from "./api";

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadArticles() {
      const data = await fetchArticles();
      setArticles(data);
      setLoading(false);
    }
    loadArticles();
  }, []);

  if (loading) return <div className="App"><h2>Loading articles...</h2></div>;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Inventors Articles</h1>
        {articles.length === 0 && <p>No articles found.</p>}
        <ul className="article-list">
          {articles.map((article) => (
            <li key={article.id} className="article-item">
              <a href={article.url} target="_blank" rel="noopener noreferrer">
                <h2>{article.title}</h2>
              </a>
              <p><strong>Source:</strong> {article.source}</p>
              <p><strong>Published:</strong> {new Date(article.published_date).toLocaleString()}</p>
              {article.summary && <p>{article.summary}</p>}
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
