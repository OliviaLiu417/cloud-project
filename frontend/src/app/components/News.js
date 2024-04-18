"use client";
import React, { useState, useEffect } from "react";
import ExternalImage from "./ExternalImage";
import styles from "../styles/News.module.css";
import Link from "next/link";

const News = ({ category, selectedSource, setCounts }) => {
  const [articles, setArticles] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          process.env.NEXT_PUBLIC_SERVER_URL + "/news/"
        );
        const data = await response.json();
        const allArticles = data.flatMap((category) => category.articles);

        // Filter out articles with no url and articles that are not in the selected category
        const filteredArticles = allArticles.filter(
          (article) =>
            article.url !== "[Removed]" &&
            (category === "topHeadlines" ||
              data
                .find((cat) => cat.category === category)
                ?.articles.includes(article))
        );

        // Replace missing images with placeholders
        const articlesWithPlaceholders = filteredArticles.map((article) => ({
          ...article,
          urlToImage:
            article.urlToImage === "not_available"
              ? "not_available"
              : article.urlToImage,
        }));

        // Count news sources
        let counts = {};
        articlesWithPlaceholders.forEach((article) => {
          counts[article.source] = counts[article.source]
            ? counts[article.source] + 1
            : 1;
        });
        setCounts(counts);

        // Filter articles by selected source if selected from doughnut chart
        if (selectedSource) {
          const filteredArticles = articlesWithPlaceholders.filter(
            (article) => article.source === selectedSource
          );
          setArticles(filteredArticles);
          return;
        }
        setArticles(articlesWithPlaceholders);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
    };
    fetchData();
  }, [category, selectedSource]);

  return (
    <>
      <hr className={styles.split}></hr>
      <div className={styles.grid}>
        {articles.map((article, index) => (
          <a
            key={index}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.card}
          >
            <div className={styles.cardImage}>
              {article.urlToImage && article.urlToImage !== "not_available" ? (
                <ExternalImage src={article.urlToImage} alt={article.title} />
              ) : (
                <div className={styles.sourceBox}>
                  <p className={styles.sourceText}>{article.source}</p>
                </div>
              )}
            </div>
            <div className={styles.cardContent}>
              <p>{article.title}</p>
              <span>source: {article.source}</span>
            </div>
          </a>
        ))}
      </div>
    </>
  );
};

export default News;