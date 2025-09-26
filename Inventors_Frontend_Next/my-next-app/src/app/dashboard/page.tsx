"use client";

import { useEffect, useState } from "react";
import { SidebarInset } from "@/components/ui/sidebar";
import { SiteHeader } from "@/components/site-header";

interface Article {
  id: number;
  title: string;
  source: string;
  date: string;
  summary: string;
}

const mockArticles: Article[] = [
  { id: 1, title: "AI Innovation in 2025", source: "TechCrunch", date: "Sep 25, 2025", summary: "Exploring the latest AI trends and how they're shaping the tech landscape." },
  { id: 2, title: "Quantum Computing Breakthrough", source: "Wired", date: "Sep 24, 2025", summary: "A new quantum algorithm promises faster computations for real-world problems." },
  { id: 3, title: "Renewable Energy Advances", source: "MIT Tech Review", date: "Sep 23, 2025", summary: "Innovations in solar and wind technologies are accelerating the green transition." },
];

export default function DashboardPage() {
  const [articles, setArticles] = useState<Article[] | null>(null);

  useEffect(() => {
    setTimeout(() => setArticles(mockArticles), 500);
  }, []);

  return (
    <SidebarInset>
      <SiteHeader />
      <div className="flex flex-1 flex-col gap-6 px-4 py-6 lg:px-6 md:py-6">
        {articles ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <div key={article.id} className="bg-card text-card-foreground rounded-xl p-6 shadow-md hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <h2 className="text-lg font-semibold mb-2">{article.title}</h2>
                <div className="flex justify-between items-center text-xs text-muted-foreground mb-2">
                  <span>{article.source}</span>
                  <span>{article.date}</span>
                </div>
                <p className="text-sm">{article.summary}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="bg-card rounded-xl p-6 animate-pulse space-y-3">
                <div className="h-6 bg-muted rounded w-3/4"></div>
                <div className="h-4 bg-muted rounded w-1/2"></div>
                <div className="h-4 bg-muted rounded w-full"></div>
              </div>
            ))}
          </div>
        )}
      </div>
    </SidebarInset>
  );
}
