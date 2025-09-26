"use client";

import { useState } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";

const mockArticles = [
  {
    id: 1,
    title: "AI-powered biotech discovery",
    source: "Nature",
    image: "/placeholder.svg",
    category: "Biotech",
  },
  {
    id: 2,
    title: "Quantum computing startup raises $50M",
    source: "TechCrunch",
    image: "/placeholder.svg",
    category: "Quantum",
  },
  {
    id: 3,
    title: "New battery tech promises 5x efficiency",
    source: "IEEE Spectrum",
    image: "/placeholder.svg",
    category: "Energy",
  },
];

export default function Home() {
  const [filter, setFilter] = useState("All");

  const filteredArticles =
    filter === "All"
      ? mockArticles
      : mockArticles.filter((a) => a.category === filter);

  return (
    <div className="flex flex-col gap-6 p-6">
      {/* Filter */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Innovation Feed</h1>
        <select
          className="rounded-md border border-border bg-background px-3 py-2 text-sm"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="All">All</option>
          <option value="Biotech">Biotech</option>
          <option value="Quantum">Quantum</option>
          <option value="Energy">Energy</option>
        </select>
      </div>

      {/* Articles */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filteredArticles.map((article) => (
          <div
            key={article.id}
            className="rounded-lg border border-border bg-card shadow-sm hover:shadow-md transition"
          >
            <Image
              src={article.image}
              alt={article.title}
              width={400}
              height={200}
              className="w-full rounded-t-lg object-cover"
            />
            <div className="p-4 flex flex-col gap-2">
              <h2 className="font-semibold text-lg">{article.title}</h2>
              <p className="text-sm text-muted-foreground">{article.source}</p>
              <Button variant="secondary" className="mt-2 w-fit">
                Read more
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
